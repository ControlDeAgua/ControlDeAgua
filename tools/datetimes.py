"""
Check datetimes.

All the datetimes, tested here have this scheme provided
by `datetime.datetime.today.strftime("%B %d, %Y %H:%M:%S")`:

    MONTH_NAME DAY, YEAR HOURS:MINUTES:SECONDS

Considering this can help us to analyze 2 date strings.
"""

__all__ = ("parse_dates", "compare_dates")

from datetime import datetime
from typing import Optional, Dict, Any

MONTH_MAP = {"January": 1,
             "February": 2,
             "March": 3,
             "April": 4,
             "May": 5,
             "June": 6,
             "July": 7,
             "August": 8,
             "September": 9,
             "October": 10,
             "November": 11,
             "December": 12}

def parse_dates(d1: str, d2: str) -> Dict[str, Any]:
    "translate the datetime strings"
    d1, d2 = d1.replace(",", "").split(), d2.replace(",", "").split()
    d1_dict, d2_dict = {}, {}
    for i, ii in [(d1_dict, d1), (d2_dict, d2)]:
        i["month"] = ii[0]
        i["day"] = ii[1]
        i["year"] = ii[2]
        i["time"] = ii[3].split(":")
        # at this point, each `i` (`d1_dict` and `d2_dict`) looks like this:
        #
        #    {"month": "MONTH_NAME",
        #     "day": "DAY",
        #     "year": "YEAR",
        #     "time": ["HOURS", "MINUTES", "SECONDS"]}
    return d1_dict, d2_dict

def compare_dates(date1: str, date2: str) -> Optional[bool]:
    "compare 2 strings with datetimes"
    d1, d2 = parse_dates(date1, date2)
    if (int(d1["year"]) > int(d2["year"]) or
        d1["year"] == d2["year"] and MONTH_MAP[d1["month"]] > MONTH_MAP[d2["month"]] or
        d1["year"] == d2["year"] and d1["month"] == d2["month"] and d1["day"] > d2["day"] or
        d1["year"] == d2["year"] and d1["month"] == d2["month"] and d1["day"] == d2["day"] and d1["time"] > d2["time"]):
        # if `d1` represents an older date than `d2`, raise a ValueError
        raise ValueError(f"Date '{date1}' is larger than '{date2}'")
    return True
