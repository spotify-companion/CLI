from rich import print
from rich.pretty import Pretty
from rich.panel import Panel
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Column, Table

class Logger:
    __shared_instance = "Logger"
    @staticmethod
    def get_instance():
        """ Static access for singleton implementation""" 

        if Logger.__shared_instance == "Logger":
            Logger()
        
        return Logger.__shared_instance

    def __init__(self):
        Logger.__shared_instance = self
        FORMAT = "%(message)s"
        logging.basicConfig(
             format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )
        self.log = logging.getLogger("rich")
        # self.log.info("Hello, World!")
                

class Printer:
    __shared_instance = "Printer"
    @staticmethod
    def get_instance():
        """ Static access for singleton implementation""" 

        if Printer.__shared_instance == "Printer":
            Printer()
        
        return Printer.__shared_instance

    def __init__(self):
        Printer.__shared_instance = self
        self.console = Console()
        self.table = Table()
    
    def printPlayList(self, data, headers, name = None):
        table = Table(show_header=True, header_style="bold magenta", title=name)
        for col in headers:
            table.add_column(col, justify="center")
        for row in data:
             table.add_row(row[0], row[1])
                
        self.console.print(table)

