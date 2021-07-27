from MeCabWrapper import MeCabWrapper
import jaconv
import re

class Rubi:
  def __init__(self, dictpath=None):
    if dictpath:
      self.m = MeCabWrapper(dictpath)
    else:
      self.m = MeCabWrapper()
    Const = self.Constant
    pattern = r"(?P<{}>[ァ-ヴー]+)|(?P<{}>[ぁ-ゔー]+)|(?P<{}>[^ぁ-ゔァ-ヴー]+)".format(Const.KATA, Const.HIRA, Const.OTHER) #カタカナ、ひらがな、カナ以外にグループマッチ
    self.pattern = re.compile(pattern)
  
  class Constant:
    SURFACE = "surface"
    POS = "pos"
    PRONUNCIATION = "pronunciation"
    IN_SURFACE_POS = "IN_SURFACE_POS"
    TYPE = "type"
    SIGN = "sign"
    HIRA = "hira"
    KATA = "kata"
    ALPHA = "alpha"
    OTHER = "other"
  
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
    
    
    

if __name__ == "__main__":
  rubi = Rubi()
  y=rubi.kanaTokenize("今日は来てくれて慮る")
  y = rubi.kanaAllocate(y,"キョウハキテクレテオモンパカル")
    
  
  print(y)    
