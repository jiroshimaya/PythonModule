import re
class BadKana:
  first_bad_kana = re.compile("^[ャュョァィゥェォヮッンー][ーンッ]*")
  last_bad_kana = re.compile("[ャュョァィゥェォヮッンー]*$")
  
  #不正なひらがなで始まっていたらその文字列を、そうでなければ空文字を返す
  @classmethod
  def first(cls, text):
    result = cls.first_bad_kana.search(text)
    if not result: return ""
    else: return result.group()
  @classmethod
  def last(cls, text):
    result = cls.last_bad_kana.search(text)
    if not result: return ""
    else: return result.group()
    
  #小文字や促音などで始まっている発音があれば直前の要素と調整して修正する
  @classmethod
  def formatList(cls, output):
    output = output[:]
    result = [output[0]]
    for s,p in output[1:]:
      badFirstKana = cls.first(p)
      if not badFirstKana:
        result.append([s,p])
        continue
      
      last_p = result[-1][1]
      lastBadKana = cls.last(last_p)
      thisRest = p[len(badFirstKana):]
      lastRest = last_p[:(len(last_p)-len(lastBadKana))]
      
      if len(lastRest) <= len(thisRest):
        #print("if")
        #print(lastRest)
        #print(lastBadKana)
        #print(thisRest)
        #print(badFirstKana)
        result[-1][1] += badFirstKana
        result.append([s, thisRest])
      else:
        print(last_p[:-1*(len(lastBadKana)+1)])
        result[-1][1] = last_p[:-1*(len(lastBadKana)+1)]
        result.append([s, last_p[-1*(len(lastBadKana)+1):]+p])
    return result

  
if __name__=="__main__":
  print(BadKana.formatList([["野","ノ"],["幌","ッポロ"]]))
  print(BadKana.formatList([["包","ホウチ"],["丁","ョウ"]]))
  print(BadKana.formatList([["包","ホウ"],["丁","チョウ"]]))
