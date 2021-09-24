import os,sys
import json
import jaconv

ENGLISH_DICT_PATH = os.path.join(os.path.dirname(__file__),"data","bep-eng.json")
ROMAN_TREE_PATH = os.path.join(os.path.dirname(__file__),"data","tree_roma2kana.json")
class JsonLoader:
  @staticmethod
  def load(path):
    data = None
    with open(path) as f:
      data = json.load(f)
    return data
  @classmethod
  def loadRelative(cls,path):
    path = os.path.join(os.path.dirname(__file__),path)
    return cls.load(path)
 
  
class Apostrophe:
  STRING = "APOSTROPHE"
  APOS = "'"
  OTHER_APOS = "’" 
  @classmethod
  def toString(cls,text):
    return text.replace(cls.OTHER_APOS, cls.APOS).replace(cls.APOS,cls.STRING)
  @classmethod
  def toSign(cls,text):
    return text.replace(cls.STRING, cls.APOS)
  @classmethod
  def removeString(cls, text):
    return text.reaplce(cls.STRING, "")
  @classmethod
  def include(cls, text):
    return cls.STRING in text
  @classmethod
  def format(cls, text):
    return text.replace(OTHER_APOS, APOS)

class English:
  english = JsonLoader.loadRelative(ENGLISH_DICT_PATH)
  
  @staticmethod
  def load(path=None):
    if not path:
      path = PATH
    path = os.path.join(os.path.dirname(__file__), path)
    data = None
    with open(path, "r") as f:
      data = json.load(f)
    return data
  @staticmethod
  def zenToHan(text):
    return mojimoji.zen_to_han(text)
  
  @staticmethod
  def romanToKana(text):
    pass 

if __name__=="__main__":
  testcase = [
    "Hello",
    "I'm"
    ]
  print(RomanToKana.execute("konnichiwan"))