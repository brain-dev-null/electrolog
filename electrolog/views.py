import logging
import os
import requests
import tkinter as tk
import time
import re
from tkinter import filedialog, ttk
from typing import Optional

from electrolog.data import (
    download_past_hour,
    download_past_day,
    download_past_week,
    download_past_year,
)

LOGGER = logging.getLogger(__name__)

BYTE = r"(25[0-5]|2[0-4]\d|1\d\d|\d\d?)"
IP_PATTERN = f"{BYTE}\\.{BYTE}\\.{BYTE}\\.{BYTE}"
IP_REGEX = re.compile(IP_PATTERN)


class LoginView:
    def __init__(self, root: tk.Tk, default_ip: Optional[str] = "") -> None:

        if os.path.isfile("ip.txt"):
            with open("ip.txt", "r") as ip_file:
                default_ip = ip_file.read()

        self.root = root
        self.login_form = tk.Frame(root, padx=15, pady=15)

        self.ip_var = tk.StringVar(self.login_form, value=default_ip)
        self.pw_var = tk.StringVar(self.login_form)

        ip_entry = tk.Entry(
            self.login_form,
            width=20,
            justify="center",
            textvariable=self.ip_var,
        )
        ip_entry.grid(row=0, column=1, sticky="e")

        ip_label = tk.Label(self.login_form, text="IP address: ")
        ip_label.grid(row=0, column=0, sticky="e")

        password_entry = tk.Entry(
            self.login_form,
            width=20,
            justify="center",
            show="*",
            textvariable=self.pw_var,
        )
        password_entry.grid(row=1, column=1, sticky="e")

        password_label = tk.Label(self.login_form, text="Password: ")
        password_label.grid(row=1, column=0, sticky="e")

        login_button = tk.Button(
            self.login_form,
            pady=1,
            text="Login",
            relief="groove",
            command=self.login_button_callback,
        )
        login_button.grid(row=2, columnspan=2, pady=10)

        self.login_form.pack()

    def login_button_callback(self) -> None:
        IP = self.ip_var.get()
        PASSWORD = self.pw_var.get()

        if IP is None or len(IP) == 0:
            LOGGER.warning("Missing IP address!")
            ErrorView("IP address is missing!")
            return

        if IP_REGEX.fullmatch(IP) is None:
            LOGGER.warning('Invalid IP address "{IP}"!')
            ErrorView("IP address invalid!")
            return

        if PASSWORD is None or len(PASSWORD) == 0:
            LOGGER.warning("Missing password!")
            ErrorView("Password is missing!")
            return

        host = f"http://{IP}"
        LOGGER.info(f'Attempting to login at host "{host}"')

        url = f"{host}/l"
        params = {"w": PASSWORD}

        session = requests.Session()

        try:
            preflight = requests.get(host, timeout=5)
            if "Wachtwoord" not in preflight.text:
                LOGGER.warning(f"Preflight to {host} failed!")
                ErrorView("Wrong IP!")
                return

            LOGGER.debug("Preflight successful!")

            time.sleep(0.5)

            login = session.get(url, params=params, timeout=5)

            if login.ok:
                LOGGER.info("Login successful!")
                self.login_form.destroy()
                with open("ip.txt", "w") as ip_file:
                    ip_file.write(IP)
                DataSelectionView(self.root, session, host)

            else:
                LOGGER.warning("Login failed!")
                ErrorView("Login failed! Check password.")

        except requests.Timeout:
            LOGGER.exception("Timeout during login")
            ErrorView("Login timeout! Check IP address.")

        except requests.exceptions.ConnectionError:
            LOGGER.exception("Connection error during login")
            ErrorView("Connection error! Check IP address.")


class ErrorView:
    def __init__(self, message: str) -> None:
        self.root = tk.Tk()
        self.root.title("electrolog - Warning!")

        tk.Label(self.root, text=message, padx=40, pady=20).pack()
        tk.Button(
            self.root, text="Ok", padx=10, pady=5, command=self.ok_callback
        ).pack(pady=10)

        self.root.mainloop()

    def ok_callback(self) -> None:
        self.root.destroy()


class DataSelectionView:
    GRANULARITIES = [
        "Past year (daily)",
        "Past week (hourly)",
        "Past day (10 min intervalls)",
        "Past hour (minutely)",
    ]

    def __init__(
        self, root: tk.Tk, session: requests.Session, base_url: str
    ) -> None:
        self.session = session
        self.root = root
        self.base_url = base_url
        self.data_selection_form = tk.Frame(root, padx=15, pady=15)

        self.range_selection = ttk.Combobox(
            self.data_selection_form,
            values=self.GRANULARITIES,
            state="readonly",
        )
        self.range_selection.set("Pick a data range")

        export_button = ttk.Button(
            self.data_selection_form,
            text="Download data",
            command=self.export_callback,
        )

        self.range_selection.pack(pady=10)
        export_button.pack(pady=10)

        self.data_selection_form.pack()

    def export_callback(self) -> None:
        selected_range = self.range_selection.get()
        index = self.GRANULARITIES.index(selected_range)

        LOGGER.info(f'Export using range "{selected_range}"')

        match index:
            case 0:
                data = download_past_year(self.session, self.base_url)
            case 1:
                data = download_past_week(self.session, self.base_url)
            case 2:
                data = download_past_day(self.session, self.base_url)
            case 3:
                data = download_past_hour(self.session, self.base_url)

        output_file = filedialog.asksaveasfilename(
            title="Store retrieved data",
            initialfile="output",
            defaultextension=".xls",
        )

        LOGGER.info(f'Store data at "{output_file}"')

        if len(output_file) > 0:
            data.to_excel(output_file)
