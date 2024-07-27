import json
import threading
import socket


# HOST = '127.0.0.1'
# PORT = 55555


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def process_data(data) -> None:
        if data:
            print(f'Received {data}')
        else:
            print("No data to process")

    # TODO: Obsłużyć przypadek 2 list w sockecie
    # TODO: Rozgraniczyć listy JSON'owe, sprawdzić czy w stringu jest pełny JSON

    def handle_client(self, conn: socket.socket, addr) -> None:
        with conn:
            print(f'Connected by: {addr}')
            data = b''
            while True:
                packet = conn.recv(4096)
                print(f"{packet.decode('utf-8')}")
                if not packet:
                    break
                data += packet
            # data = data.decode('utf-8')
            # self.process_data(data)

    def start_server(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f'Server listening on port {self.host}:{self.port}')
            while True:
                conn, addr = s.accept()
                self.handle_client(conn, addr)

# class Server:
#     def __init__(self, host: str, port: int):
#         self.host = host
#         self.port = port
#
#     @staticmethod
#     def process_data(data: str) -> None:
#         try:
#             json_data = json.loads(data)
#             print(f'Received JSON data: {json_data}')
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#
#     def handle_client(self, conn: socket.socket, addr) -> None:
#         with conn:
#             print(f'Connected by: {addr}')
#             buffer = b''
#             while True:
#                 packet = conn.recv(4096)
#                 print(f"x + {packet}")
#                 if not packet:
#                     break
#                 buffer += packet
#
#                 # Decode the buffer into a string
#                 buffer_str = buffer.decode('utf-8')
#
#                 # Process each complete JSON object
#                 while True:
#                     try:
#                         # Find the end of the JSON object
#                         end_idx = buffer_str.find('\n')
#                         if end_idx == -1:
#                             # No complete JSON object found
#                             break
#
#                         # Extract JSON object and remove it from the buffer
#                         json_str = buffer_str[:end_idx]
#                         buffer_str = buffer_str[end_idx + 1:]
#                         self.process_data(json_str)
#                     except json.JSONDecodeError as e:
#                         print(f"Error decoding JSON: {e}")
#                         break
#
#                 # Update buffer with remaining data
#                 buffer = buffer_str.encode('utf-8')
#
#     def start_server(self) -> None:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.bind((self.host, self.port))
#             s.listen()
#             print(f'Server listening on {self.host}:{self.port}')
#             while True:
#                 conn, addr = s.accept()
#                 self.handle_client(conn, addr)

    # def manage_clients(self, conn: socket.socket) -> None:
    #     change_settings = input("do you want to change settings? y/n")
    #     if change_settings == 'y':
    #         # fetcher = input("which fetcher settings do you want to change?")
    #         # #match - case do innych fetcherów
    #         cities = input("which city do you want to collect?")
    #         fetcher_settings: dict = {"fetcher": fetcher, "cities": cities}
    #         conn.send(json.dumps(fetcher_settings).encode('utf-8'))
    #     elif change_settings == 'n':
    #         pass
    #     else:
    #         pass
