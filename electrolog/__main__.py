import logging
import sys

from electrolog.views import IP_REGEX
from electrolog.electrolog import main

if __name__ == "__main__":
    in_dev = "--dev" in sys.argv
    if IP_REGEX.fullmatch(sys.argv[-1]) is not None:
        default_ip = sys.argv[-1]
    else:
        default_ip = ""

    if in_dev:
        handler = logging.StreamHandler()
        log_level = logging.DEBUG
    else:
        handler = logging.FileHandler("electrolog.log")
        log_level = logging.INFO

    logging.basicConfig(
        level=logging.DEBUG,
        style="{",
        format="{asctime} - {levelname:<8} - {filename}:{funcName}:{lineno} - "
        "{message}",
        handlers=[handler],
    )

    main(in_dev, default_ip=default_ip)
