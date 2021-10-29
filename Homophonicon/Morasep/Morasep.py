import re

class Morasep:
  #各条件を正規表現で表す
  p1 = '[ウクスツヌフムユルグズヅブプヴ][ァィェォ]' #ウ段＋「ァ/ィ/ェ/ォ」
  p2 = '[イキシチニヒミリギジヂビピ][ャュェョ]' #イ段（「イ」を除く）＋「ャ/ュ/ェ/ョ」
  p3 = '[テデ][ィュ]' #「テ/デ」＋「ャ/ィ/ュ/ョ」
  p4 = '[ァ-ヴー]' #カタカナ１文字（長音含む）
  re_mora = re.compile('({}|{}|{}|{})'.format(p1,p2,p3,p4))

  @classmethod
  def split(cls,kana_text):
      return cls.re_mora.findall(kana_text)

if __name__=="__main__":
  pass