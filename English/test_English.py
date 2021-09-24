import unittest
from English import English

#テストケース
class Case:
  toKana = [
    ("Hello","ハロー"),
    ("zyakojika","ジャコジカ"),
    ("I'm","アイム"),
    ("perfect","パーフェクトゥ"),
    ("HECCHARA","ヘッチャラ"),
    ("砂糖taiyo","砂糖タイヨ")
    ]

class TestEnglish(unittest.TestCase):
  def test_toKana(self):
    for arg, result in Case.toKana:
      self.assertEqual(English.toKana(arg), result)

if __name__=="__main__":
  unittest.main()