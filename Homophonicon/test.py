import unittest
Cases = [
  ["ヒトカゲ","ヒトカゲ"],
  ]

class Test(unittest.TestCase):
  def test_practice0(self):
    for arg, result in Cases:
      self.assertEqual(Homophonicon.execute(arg), result)

if __name__=="__main__":
  unittest.main()