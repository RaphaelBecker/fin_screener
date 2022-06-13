from datetime import datetime


def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")