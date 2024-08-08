import asyncio
from climanager import *


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.active_client = None
        self.buffer = b""
        self.delimiter = b"\\r\\n"
        self.buffer_size = 2048

    async def get_line_from_buffer(self, reader: asyncio.StreamReader) -> str:
        while self.delimiter not in self.buffer:
            data = await reader.read(self.buffer_size)
            if not data:
                break
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(self.delimiter)
        return line.decode()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info('peername')
        print(f'Connected by: {addr}')
        self.clients.append((reader, writer))
        print(f'{self.clients}')
        if self.active_client is None:
            self.active_client = writer

        try:
            while True:
                message: str = await self.get_line_from_buffer(reader)
                print(f"Received from {addr}: {message}")
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            self.clients.remove((reader, writer))
            writer.close()
            await writer.wait_closed()

    async def send_instructions(self):
        while True:
            if self.clients:
                print("Available clients:")
                for i, (_, writer) in enumerate(self.clients):
                    addr = writer.get_extra_info('peername')
                    print(f"{i}: {addr}")

                try:
                    client_index = int(input("Select client index to send instructions: "))
                    reader, writer = self.clients[client_index]

                    instruction = input("Enter instruction to send: ")
                    writer.write(instruction.encode())
                    await writer.drain()
                    print(f"Sent instruction to {writer.get_extra_info('peername')}")
                except (ValueError, IndexError):
                    print("Invalid client index")
            else:
                print("No clients connected")

            await asyncio.sleep(1)

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'Server listening on {addr}')

        async with server:
            await asyncio.gather(server.serve_forever(), self.send_instructions())
