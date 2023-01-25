from colorama import Fore, Back, Style
import logging


class Logger:
    def info(self, info):
        print(Fore.LIGHTBLUE_EX + "INFO" + Fore.BLACK + ":" + 4 * " ", info)

    def error(self, error):
        print(Fore.RED + "ERROR" + Fore.BLACK + ":" + 3 * " ", error)

    def success(self, msg):
        print(Fore.GREEN + "SUCCESS" + Fore.BLACK + ":" + 1 * " ", msg)


log = Logger()


logging.basicConfig(level="INFO")

cronLogger = logging.getLogger("cron")
