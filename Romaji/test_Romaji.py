import unittest
from Romaji import Romaji

#テストケース
class Case:
  toKana = [
    ("Hello","ヘッォ"),
    ("zyakojika","ジャコジカ"),
    ("I'm","イ'ン"),
    ("HECCHARA","ヘッチャラ"),
    ("砂糖taiyo","砂糖タイヨ")
    ]

class TestRomaji(unittest.TestCase):
  def test_toKana(self):
    for arg, result in Case.toKana:
      self.assertEqual(Romaji.toKana(arg), result)

if __name__=="__main__":
  unittest.main()