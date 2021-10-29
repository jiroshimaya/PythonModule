import re
import editdistance as ed
import sys,os
sys.path.append(os.path.dirname(__file__))
from Morasep import Morasep
import json

K2V, K2C = None, None
K2V_PATH = os.path.join(os.path.dirname(__file__),"dict","k2v.json")
K2C_PATH = os.path.join(os.path.dirname(__file__), "dict", "k2c.json")
with open(K2C_PATH) as f:
  K2V = json.load(f)
with open(K2C_PATH) as f:
  K2C = json.load(f)


class KanaConv():

  @classmethod
  def toVowel(kana):
    vowel = []
    for c in kana:
      if c not in K2V: 
    return K2V.
  @classmethod
  def toConsonant(kana):
    pass


  def __init__(self):
    self.re_mora = self.__get_mora_unit_re()

  #モウラ単位に分割するための正規表現パターンを得る
  def __get_mora_unit_re(self):
    #各条件を正規表現で表す
    c1 = '[ウクスツヌフムユルグズヅブプヴ][ヮァィェォ]' #ウ段＋「ヮ/ァ/ィ/ェ/ォ」
    c2 = '[イキシシニヒミリギジヂビピ][ャュェョ]' #イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
    c3 = '[テデ][ャィュョ]' #「テ/デ」＋「ャ/ィ/ュ/ョ」
    c4 = '[ァ-ヴー]' #カタカナ１文字（長音含む）

    cond = '('+c1+'|'+c2+'|'+c3+'|'+c4+')'
    re_mora = re.compile(cond)
    return re_mora

  #カタカナ文字列をモウラ単位に分割したリストを返す
  def mora_wakachi(self, kana_text):
    return self.re_mora.findall(kana_text)

  def char2vowel(self, text):
    t = text[-1] #母音に変換するには最後の１文字を見れば良い
    if t in "アカサタナハマヤラワガザダバパァャヮ":
      return "ア"
    elif t in "イキシチニヒミリギジヂビピィ":
      return "イ"
    elif t in "ウクスツヌフムユルグズヅブプゥュヴ":
      return "ウ"
    elif t in "エケセテネヘメレゲゼデベペェ":
      return "エ"
    elif t in "オコソトノホモヨロヲゴゾドボポォョ":
      return "オ"
    elif t == "ン":
      return "ン"
    elif t == "ッ":
      return "ッ"
    else:
      print(text, "no match")
      return text

  #長音を母音に変換
  #入力はモウラの単位で分割されたカナのリスト
  def bar2vowel(self, kana_list):
    output = []
    output.append(kana_list[0])
    #最初に長音がくることは想定しないので、２番めの要素からループを始める
    for i,v in enumerate(kana_list[1:]):
      if v == "ー":
        kana = self.char2vowel(output[i])#長音が連続した場合に対応するために念の為、outputから直前の要素を取得する
      else:
        kana = v
      output.append(kana)
    return output

  #カナを母音に変換する
  def kana2vowel(self, kana_list):
    output = []
    for v in kana_list:
      kana = self.char2vowel(v)
      output.append(kana)
    return output

  #受け取ったカナ１単位を子音に変換して返す
  #入力はモウラ１単位に相当するカナ文字列（長さ１または２）
  def char2consonant(self, text):
    t = text[0] #子音に変換するには最初の１文字を見れば良い
    if t in "アイウエオヤユヨワヲ":
      return "a"
    elif t in "カキクケコ":
      return "k"
    elif t in "サシスセソ":
      return "s"
    elif t in "タチツテト":
      return "t"
    elif t in "ナニヌネノ":
      return "n"
    elif t in "ハヒフヘホ":
      return "h"
    elif t in "マミムメモ":
      return "m"
    elif t in "ラリルレロ":
      return "r"
    elif t in "ガギグゲゴ":
      return "g"
    elif t in "ザジズゼゾヂヅ":
      return "z"
    elif t in "ダデド":
      return "d"
    elif t in "バビブベボヴ":
      return "b"
    elif t in "パピプペポ":
      return "p"
    elif t == "ッ":
      return "q"
    elif t == "ン":
      return "N"
    else:
      print(text, "no match")
      return text
  #カナ文字列を子音にして返す
  def kana2consonant(self, kana_list):
    output = []
    for v in kana_list:
      kana = self.char2consonant(v)
      output.append(kana)
    return output

  #置換のみによる編集距離を求める
  def replace_ed(self, kana_list1, kana_list2):
    if len(kana_list1) != len(kana_list2): #kana_list1とkana_list2の文字列長が異なるとき警告を出す
      print("warning: length of kana_list1 is different from one of kana_list2")
    dist = 0
    for k1,k2 in zip(kana_list1, kana_list2):
      if k1 != k2:
        dist += 1
    return dist

  #text1, text2: 一意に発音できるカタカナ文字列
  #is_relative: False、Trueのときそれぞれ絶対、相対編集距離を求める
  #ed_type: "normal","replace"のときそれぞれ一般的な、置換のみによる編集距離を求める
  #kana_type: "kana","vowel","consonant"のときそれぞれ、カナ、母音、子音の編集距離を求める
  def calc_ed(self, text1, text2, is_relative=False, ed_type="normal", kana_type="kana"):
    #入力をモウラの単位に分割
    kana_list1 = self.mora_wakachi(text1)
    kana_list2 = self.mora_wakachi(text2)

    #長音を母音に変換
    kana_list1 = self.bar2vowel(kana_list1)
    kana_list2 = self.bar2vowel(kana_list2)

    #kana_typeに応じて何もしない、または母音や子音に変換
    if kana_type=="kana":
      pass
    elif kana_type == "vowel":
      kana_list1 = self.kana2vowel(kana_list1)
      kana_list2 = self.kana2vowel(kana_list2)
    elif kana_type == "consonant":
      kana_list1 = self.kana2consonant(kana_list1)
      kana_list2 = self.kana2consonant(kana_list2)
    else:
      print("warning: kana_type is invalid")

    #ed_typeに応じた編集距離を求める
    dist = 0
    if ed_type == "normal":
      dist = ed.eval(kana_list1, kana_list2)
    elif ed_type == "replace": 
      dist = self.replace_ed(kana_list1, kana_list2)
    else:
      print("warning: ed_type is invalid")

    #is_relativeがTrueならkana_list1の文字列長で規格化する
    if is_relative: 
      dist /= len(kana_list1)  
    return dist  

  #カナの編集距離を求める
  def kana_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "normal", "kana")

  #母音の編集距離を求める
  def vowel_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "normal", "vowel")

  #子音の編集距離を求める
  def consonant_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "normal", "consonant")    

  #カナの置換のみによる編集距離を求める
  def kana_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "replace", "kana")

  #母音の置換のみによる編集距離を求める
  def vowel_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "replace", "vowel")

  #子音の置換のみによる編集距離を求める
  def consonant_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, False, "replace", "consonant")    

  #カナの相対編集距離を求める
  def relative_kana_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "normal", "kana")

  #母音の相対編集距離を求める
  def relative_vowel_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "normal", "vowel")

  #子音の相対編集距離を求める
  def relative_consonant_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "normal", "consonant")    

  #カナの置換のみによる相対編集距離を求める
  def relative_kana_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "replace", "kana")

  #母音の置換のみによる相対編集距離を求める
  def relative_vowel_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "replace", "vowel")

  #子音の置換のみによる相対編集距離を求める
  def relative_consonant_replace_ed(self, text1,text2):
    return self.calc_ed(text1, text2, True, "replace", "consonant")    

