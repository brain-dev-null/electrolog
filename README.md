# __Electro Log__

Electro Log is a python-based data-analysis-tool that communicates with a *You Less LS110* kWh-meter that logs the electrical power usage in a household and provides its data via an API specified [here](http://wiki.td-er.nl/index.php?title=YouLess)

The basic functionality will consist of a simple executable file for windows that returns the electricity-usage-data in a .csv-file that can be handled by other software.


## __Installation__

#### _Windows_

1. If you don't have Python installed get it from [here](https://www.python.org/downloads/) (3.6+) and install it
2. If you don't have pip installed get it from [here](https://bootstrap.pypa.io/get-pip.py) and install it with

    `python get-pip.py`
3. For the dependencies to install run the following command:

   `pip install pandas numpy requests`
4. Enter the IP-adress of your LS110 device in the config.txt and save it
   
## __Usage__

#### _Windows_

1. Start the run.bat script
2. Choose your desired data-set granulation (year, week, day, hour)
3. Enter your password for the device
4. The program will save the data as a .csv into ./data_out/_granulation_/_timestamp-begin_-_timestamp-end_.csv
