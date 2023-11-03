from datetime import datetime, time, timedelta
# import datetime

def mrng_access_allowed():
    current_datetime = datetime.now()
    start_time = time(hour = 9, minute = 0)
    end_time = time(hour = 13, minute = 0)
    return start_time <= current_datetime.time() < end_time

def evng_access_allowed():
    current_datetime = datetime.now()
    start_time = time(hour = 13, minute = 0)
    end_time = time(hour = 18, minute = 0)
    return start_time <= current_datetime.time() <= end_time