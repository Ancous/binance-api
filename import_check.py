import time
import datetime
from random import randint

from numpy import arange

# my_time_1 = datetime.date(2023, 6, 4)
# print(time.mktime(my_time_1.timetuple()) * 1000)
# my_time = datetime.date(2023, 6, 5)
# print(time.mktime(my_time.timetuple()) * 1000)
# print(time.mktime(my_time_1.timetuple()) * 1000 - time.mktime(my_time.timetuple()) * 1000)
# local_time = time.ctime(1661990400000 / 1000)
# print("Местное время:", local_time)
# local_time = time.ctime(1686844079999 / 1000)
# print("Местное время:", local_time)
# local_time = time.ctime(1683399064927 / 1000)
# print("Местное время:", local_time)
# local_time = time.ctime(1683399065085 / 1000)
# print("Местное время:", local_time)

# s = 86400
ms = 86400000
#
now = int(time.time()) * 1000
print(now)
tom = now - ms
print(time.ctime(1688468400000/1000))
# d = time.time() - s
print(time.ctime(1688554500000/1000))