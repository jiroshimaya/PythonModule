import unittest
from JapaneseDatetime import JapaneseDatetime as jd
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
#テストケース
class Case:
  Extract = [
    ("今日", dt.now()),
    ("明日",dt.now()+rd(days=+1)),
    ("明後日", dt.now()+rd(days=+2)),
    ("明々後日", dt.now()+rd(days=+3)),
    ("３日後", dt.now()+rd(days=+3)),
    ("昨日",dt.now()+rd(days=-1)),
    ("一昨日",dt.now()+rd(days=-2)),
    ("一昨々日",dt.now()+rd(days=-3)),
    ("４日前", dt.now()+rd(days=-4)),
    ("来月", dt.now()+rd(months=+1)),
    ("翌月", dt.now()+rd(months=+1))
    #("来月1日", dt.now()+rd(months=+1, day=1)),
    #("先月末", dt.now()+rd(day=1,days=-1)),
    #("３日後の５時", dt.now()+rd(days=+3, hour=5)),
    #("今週水曜", dt.now()+rd(weekday=WE(+1)))
  ]

class Test(unittest.TestCase):
  def test_getDatetime(self):
    for arg, result in Case.Extract:
      r = jd.getDatetime(arg) + rd(microsecond=0)
      result += rd(microsecond=0)
      self.assertEqual(r, result)

if __name__=="__main__":
  unittest.main()