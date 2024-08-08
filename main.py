import asyncio
from server import Server

server = Server('127.0.0.1', 55555)
asyncio.run(server.start_server())
