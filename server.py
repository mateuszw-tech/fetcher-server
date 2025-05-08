import asyncio
import database_manager
import json
import os


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.buffer = b""
        self.delimiter = b"\r\n"
        self.buffer_size = 2048
        self.databaseManager = database_manager.DatabaseManager()
        self.api_key = os.getenv('FetcherApiKey')

    async def get_line_from_buffer(self, reader: asyncio.StreamReader) -> str:
        while self.delimiter not in self.buffer:
            data = await reader.read(self.buffer_size)
            if not data:
                break
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(self.delimiter)
        return line.decode(encoding='UTF-8')

    async def get_data_from_client(self, client):
        reader, writer = client
        addr = writer.get_extra_info('peername')
        try:
            while True:
                advertisement_info: str = await self.get_line_from_buffer(reader)
                self.databaseManager.insert_advertisement_info_to_database(json.loads(advertisement_info))
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            self.clients.remove((reader, writer))
            writer.close()
            await writer.wait_closed()

    async def get_data_from_all_clients(self) -> None:
        for client in self.clients:
            await self.get_data_from_client(client)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        api_key = await reader.read(1024)
        if api_key.decode() == self.api_key:
            self.clients.append((reader, writer))

            writer.write("Valid API key".encode('utf-8'))
            await writer.drain()

            await self.get_data_from_client((reader, writer))
        else:
            writer.write("Invalid API key".encode('utf-8'))
            await writer.drain()

            writer.close()
            await writer.wait_closed()

    def show_active_clients(self) -> None:
        print("Available clients:")
        for i, (_, writer) in enumerate(self.clients):
            addr = writer.get_extra_info('peername')
            print(f"{i}: {addr}")

    def find_advertisement_in_db_by_phone_number(self, phone_number: str) -> dict:
        return self.databaseManager.return_advertisement_in_db_by_phone_number(phone_number)

    async def update_client_settings(self) -> None:
        if self.clients:
            try:
                client_index = int(input("Select client index to send instructions: "))
                reader, writer = self.clients[client_index]
                settings = json.dumps(json.load(open('settings.json', 'r')))
                writer.write(settings.encode())
                await writer.drain()
                print(f"settings sent to: {writer.get_extra_info('peername')}")
            except (ValueError, IndexError):
                print("Invalid client index")
        else:
            print("No clients connected")

        await asyncio.sleep(1)

    async def start_fetching(self) -> None:
        if self.clients:
            try:
                client_index = int(input("Select client index you want to start: "))
                reader, writer = self.clients[client_index]
                instruction = "fetch"
                writer.write(instruction.encode())
                await writer.drain()
                print(f"Sent instruction to {writer.get_extra_info('peername')}")
            except (ValueError, IndexError):
                print("Invalid client index")
        else:
            print("No clients connected")

        await asyncio.sleep(1)

    async def stop_fetching(self) -> None:
        if self.clients:
            try:
                client_index = int(input("Select client index you want to stop: "))
                reader, writer = self.clients[client_index]
                instruction = "stop"
                writer.write(instruction.encode())
                await writer.drain()
                print(f"Sent instruction to {writer.get_extra_info('peername')}")
            except (ValueError, IndexError):
                print("Invalid client index")
        else:
            print("No clients connected")

        await asyncio.sleep(1)

    async def run_server(self) -> None:
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with server:
            await server.serve_forever()

    async def stop_server(self) -> None:
        pass
