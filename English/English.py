import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import json
from Romaji import Romaji
import re
#import jaconv

ENGLISH_DICT_PATH = os.path.join(os.path.dirname(__file__),"data","bep-eng.json")
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
    return text.replace(cls.OTHER_APOS, cls.APOS)

class English:
  english = JsonLoader.loadRelative(ENGLISH_DICT_PATH)
  transtable = str.maketrans(
    'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ',
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
  alphabet_pattern = re.compile("[a-zA-Z]+")
  
  @classmethod
  def containAlphabet(cls, text):
    if cls.alphabet_pattern.search(text):
      return True
    else:
      return False
  
  @staticmethod
  def load(path=None):
    if not path:
      path = PATH
    path = os.path.join(os.path.dirname(__file__), path)
    data = None
    with open(path, "r") as f:
      data = json.load(f)
    return data
  @classmethod
  def zenToHan(cls,text):
    return text.translate(cls.transtable)
  
  @staticmethod
  def romanToKana(text):
    return Romaji.toKana(text)
  
  @classmethod
  def wordToKana(cls, text):
    text2 = text.upper()
    text2 = Apostrophe.format(text2)
    return cls.english.get(text2,text)
  
  @classmethod
  def alphabetToKana(cls, text):
    text2 = text.upper()
    result = ""
    for t1,t2 in zip(text, text2):
      result += cls.english.get(t2,t1)
    return result
  
  @classmethod
  def toKana(cls, text):
    text = cls.zenToHan(text)
    text = cls.wordToKana(text)
    if not cls.containAlphabet(text):
      return text
    text = cls.romanToKana(text)
    if not cls.containAlphabet(text):
      return text
    text = cls.alphabetToKana(text)
    return text
    

if __name__=="__main__":
  testcase = [
    "Hello",
    "I'm"
    ]
  print(English.toKana("konnichiwan"))