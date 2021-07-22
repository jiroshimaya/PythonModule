import MeCab
import regex

class IndependentWord:
  def __init__(self, dictpath=None):
    if dictpath:
      self.m = MeCab.Tagger("-d "+dictpath)
    else:
      self.m = MeCab.Tagger()   
    self.kanaalpha = regex.compile(r'[\p{Script=Hiragana}\p{Script=Katakana}ーA-Za-z]+')
    self.number = regex.compile("[0-9０-９]+")
  
  class Constant:
    BASIC = "basic_form" #原型
    SURFACE = "surface_form" #表層型
    POS = "pos" #品詞
    POS_DETAIL_1 = "pos_detail_1" #品詞詳細1
    POS_DETAIL_2 = "pos_detail_2" #品詞詳細2
    POS_DETAIL_3 = "pos_detail_3" #品詞詳細3
    PRONUNCIATION = "pronunciation" #発音
    READING = "reading" #読み
    CONJUGATED_TYPE = "conjugated_type" #活用
    CONJUGATED_FORM = "conjugated_form" #活用形
    
  #mecabの出力行をobjectに変換
  #mecabの出力フォーマットに応じて適宜修正する
  def mecabLineToDict(self, line):
    surface, tmp = line.split("\t")
    others = tmp.split(",")
    
    Const = self.Constant
    
    return {
      Const.SURFACE: surface,
      Const.POS: others[0],
      Const.POS_DETAIL_1: others[1],
      Const.POS_DETAIL_2: others[2],
      Const.POS_DETAIL_3: others[3],
      Const.CONJUGATED_TYPE: others[4],
      Const.CONJUGATED_FORM: others[5],
      Const.BASIC: others[6],
      Const.READING: others[7],
      Const.PRONUNCIATION: others[8]
      }
  #自立語かどうかの判定
  def isIndependentWord(self, token):
    pos = token[self.Constant.POS]
    pos_detail_1 = token[self.Constant.POS_DETAIL_1]
    if pos == "名詞" and pos_detail_1 in ['一般','固有名詞','サ変接続','形容動詞語幹']: #用途によっては「副詞可能」を足しても良いかもしれません
      return True
    elif pos == '形容詞' and pos_detail_1 == '自立':
      return True
    elif pos == "副詞" and pos_detail_1 == "一般":
      return True
    elif pos == "動詞" and pos_detail_1 == "自立":
      return True
    else:
      return False
  #カナやアルファベット１文字や数字出ないかの判定
  def isReliableWord(self, token):
    surface = token[self.Constant.SURFACE]
    if self.number.fullmatch(surface):
      return False
    elif self.kanaalpha.fullmatch(surface):
      return False
    else:
      return True
    
  #自立語の原型を抽出
  def extract(self,text):
    lines = self.m.parse(text).splitlines()[:-1]
    tokens = [self.mecabLineToDict(line) for line in lines]
    
    independent_words = []
    for token in tokens:
      if self.isIndependentWord(token) and self.isReliableWord(token):
        surface = token[self.Constant.SURFACE]
        basic = token[self.Constant.BASIC]
        if basic == "*":
          independent_words.append(surface)
        else:
          independent_words.append(basic)
    return independent_words    

if __name__ == "__main__":
  idptwd = IndependentWord()
  result = idptwd.extract("今日は来てくれてありがとう")
  print(result)
