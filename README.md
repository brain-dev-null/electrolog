# __Electro Log__

Electro Log is a python-based data-analysis-tool that communicates with a *"You Less LS110"* kWh-meter that logs the electrical power usage in a household and provides its data via an API specified [here](http://wiki.td-er.nl/index.php?title=YouLess)

The basic functionality will consist of simple executables for Windows and Linux that return the electricity-usage-data in a .xls spreadsheet with a chosen granularity.


## __Installation__

1. If you don't have Python installed get it from [here](https://www.python.org/downloads/) (3.6+) and install it
2. If you don't have pip installed get it from [here](https://bootstrap.pypa.io/get-pip.py) and install it with

    `python get-pip.py`
3. Dependencies will install with the first launch of the run-script

4. If the IP of your LS110 isn't __192.168.178.14__ then change it in "src/main.py" under the variable "URL"
   
## __Usage__

1. Windows: execute run.bat
   
   Linux:   execute run.sh
2. Enter your device's IP if it's not the default, else just press "Enter"
3. Enter your password for the device
4. Choose your desired data-set intervall (year, week, day, hour)
5. The program wil show you the average powedraw and the total power consumption plotted against the chosen time-intervall.
6. After closing both plots it will ask you, wether you want to save the data as a .xls into the script's directory as "_timestamp-begin_\_to\__timestamp-end_.xls".
