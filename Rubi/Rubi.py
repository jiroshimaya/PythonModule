import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from MeCabWrapper import MeCabWrapper
from Kanji import Kanji
from Allocator import Allocator
from BadKana import BadKana
import jaconv
import re
import itertools

class Rubi:
  def __init__(self, dictpath=None):
    if dictpath:
      self.m = MeCabWrapper(dictpath)
    else:
      self.m = MeCabWrapper()
    Const = self.Constant
    pattern = r"(?P<{}>[ァ-ヴー]+)|(?P<{}>[ぁ-ゔー]+)|(?P<{}>[^ぁ-ゔァ-ヴー]+)".format(Const.KATA, Const.HIRA, Const.OTHER) #カタカナ、ひらがな、カナ以外にグループマッチ
    self.pattern = re.compile(pattern)
    self.kanji = Kanji()
  
  class Constant:
    SURFACE = "surface"
    POS = "pos"
    PRONUNCIATION = "pronunciation"
    IN_SURFACE_POS = "in_surface_pos"
    TYPE = "type"
    SIGN = "sign"
    HIRA = "hira"
    KATA = "kata"
    ALPHA = "alpha"
    OTHER = "other"
    SIGN_JP = "記号"
  
  @staticmethod
  def flatten(array):
    return list(itertools.chain.from_iterable(array))
  def getYomi(self, text):
    tokens = self.m.parse(text)
    Const = self.m.Constant
    ret = []
    for token in tokens:
      surface = token[Const.SURFACE]
      surface_kata = jaconv.hira2kata(surface)
      reading = token[Const.READING]
      pos = token[Const.POS]
      if pos == "*":
        reading = ""
      elif reading == "*":
        reading = surface_kata
      ret.append((surface_kata, reading))
    return ret
  
  def tokenize(self, text):
    tokens = self.m.parse(text)
    Const = self.m.Constant
    result = []
    for token in tokens:
      surface = token[Const.SURFACE]
      surface_kata = jaconv.hira2kata(surface)
      reading = token[Const.READING]
      pos = token[Const.POS]
      if pos == "*":
        reading = ""
      elif pos == Const.SIGN:
        reading = ""
      elif reading == "*":
        reading = surface_kata
      token[Const.READING] = reading
      result.append(token)
    return result
  
  def kanaTokenize(self, text):
    Const = self.Constant
    #例外処理。万が一から文字であればカラのリストを返す
    if not text: return []
    
    tokens = [m.groupdict() for m in self.pattern.finditer(text)]
    result = []
    for token in tokens:
      for k,v in token.items():
        if v:
          obj = {Const.SURFACE: v, Const.TYPE: k}
          result.append(obj)
          break
    return result
    
  def kanaAllocate(self, tokens, pronunciation):  
    if not tokens: return []
    
    Const = self.Constant
    kana_index, other_index = 0,1
    if tokens[0][Const.TYPE] == Const.OTHER:
      kana_index, other_index = 1,0
    
    output = []
    rest_text = pronunciation
    
    for i,token in enumerate(tokens):
      type_ = token[Const.TYPE]
      surface = token[Const.SURFACE]
      
      if type_ != Const.HIRA and type_ != Const.KATA: continue
      
      katakana = surface
      if type_ == Const.HIRA: katakana = jaconv.hira2kata(surface)
      
      start = rest_text.index(katakana) if katakana in rest_text else -1
      
      if start > 0:
        other = tokens[i-1]
        output.append(
          {
            Const.SURFACE: other[Const.SURFACE],
            Const.PRONUNCIATION: rest_text[:start],
            Const.TYPE: other[Const.TYPE]
            })
        rest_text = rest_text[start:]
      
      output.append(
        {
          Const.SURFACE: surface,
          Const.PRONUNCIATION: rest_text[:len(katakana)],
          Const.TYPE: type_
          })
      rest_text = rest_text[len(katakana):]
      
    if rest_text:
      last = tokens[-1]
      output.append({
        Const.SURFACE: last[Const.SURFACE],
        Const.PRONUNCIATION: rest_text,
        Const.TYPE: type_
        })
    return output  

  def execute(self, text):
    Const = self.m.Constant
    tokens = self.tokenize(text)
    
    kana_correspondance = []
    for token in tokens:
      surface = token[Const.SURFACE]
      pronunciation = token[Const.PRONUNCIATION]
      pos = token[Const.POS]
      
      separated = self.kanaTokenize(surface)
      correspondance = self.kanaAllocate(separated, pronunciation)
      
      if pos == Const.SIGN:
        for i in range(len(correspondance)):
          correspondance[i][self.Constant.TYPE] = self.Constant.SIGN
      kana_correspondance.extend(correspondance)
    
    char_correspondance = []
    
    for token in kana_correspondance:
      surface = token[self.Constant.SURFACE]
      type_ = token[self.Constant.TYPE]
      pronunciation = token[self.Constant.PRONUNCIATION]
      
      
      if type_ == self.Constant.OTHER:
        correspondance = self.kanji.allocate(surface, pronunciation)
        correspondance = [Allocator.execute(*c) for c in correspondance]
        correspondance = self.flatten(correspondance)
      else:
        correspondance = Allocator.execute(surface, pronunciation)
      
      for s,p in correspondance:
        for j,p2 in enumerate(p):
          obj = {
            self.Constant.SURFACE: s,
            self.Constant.PRONUNCIATION: p2,
            self.Constant.TYPE: type_,
            self.Constant.IN_SURFACE_POS: j
            }
          char_correspondance.append(obj)
    return char_correspondance;

    

if __name__ == "__main__":
  rubi = Rubi()
  testcase = [
    "今日は「来てくれて」慮る。",
    "hello, nice to meet you"
    ]
  for c in testcase:
    print(rubi.execute(c))
