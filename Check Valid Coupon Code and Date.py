from datetime import datetime as dt
def check_coupon(ec, cc, cd, ed):
    return ec and ec == cc and dt.strptime(cd,"%B %d, %Y") <= dt.strptime(ed,"%B %d, %Y") 

# https://www.codewars.com/kata/539de388a540db7fec000642
