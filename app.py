from base_telegram import BaseTelegram
from dotenv import load_dotenv
import os

def main() -> None:
    """
        main function
    """
    load_dotenv()
    BaseTelegram(token=os.environ.get("BOT_TOKEN"))


if __name__ == "__main__":
    """BaseTelegram Test"""
    main()

    while(True):
        pass