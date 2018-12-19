from datetime import datetime

def remove_trailing_zero(s):
    """Given an s such as 09, remove the trailing zero"""
    if s == "00":
        return s
    
    # splitting by zero always leaves an empty string in the zero position
    if s.split("0")[0] == "":
        return s.split("0")[1]
    return s

assert(remove_trailing_zero("07") == "7")
assert(remove_trailing_zero("10") == "10")
assert(remove_trailing_zero("20") == "20")
assert(remove_trailing_zero("01") == "1")


def make_datetime_object(date):
    date = date.split()
    date_component = date[0].split("-")
    time_component = date[1].split(":")

    return datetime(
        int(date_component[0]),
        int(remove_trailing_zero(date_component[1])), 
        int(remove_trailing_zero(date_component[2])),
        int(remove_trailing_zero(time_component[0])), 
        int(remove_trailing_zero(time_component[1])), 
        int(remove_trailing_zero(time_component[2]))
    )    

assert(make_datetime_object("2015-07-15 15:13:31") == datetime(2015, 7, 15, 15, 13, 31))
assert(make_datetime_object("2016-04-18 00:13:31") == datetime(2016, 4, 18, 0, 13, 31))
