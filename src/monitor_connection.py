import requests as req
import pandas as pd
import numpy as np

class requestor():
    def data_row(self, unit, delta_seconds, values, index):
        if unit == 'kWh':
            total = float(values[index].replace(",", "."))
            avg = total / 0.024
        else:
            avg = float(values[index].replace(",","."))
            total = (delta_seconds * avg) / 3600000
        return {"AvgPower(in W)":avg,"TotalConsumption(in kWh)":total}

    def timestamp_row(self, begin_timestamp, delta_seconds, index):
        return pd.Timestamp(begin_timestamp + np.timedelta64(delta_seconds * index, 's'))

    def __init__(self, URL:str,PW:str):
        self.URL = URL
        self.PW = PW
        self.intervall_dict = {}
        self.session = req.session()
        self.session.get(URL + "/L", params={"w":PW})
        self.timeblock_info =   {
                                "block_range":
                                    {
                                    "year":range(1,13),
                                    "week":range(1,7),
                                    "day" :range(1,4),
                                    "hour":range(1,3)
                                    },
                                "block_param":
                                    {
                                    "year":"m",
                                    "week":"d",
                                    "day" :"w",
                                    "hour":"h"
                                    }
                                }

    def getData(self, timeblock):
        data = []
        timestamps = []
        block_range = self.timeblock_info["block_range"][timeblock]
        block_param = self.timeblock_info["block_param"][timeblock]

        for block in block_range:
            api_json_response   = self.session.get(self.URL + "/V", params={block_param:block, "f":"j"}).json()
            values              = api_json_response["val"]
            unit                = api_json_response["un"]
            begin_timestamp     = np.datetime64( api_json_response["tm"])
            delta_seconds       = int(api_json_response["dt"])
            for index in range(0, len(values)-1):
                timestamps.append(self.timestamp_row(begin_timestamp, delta_seconds, index))
                data.append(self.data_row(unit, delta_seconds, values, index))
        data_frame = pd.DataFrame(data=data, index=timestamps)
        data_frame.sort_index(inplace=True)
        return data_frame