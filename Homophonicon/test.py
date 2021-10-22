import unittest
Cases = [
  ["ヒトカゲ","ヒトカゲ"],
  ]

class Test(unittest.TestCase):
  def test(self):
    for arg, result in Cases:
      self.assertEqual(Homophonicon.execute(arg), result)

if __name__=="__main__":
  unittest.main()