import os
import sys

sys.path.append(os.getcwd())

from whitebox.utils.passwords import decrypt_api_key
from whitebox.core.settings import get_settings

value = sys.argv[1]
settings = get_settings()

if __name__ == "__main__":
    api_key = decrypt_api_key(value, settings.SECRET_KEY.encode())
    print(api_key)
