#参考
#https://docs.python.org/ja/3/library/datetime.html
#https://qiita.com/dkugi/items/8c32cc481b365c277ec2
#https://python.civic-apps.com/add-month-relativedelta/
#https://zenn.dev/wtkn25/articles/python-relativedelta

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import SU,MO,TU,WE,TH,FR,SA
import re


class JapaneseDatetime:

  zengo = re.compile(r"(?:(\d+)年)?(?:(\d+)[ヵヶ]月)?(?:(\d+)週間?)?(?:(\d+)日)?(?:(\d+)時間)?(?:(\d+)分間?)?(?:(\d+)秒間?)?([前後])")
  word = {
    "今日": rd(days=0),
    "明日": rd(days=+1),
    "明後日": rd(days=+2),
    "明々後日": rd(days=+3),
    "弥明後日": rd(days=+4),
    "昨日": rd(days=-1),
    "一昨日": rd(days=-2),
    "一昨々日": rd(days=-3),
    "今週": rd(weeks=0),
    "来週": rd(weeks=+1),
    "翌週": rd(weeks=+1),
    "再来週": rd(weeks=+2),
    "先週": rd(weeks=-1),
    "先々週": rd(weeks=-2),
    "今月":rd(months=0),
    "来月":rd(months=+1),
    "翌月":rd(months=+1),
    "再来月":rd(months=+2),
    "先月":rd(months=-1),
    "先々月":rd(months=-2),
    "今年":rd(years=0),
    "翌年":rd(years=+1),
    "来年":rd(years=+1),
    "再来年":rd(years=+2),
    "去年":rd(years=-1),
    "昨年":rd(years=-1),
    "一昨年":rd(years=-2),
  }
  @classmethod
  def getDatetime(cls,text):
    now = dt.now()


    if text in cls.word:
      return now + cls.word[text]
    elif cls.zengo.fullmatch(text):
      y,m,w,d,H,M,S,drc = cls.zengo.match(text).groups()
      
      if drc == "前":
        sign = -1
      elif drc == "後":
        sign = +1
      
      if y is not None:
        now += rd(years=sign*int(y))
      if m is not None:
        now += rd(months=sign*int(m))
      if w is not None:
        now += rd(weeks=sign*int(w))
      if d is not None:
        now += rd(days=sign*int(d))
      if H is not None:
        now += rd(hours=sign*int(H))
      if M is not None:
        now += rd(minutes=sign*int(M))
      if S is not None:
        now += rd(seconds=sign*int(S))
      return now
    
      
    
    return None

if __name__=="__main__":
  print("program start at", dt.now())
  while True:
    print(">", end="")
    text = input()
    result = JapaneseDatetime.getDatetime(text)
    print(result)
  
