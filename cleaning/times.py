import datetime
from datetime import date, datetime, timedelta

def five_oclock():
    mid = datetime.min.time() # midnight
    delta = timedelta(hours=5) # plus 5 hours
    five = (datetime.combine(date(1,1,1),mid)+delta).time()
    return five