if __name__=="__main__":
  edu = EditDistanceUtil()
  text1 = "コンニチワ"
  text2 = "ワコンタラ"

  print("normal edit distance")
  print(edu.kana_ed(text1,text2))
  print("")
  print(edu.kana2vowel(text1), edu.kana2vowel(text2))
  print(edu.vowel_ed(text1,text2))
  print("")
  print(edu.kana2consonant(text1), edu.kana2consonant(text2))
  print(edu.consonant_ed(text1,text2))

  print("")
  print("replace edit distance")
  print(edu.kana_replace_ed(text1,text2))
  print("")
  print(edu.kana2vowel(text1), edu.kana2vowel(text2))
  print(edu.vowel_replace_ed(text1,text2))
  print("")
  print(edu.kana2consonant(text1), edu.kana2consonant(text2))
  print(edu.consonant_replace_ed(text1,text2))

  print("")
  print("relative normal edit distance")
  print(edu.relative_kana_ed(text1,text2))
  print("")
  print(edu.kana2vowel(text1), edu.kana2vowel(text2))
  print(edu.relative_vowel_ed(text1,text2))
  print("")
  print(edu.kana2consonant(text1), edu.kana2consonant(text2))
  print(edu.relative_consonant_ed(text1,text2))

  print("")
  print("relative replace edit distance")
  print(edu.relative_kana_replace_ed(text1,text2))
  print("")
  print(edu.kana2vowel(text1), edu.kana2vowel(text2))
  print(edu.relative_vowel_replace_ed(text1,text2))
  print("")
  print(edu.kana2consonant(text1), edu.kana2consonant(text2))
  print(edu.relative_consonant_replace_ed(text1,text2))