import os
import json

ROMAJI_DICT_PATH = os.path.join(os.path.dirname(__file__),"data","romaji_dict.json")

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

class Romaji:
  tree = JsonLoader.load(ROMAJI_DICT_PATH)    
  max_unit_len = max([len(k) for k in tree])
  
  @classmethod
  def isUnit(cls, tokens, s=0):
    for i in range(1,cls.max_unit_len):
      if tokens[s:s+i] in cls.tree:
        return True
    return False

  @classmethod
  def isSokuon(cls, tokens, s=0):
    if s+1 >= len(tokens):
      return False
    if tokens[s] != tokens[s+1]:
      return False
    if not tokens[s].isalpha():
      return False
    return True
    
  @classmethod
  def isHatsuon(cls, tokens, s=0):
    if s >= len(tokens):
      return False
    if tokens[s] not in ["n","m"]:
      return False
    return True

  @classmethod
  def getUnit(cls, tokens, s=0):
    for i in range(1,cls.max_unit_len):
      if tokens[s:s+i] in cls.tree:
        return cls.tree[tokens[s:s+i]], s+i
    return "",s

  @classmethod
  def getSokuon(cls, tokens, s=0):
    return "ッ", s+1
  
  @classmethod
  def getHatsuon(cls, tokens, s=0):
    return "ン", s+1
  
  @classmethod
  def getKana(cls, tokens, s=0):
    if s >= len(tokens) or s < 0:
      return ""
    kana = ""
    idx = s
    if cls.isUnit(tokens, idx):
      kana, idx = cls.getUnit(tokens, idx)
    elif cls.isHatsuon(tokens, idx):
      kana, idx = cls.getHatsuon(tokens, idx)
    elif cls.isSokuon(tokens, idx):
      kana, idx = cls.getSokuon(tokens, idx)
    else:
      kana, idx = tokens[idx], idx+1
    if idx >= len(tokens):
      return kana
    else:
      return kana + cls.getKana(tokens, idx)     
    
  @classmethod
  def toKana(cls, text): 
    text = text.lower()
    return cls.getKana(text,0)

if __name__=="__main__":
  testcase = [
    "Hello",
    "I'm",
    "konnichiwa",
    "砂糖",
    "hecchara",
    "ampamman"
    ]
  for t in testcase:
    print(t,Romaji.toKana(t))
