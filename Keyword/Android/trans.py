#coding:utf-8
import time
import datetime

date_table = {"TR": {"Ocak": 1,
                     "Şubat": 2,
                     "Mart": 3,
                     "Nisan": 4,
                     "Mayıs": 5,
                     "Haziran": 6,
                     "Temmuz": 7,
                     "Ağustos": 8,
                     "Eylül": 9,
                     "Ekim": 10,
                     "Kasım": 11,
                     "Aralık": 12},
              "RU": {"января": 1,
                     "Февраля": 2,
                     "февраля": 2,
                     "Март": 3,
                     "марта": 3,
                     "апреля": 4,
                     "май": 5,
                     "мая": 5,
                     "июня": 6,
                     "июля": 7,
                     "августа": 8,
                     "сентября": 9,
                     "октября": 10,
                     "ноября": 11,
                     "декабря": 12},
              "EN": {"January": 1,
                     "February": 2,
                     "March": 3,
                     "April": 4,
                     "May": 5,
                     "June": 6,
                     "July": 7,
                     "August": 8,
                     "September": 9,
                     "October": 10,
                     "November": 11,
                     "December": 12}
              }



def trans(language, s):
    if language == "CN":
        t = time.strptime(s, "%Y年%m月%d日")

    elif language == "EN":
        t = time.strptime(s, "%B %d, %Y")

    elif language == "RU":
        a = s.split()
        t = datetime.date(day=int(a[0]), month=date_table["RU"][a[1]], year=int(a[2])).timetuple()

    elif language == "TR":
        a = s.split()
        t = datetime.date(day=int(a[0]), month=date_table["TR"][a[1]], year=int(a[2])).timetuple()


    timestamp = time.mktime(t)
    return timestamp
    
def timestamp2date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
