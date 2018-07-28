import os
import monitor_connection
import pandas as pd

URL = "http://192.168.178.14"
blocks = {"1":"year", "2":"week", "3":"day", "4":"hour"}

print("Welcome to Electro Log!\nFollowing data is available:"+
        "\n[1]---Past Year (Daily Data)"+
        "\n[2]---Past Week (Hourly Data)"+
        "\n[3]---Past Day  (10-minute-intervall Data"+
        "\n[4]---Past Hour (Minutely Data\n\n")

dataset_index = input("Please select dataset [1-4]:")
time_block = blocks[dataset_index]

PW = input("Please enter your password:")

requestor = monitor_connection.requestor(URL, PW)
dataset = requestor.getData(time_block)
dataset.to_csv(path_or_buf=os.path.dirname(__file__)+"electro_log_"+time_block+".csv")