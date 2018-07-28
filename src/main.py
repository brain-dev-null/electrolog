import os
import monitor_connection
import pandas as pd

def run(URL, PW):
    print("\nFollowing data is available:"+
            "\n[1]---Past Year (Daily Data)"+
            "\n[2]---Past Week (Hourly Data)"+
            "\n[3]---Past Day  (10-minute-intervall Data)"+
            "\n[4]---Past Hour (Minutely Data)\n\n")
    dataset_index   = input("Please select dataset [1-4]:")
    time_block      = blocks[dataset_index]
    requestor       = monitor_connection.requestor(URL, PW)
    dataset         = requestor.getData(time_block)
    dates           = dataset["Date"].tolist()
    begin           = dates[0]
    end             = dates[len(dates) - 1]
    begin_string    = str(begin.year) + "-" + str(begin.month) + "-" + str(begin.day) + "-" + str(begin.hour) + "h" + str(begin.minute) + "m"
    end_string      = str(end.year) + "-" + str(end.month) + "-" + str(end.day) + "-" + str(end.hour) + "h" + str(end.minute) + "m"

    dataset.to_csv(path_or_buf= path + time_block + "_" + begin_string + "_to_" + end_string + ".csv")

    if (input("Create another dataset?[y/n]") == "y"):
        return True
    else:
        return False

path    = str(os.path.abspath(__file__)).replace("src/main.py", "").replace("src\\main.py", "")
blocks  = {"1":"year", "2":"week", "3":"day", "4":"hour"}

print("----Welcome to Electro Log!----\n")

URL     = "http://192.168.178.14"
PW      = input("Please enter your password:")

while(run(URL, PW) == True):
    pass


