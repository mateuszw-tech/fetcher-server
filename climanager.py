from typing import Callable

from server import Server
import asyncio
from threading import Thread
from rich.console import Console
import sys


class CliManager:

    def __init__(self):
        self.server = Server('127.0.0.1', 55555)
        self.console = Console()
        self.commands = {
            "show_active_clients": self.display_active_clients,
            "send_instructions": self.send_instructions_to_client,
            "send_instructions_to_all_clients": print,
            "close": sys.exit
        }

    def display_active_clients(self):
        self.server.show_active_clients()

    def send_instructions_to_client(self):
        asyncio.run(self.server.send_instructions_to_one_client())

    def launch_cli(self):
        self.display_welcome_message()
        self.initiate_server()
        self.run_app_menu()

    def display_welcome_message(self):
        print()
        self.console.rule("[pale_green3]\n Welcome to Webscraper [/pale_green3]")
        self.console.print(f"[pale_green3]server is running on {self.server.host}:{self.server.port}", justify="center")

    def initiate_server(self):
        server_thread = Thread(target=self.run_server, daemon=True)
        server_thread.start()

    def run_server(self):
        asyncio.run(self.server.run_server())

    def run_app_menu(self) -> None:
        while True:
            self.console.print("\n[pale_green3]available options:", justify="left")

            for command in self.commands:
                self.console.print(f"‣ {command}", justify="left")

            input_from_user = self.console.input("[dark_red]Command: [/dark_red]")

            if input_from_user in self.commands:
                self.commands[input_from_user]()
            else:
                self.console.print("[indian_red]Invalid command")
