import os
import subprocess
import platform
from server import Server
import asyncio
from threading import Thread
from rich.console import Console
from rich.table import Table
import sys


class CliManager:
    # todo: Api key w env variable, Agent musi podać przy łączeniu się API key

    def __init__(self):
        self.server = Server('127.0.0.1', 55555)
        self.console = Console()
        self.commands = {
            "display_active_clients": self.display_active_clients,
            "find_advertisement_by_phone_number": self.find_by_phone_number,
            "send_settings_to_client": self.send_settings_to_client,
            "start_fetching": self.start_fetching_data,
            "stop_fetching": self.stop_fetching_data,
            "settings": self.open_settings,
            "help": self.display_help_menu,
            "close": sys.exit
        }
        self.shortcuts = {
            "-dac": self.display_active_clients,
            "-fa": self.find_by_phone_number,
            "-sf": self.start_fetching_data,
            "-st": self.stop_fetching_data,
            "-sstc": self.send_settings_to_client,
            "-s": self.open_settings,
            "-h": self.display_help_menu,
            "-c": sys.exit
        }
        self.settings_path = "settings.json"

    def display_help_menu(self) -> None:
        help_menu_table = Table(title="Help")

        help_menu_table.add_column("COMMAND", justify="left", style="cyan", no_wrap=True)
        help_menu_table.add_column("SHORTCUT", justify="center", style="magenta")
        help_menu_table.add_column("DESCRIPTION", justify="left")

        help_menu_table.add_row("display_active_clients", "-dac", "Displaying connected clients")
        help_menu_table.add_row("find_advertisement_by_phone_number", "-fa",
                                "Find advertisement in database by searching with phone number")
        help_menu_table.add_row("start_fetching", "-sf", "Start fetching data on specific client")
        help_menu_table.add_row("stop_fetching", "-st", "Stop fetching data on specific client")
        help_menu_table.add_row("send_settings_to_client", "-sstc", "Update fetcher settings on specific client")
        help_menu_table.add_row("settings", "-s", "Open settings file which can be updated to client")
        help_menu_table.add_row("help", "-h", "Display help menu")
        help_menu_table.add_row("close", "-c", "Close the program")

        self.console.print(help_menu_table, justify="center")

    def open_settings(self):
        if platform.system() == 'Darwin':
            subprocess.call(('open', self.settings_path))
        elif platform.system() == 'Windows':
            os.startfile(self.settings_path)
        elif platform.system() == 'Linux':
            subprocess.call(('xdg-open', self.settings_path))

    def send_settings_to_client(self):
        asyncio.run(self.server.update_client_settings())

    def find_by_phone_number(self):
        phone_number = self.console.input("[dark_red]Phone number: [/dark_red]")
        self.console.print(f"[red]{self.server.find_advertisement_in_db_by_phone_number(phone_number)}")

    def start_fetching_data(self):
        asyncio.run(self.server.start_fetching())

    def stop_fetching_data(self):
        asyncio.run(self.server.stop_fetching())

    def display_active_clients(self):
        self.server.show_active_clients()

    def update_settings_to_client(self):
        asyncio.run(self.server.update_client_settings())

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
            elif input_from_user in self.shortcuts:
                self.shortcuts[input_from_user]()
            else:
                self.console.print("[indian_red]Invalid command")
