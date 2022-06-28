import datetime
datetime.datetime(2020,1,1).timestamp()

import requests
def render_ur12(feed_code, mm_start, dd_start, yyyy_start, mm_end, dd_end, yyyy_end):
    dt_start = int(datetime.datetime(yyyy_start, mm_start, dd_start, 0, 0, 0).timestamp())
    dt_end = int(datetime.datetime (yyyy_end, mm_end, dd_end, 23, 59, 59).timestamp())

    base_url = "https://queryl.finance.yahoo.com/v7/finance/download/"
    render_url =  "()?period1=()&period2=()&interval+1d&envents=history&frequency=1d".format (feed_code,
                                                                                              str(dt_start),
                                                                                              str(dt_end))
    complete_url = base_url + render_url
    print (complete_url)
    return complete_url
