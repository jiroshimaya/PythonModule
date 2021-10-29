import unittest
from Morasep import Morasep
Cases = [
  ["シンシュンシャンソンショー",['シ', 'ン', 'シュ', 'ン', 'シャ', 'ン', 'ソ', 'ン', 'ショ', 'ー']],
  ["トーキョートッキョキョカキョク", ['ト', 'ー', 'キョ', 'ー', 'ト', 'ッ', 'キョ', 'キョ', 'カ', 'キョ', 'ク']],
  ["アウトバーン",['ア', 'ウ', 'ト', 'バ', 'ー', 'ン']],
  ["ガッキュウホウカイ",['ガ', 'ッ', 'キュ', 'ウ', 'ホ', 'ウ', 'カ', 'イ']]
]
class Test(unittest.TestCase):
  def test_split(self):
    for arg, result in Cases:
      self.assertEqual(Morasep.split(arg), result)

if __name__=="__main__":
  unittest.main()