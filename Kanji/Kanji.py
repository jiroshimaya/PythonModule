import os
import json

PATH = os.path.join(".","data","kanjiyomi.json")

class Kanji:
  
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
            
    return output  
  
if __name__ == "__main__":
  kanji = Kanji()
  #print(kanji.getFirstBadKana("ッポロ"))
  print(kanji.allocate("野幌","ノッポロ"))
  print(kanji.allocate("閑寂","カンシャク"))
  print(kanji.allocate("包丁","ホーチョー"))
  print(kanji.allocate("包丁","ホウチョウ"))
  print(kanji.allocate("麝香鼠","ジャコウネズミ"))