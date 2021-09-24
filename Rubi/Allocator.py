class Allocator:
  @staticmethod
  def getAllocatedLength(num1,num2):
    #長い方と短い方をindexで管理する
    num = [num1,num2]
    if num1 > num2:
      longer, shorter = 0,1
    else:
      longer, shorter = 1,0
    #商と余り
    unit = num[longer]//num[shorter]
    mod = num[longer]%num[shorter]
  
    length = []
    for i in range(num[shorter]):
      l = [0,0]
      l[shorter] = 1
      l[longer] = unit
      #余りより小さければ１を足す
      if i < mod: l[longer] += 1
      length.append(l)
    return length
  
  @classmethod
  def execute(cls,text1,text2):
    #getAllocatedLengthに0が入るとまずいので例外処理
    if not all([text1,text2]):
      return [[text1,text2]]
  
    length = cls.getAllocatedLength(len(text1),len(text2))
    index1,index2=0,0
    tokens = []
    for len1,len2 in length:
      token = [text1[index1:index1+len1], text2[index2:index2+len2]]
      tokens.append(token)
      index1 += len1
      index2 += len2
    return tokens
  
if __name__=="__main__":
  import unittest
  class TestAllocator(unittest.TestCase):
    def test_blancedAllocator(self):
      self.assertEqual(Allocator.execute("abcdef","123"),[["ab","1"],["cd","2"],["ef","3"]])
      self.assertEqual(Allocator.execute("abcdefg","123"),[["abc","1"],["de","2"],["fg","3"]])
      self.assertEqual(Allocator.execute("123","abcdef"),[["1","ab"],["2","cd"],["3","ef"]])
      self.assertEqual(Allocator.execute("123","abcdefg"),[["1","abc"],["2","de"],["3","fg"]])
  unittest.main()  