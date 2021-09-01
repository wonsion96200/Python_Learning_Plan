import re
from datetime import datetime
import time

t1 = "02:07:25.965668"
t2 = "02:07:25.965667"
str = "2021-07-23 02:07:25.982096849   |   |   |   |   |   |   |   |==>|     |               0xae9ea87530229066              (XNAP)  HandoverRequestAcknowledge:"
null = ""

if null in str:
    print("Yes")
else:
    print("No")


# if t1 > t2:
#     print("1")
# else:
#     print("2")

time1 = datetime.strptime("01:07:25.108524", "%H:%M:%S.%f")
time2 = datetime.strptime("01:07:25.108464", "%H:%M:%S.%f")

print(time2 - time1)
print((time2 - time1).microseconds)
print((time2 - time1).total_seconds()*1000)
print(abs((time2 - time1).total_seconds())*1000)
