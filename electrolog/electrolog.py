import tkinter as tk
import logging

from typing import Optional

from electrolog.views import LoginView

LOGGER = logging.getLogger(__name__)


def main(dev_mode: bool, default_ip: Optional[str] = "") -> None:
    LOGGER.info("Starting electrolog")
    if dev_mode:
        LOGGER.debug("electrolog is running in dev-mode")

    root = tk.Tk()
    root.title("electrolog")

    LoginView(root, default_ip=default_ip)

    root.mainloop()
