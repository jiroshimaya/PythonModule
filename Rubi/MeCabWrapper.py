import MeCab

class MeCabWrapper:
  def __init__(self, dictpath=None):
    if dictpath:
      self.m = MeCab.Tagger("-d "+dictpath)
    else:
      self.m = MeCab.Tagger()
      
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
  def lineToDict(self, line):
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
  def parse(self, text):
    lines = self.m.parse(text).splitlines()[:-1]
    tokens = [self.lineToDict(line) for line in lines]
    return tokens
  
if __name__ == "__main__":
  m = MeCabWrapper()
  tokens = m.parse("今日は来てくれてありがとう")
  for token in tokens:
    print(token)
    
