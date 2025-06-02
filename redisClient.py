import socket
from os import getenv
import atexit


class RawRedisClient:

    def __init__(self):
        self._host = getenv("REDIS_HOST")
        self._port = int(getenv("REDIS_PORT"))
        self._timeout = float(getenv("REDIS_TIMEOUT", "5.0"))
        self._connection = None
        self._connect()
        atexit.register(self.close)

    def _connect(self):
        try:
            self._connection = socket.create_connection(
                (self._host, self._port), timeout=self._timeout)
        except (socket.timeout, ConnectionError) as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")

    def _ensure_connection(self) -> None:
        if self._connection is None:
            self._connect()

    def close(self):
        if self._connection:
            try:
                self._connection.close()
            except:
                pass
            finally:
                self._connection = None

    def _send_redis_command(self, *args):
        # RESP protocol for sending array
        try:
            self._ensure_connection()
            command = [f"*{len(args)}\r\n"]
            for arg in args:
                command.append(f"${len(str(arg))}\r\n{arg}\r\n")
            self._connection.sendall("".join(command).encode())
            return self._parse_redis_response()
        except (ConnectionError, socket.timeout) as e:
            # closing broken connection
            self.close()
            raise ConnectionError(f"Redis command failed: {str(e)}")

    def _parse_redis_response(self):
        """Parse Redis RESP protocol response"""
        try:
            response = self._connection.recv(4096).decode().strip()
            if response.startswith('+'):
                return response[1:]  # Simple string
            elif response.startswith('$'):
                length = int(response[1:].split('\r\n')[0])
                if length == -1:
                    return None
                return response.split('\r\n')[1]
            elif response.startswith(':'):
                return int(response[1:])
            elif response.startswith('*'):
                items = []
                parts = response.split('\r\n')
                count = int(parts[0][1:])
                for i in range(1, count*2, 2):
                    items.append(parts[i+1])
                return items
            return response
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid Redis response: {str(e)}")
