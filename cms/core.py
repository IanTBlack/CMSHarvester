from datetime import datetime

API_URL: str = 'https://hmsc-cms.dri.oregonstate.edu/api/'
REQ_DT_FMT: str = '%Y-%m-%d %H:%M:%S'


def format_datetime(dt: datetime):
    dt_str = dt.strftime(REQ_DT_FMT)
    return dt_str