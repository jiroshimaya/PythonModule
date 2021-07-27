import os
import json
import re

PATH = os.path.join(".","data","kanjiyomi.json")

class Kanji:
  def __init__(self, path=None):
    self.kanji = self.load(path)
    self.first_bad_kana = re.compile("^[ャュョァィゥェォヮッンー][ーンッ]*")
    self.last_bad_kana = re.compile("[ャュョァィゥェォヮッンー]*$")
  
  def load(self, path=None):
    if not path:
      path = PATH
    path = os.path.join(os.path.dirname(__file__), path)
    data = None
    with open(path, "r") as f:
      data = json.load(f)
    return data
  
  #不正なひらがなで始まっていたらその文字列を、そうでなければ空文字を返す
  def getFirstBadKana(self, text):
    result = self.first_bad_kana.search(text)
    if not result: return ""
    else: return result.group()
  def getLastBadKana(self, text):
    result = self.last_bad_kana.search(text)
    if not result: return ""
    else: return result.group()
    
  #小文字や促音などで始まっている発音があれば直前の要素と調整して修正する
  def formatOutput(self, output):
    output = output[:]
    result = [output[0]]
    for s,p in output[1:]:
      badFisrtKana = self.getFirstBadKana(p)
      if not badFisrtKana:
        result.append([s,p])
        continue
      
      last_p = result[-1][1]
      lastBadKana = self.getLastBadKana(last_p)
      thisRest = p[len(badFirstKana):]
      lastRest = last_p[:-1*(len(lastBadKana))]
      
      if len(lastRest) <= len(thisRest):
        result[-1][1] += badFirstKana
        result.append([s, thisRest])
      else:
        result[-1][1] = last_p[:-1*(len(lastBadKana)+1)]
        result.append([s, last_p[(len(lastBadKana)+1):]+p])
    return result
  
  def allocate(self, surface, pronunciation):
    kanji_dict = self.kanji
    rest_text = pronunciation
    skipped_char = ""
    output = []
    for i,char in enumerate(surface):
      yomi_candidates = kanji_dict.get(char, [])
      start, yomi = -1, ""
      for y in yomi_candidates:
        #print(y)
        if y in rest_text:
          start = rest_text.index(y)
          yomi = y
          break
        
      if start < 0:
        skipped_char += char
        continue
      
      if start == 0:
        output.append([char, yomi]);
        rest_text = rest_text[len(yomi):]
      elif skipped_char:
        output.append(
          [skipped_char, rest_text[:start]]
          )
        skipped_char = ""
        rest_text = rest_text[start:]
        output.append(
          [char, yomi]
          )
        rest_text = rest_text[len(yomi):]
      elif output:
        output[-1][1]+= rest_text[:start]
        rest_text = rest_text[start:]
        output.append([char, yomi]);
        rest_text = rest_text[len(yomi):]
      else:
        output.append([
          char, rest_text[:start+len(yomi)]
          ]);
        rest_text = rest_text[start+len(yomi):]
    
    if skipped_char and rest_text:
      output.append([
        skipped_char, rest_text
        ])
    elif skipped_char and output:
      output[-1][0] += skipped_char
    elif rest_text and output:
      output[-1][1] += rest_text
    elif not output and (skipped_char or rest_text):
      output.append([
        skipped_char, rest_text
        ])
    else:
      pass
    
    output = self.formatOutput(output)
    
            
    return output  
  
if __name__ == "__main__":
  kanji = Kanji()
  #print(kanji.getFirstBadKana("ッポロ"))
  print(kanji.allocate("野幌","ノッポロ"))
  print(kanji.allocate("閑寂","カンシャク"))
  print(kanji.allocate("包丁","ホーチョー"))
  print(kanji.allocate("包丁","ホウチョウ"))
  print(kanji.allocate("麝香鼠","ジャコウネズミ"))