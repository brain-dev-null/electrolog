from requests import Response, Session
from pandas import concat, DataFrame, Series, to_datetime
from datetime import timedelta
import logging

LOGGER = logging.getLogger(__name__)


def download_past_hour(session: Session, base_url: str) -> DataFrame:
    url = f"{base_url}/V"

    responses = [
        session.get(url, params={"h": str(page), "f": "j"})
        for page in range(1, 3)
    ]

    page_dataframes = [
        response_to_dataframe(response, "Average powerdraw (W)")
        for response in responses
    ]

    return concat(page_dataframes, sort=True).sort_index()


def download_past_day(session: Session, base_url: str) -> DataFrame:
    url = f"{base_url}/V"

    responses = [
        session.get(url, params={"w": str(page), "f": "j"})
        for page in range(1, 4)
    ]

    page_dataframes = [
        response_to_dataframe(response, "Average powerdraw (W)")
        for response in responses
    ]

    return concat(page_dataframes, sort=True).sort_index()


def download_past_week(session: Session, base_url: str) -> DataFrame:
    url = f"{base_url}/V"

    responses = [
        session.get(url, params={"d": str(page), "f": "j"})
        for page in range(1, 7)
    ]

    page_dataframes = [
        response_to_dataframe(response, "Average powerdraw (W)")
        for response in responses
    ]

    return concat(page_dataframes, sort=True).sort_index()


def download_past_year(session: Session, base_url: str) -> DataFrame:
    url = f"{base_url}/V"

    responses = [
        session.get(url, params={"m": str(page), "f": "j"})
        for page in range(1, 13)
    ]

    page_dataframes = [
        response_to_dataframe(response, "Total power consumed (kWh)", True)
        for response in responses
    ]

    return concat(page_dataframes, sort=True).sort_index()


def response_to_dataframe(
    response: Response, value_label: str, date_only=False
) -> DataFrame:
    data = response.json()
    initial_time = to_datetime(data["tm"])
    time_offset = timedelta(seconds=data["dt"])

    values = Series(data["val"]).dropna()
    times = Series(
        [initial_time + i * time_offset for i in range(len(values))]
    )

    if date_only:
        times = times.dt.date

    if data["un"] == "kWh":
        values = values.str.replace(",", ".").astype(float)
    else:
        values = values.astype(int)

    return DataFrame({"time": times, value_label: values}).set_index("time")
