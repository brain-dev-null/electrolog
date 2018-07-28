import os
import monitor_connection
import pandas as pd

path = str(os.path.abspath(__file__)).replace("src/main.py", "")

URL = "http://192.168.178.14"

blocks = {"1":"year", "2":"week", "3":"day", "4":"hour"}

print("Welcome to Electro Log!\nFollowing data is available:"+
        "\n[1]---Past Year (Daily Data)"+
        "\n[2]---Past Week (Hourly Data)"+
        "\n[3]---Past Day  (10-minute-intervall Data)"+
        "\n[4]---Past Hour (Minutely Data)\n\n")

dataset_index = input("Please select dataset [1-4]:")
time_block = blocks[dataset_index]

PW = input("Please enter your password:")

requestor = monitor_connection.requestor(URL, PW)
dataset = requestor.getData(time_block)
index = dataset.index.tolist()
begin = str(index[0])
end = str(index[len(index) - 1])
begin.replace(" ", "_")
end.replace(" ", "_")

dataset.to_csv(path_or_buf= path + time_block + "_" + str(begin) + "_to_" + str(end) + ".csv")