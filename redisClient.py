import socket
from os import getenv


class RawRedisClient:

    def __init__(self):
        self.redis_connection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.redis_connection.connect(
            (getenv("REDIS_HOST"), int(getenv("REDIS_PORT"))))

    def _send_redis_command(self, *args):
        # RESP protocol for sending array
        command = f"*{len(args)}\r\n"
        for arg in args:
            command += f"${len(str(arg))}\r\n{arg}\r\n"
        self.redis_connection.send(command.encode())
        return self._parse_redis_response()

    def _parse_redis_response(self):
        """Parse Redis RESP protocol response"""
        response = self.redis_connection.recv(4096).decode().strip()
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
