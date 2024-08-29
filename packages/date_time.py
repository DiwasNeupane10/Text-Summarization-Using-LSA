from datetime import datetime as dt
def get_date_time():
    return dt.now().strftime("%Y_%m_%d %H_%M_%S")
