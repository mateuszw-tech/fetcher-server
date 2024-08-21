import asyncio
from server import Server
from climanager import CliManager

manager = CliManager()

if __name__ == '__main__':
    manager.launch_cli()
