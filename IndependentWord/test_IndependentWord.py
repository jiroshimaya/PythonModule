import unittest
from IndependentWord import IndependentWord as iw

#テストケース
class Case:
  Extract = [
    ("今日は来てくれてありがとう",["来る"]),
    ("こんにちは",[]),
    ("あらゆる現実が私の方に捻じ曲げられたのだ",["現実",'捻じる', '曲げる']),
    ("私のお墓の前で泣かないでください。そこに私はいません",['墓', '泣く'])
    ]

class TestIndependentWord(unittest.TestCase):
  def test_extract(self):
    IW = iw()
    for arg, result in Case.Extract:
      self.assertEqual(IW.extract(arg), result)

if __name__=="__main__":
  unittest.main()