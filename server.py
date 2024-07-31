import json
from threading import Thread
import socket
from time import sleep
import os

# HOST = '127.0.0.1'
# PORT = 55555


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer_size = 2048
        self.delimiter = b"\\r\\n"
        self.buffer = b""

    def receive_data_from_the_client(self, client: socket.socket):
        while True:
            try:
                print(self.get_line_from_socket(client))
            except Exception as e:
                print(e)

    def handle_terminal(self, client: socket.socket):
        pass

    def receive_data_thread(self, client_connection_socket: socket.socket):
        receive_thread = Thread(target=self.receive_data_from_the_client, args=(client_connection_socket,))
        receive_thread.start()
        receive_thread.join()

    def get_line_from_socket(self, client: socket.socket):
        while self.delimiter not in self.buffer:
            data = client.recv(self.buffer_size)
            if not data:
                return None
            self.buffer += data
        line, sep, self.buffer = self.buffer.partition(self.delimiter)
        return line.decode("utf-8")

    def handle_client(self, client_connection_socket: socket.socket, addr) -> None:
        with client_connection_socket:
            print(f'Connected by: {addr}')
            self.receive_data_thread(client_connection_socket)

    def get_client_connection(self, server_socket: socket.socket):
        while True:
            client_connection_socket, client_connection_address = server_socket.accept()
            try:
                self.handle_client(client_connection_socket, client_connection_address)
            except Exception as e:
                print(f"Client Disconnected, {e}")

    def start_server(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f'Server listening on port {self.host}:{self.port}')

            self.get_client_connection(server_socket)  # TODO: Thready na klientów / zmienić na get client connections

# TODO: Obsłużyć przypadek 2 list w sockecie
# TODO: Rozgraniczyć listy JSON'owe, sprawdzić czy w stringu jest pełny JSON
