import os
import json
import mojimoji


ENGLISH_DICT_PATH = os.path.join(os.path.dirname(__file__),"data","bep-eng.json")
ROMAN_TREE_PATH = os.path.join(os.path.dirname(__file__),"data","tree_roma2kana.json")
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
 
  
class Apostrophe:
  STRING = "APOSTROPHE"
  APOS = "'"
  OTHER_APOS = "’" 
  @classmethod
  def toString(cls,text):
    return text.replace(cls.OTHER_APOS, cls.APOS).replace(cls.APOS,cls.STRING)
  @classmethod
  def toSign(cls,text):
    return text.replace(cls.STRING, cls.APOS)
  @classmethod
  def removeString(cls, text):
    return text.reaplce(cls.STRING, "")
  @classmethod
  def include(cls, text):
    return cls.STRING in text
  @classmethod
  def format(cls, text):
    return text.replace(OTHER_APOS, APOS)

class English:
  english = JsonLoader.loadRelative(ENGLISH_DICT_PATH)
  
  @staticmethod
  def load(path=None):
    if not path:
      path = PATH
    path = os.path.join(os.path.dirname(__file__), path)
    data = None
    with open(path, "r") as f:
      data = json.load(f)
    return data
  @staticmethod
  def zenToHan(text):
    return mojimoji.zen_to_han(text)
  
  @staticmethod
  def romanToKana(text):
    pass 

class Token:
  def __init__(self,tokens):
    self.tokens = tokens
    self.idx = 0
  
  def exist(self):
    if self.idx < 0: return False
    if len(self.tokens) <= self.idx: return False
    return True
  def read(self):
    return self.tokens[self.idx]
  def next(self):
    self.idx += 1
    return self.tokens[self.idx]
  
class RomanToKana:
  tree = JsonLoader.load(ROMAN_TREE_PATH)    
  
  @classmethod
  def isUnit(cls, tokens, s):
    return tokens[:s] in cls.tree

  @classmethod
  def unit(cls, tokens, s):
    idx = s
    node = cls.tree
    while idx < len(tokens):
      char = tokens[idx]
      if char not in node:
        return "", s
      node = node[char]
      idx+=1
      if type(node) is str:
        return node, idx
    return "", s

  @classmethod
  def isSokuon(cls, tokens, s):
    if s+1 < len(tokens):
      return False
    if tokens[s] != tokens[s+1]:
      return False
    if tokens[s] not in cls.tree:
      return False    
    return True
    
  @classmethod
  def isHatsuon(cls, tokens, s):
    if s < len(tokens):
      return False
    if tokens[s] not in ["n","m"]:
      return False
    return True
    
        
  @classmethod
  def readHead(cls, tokens, node):
    char = text[0]
    if char.isalpha():
      
  @classmethod
  def execute(cls, text):
    text = text.lower()
    result = ""
    tmp = ""
    index = 0
    node = cls.tree
    
    def push(char, toRoot:bool=True):
      nonlocal result
      result += char
      tmp = ""
      if toRoot:
        node = cls.tree    
        
      
    while index < len(text):
      char = text[index]
      if char.isalpha():
        if char in node:
          next = node[char]
          if type(next) is str:
            push(next)
          else:
            tmp += text[index]
            node = next
          index += 1
          print(index)
          continue
        prev = text[index-1]
        if prev and (prev =="n" or prev == char):
          push("ン" if prev == "n" else "ッ", False)
        if node != cls.tree and char in cls.tree:
          push(tmp)
          print(result)
          continue
      push(tmp + char)
      index += 1
      print(index)
    if tmp.endswith("n"):
      tmp = tmp[:-1]+"ン"
    push(tmp)
    return result;
    
    
a = """
function English(DICTIONARY, TREE){
  const AP = Apostrophe();
  
  function zenkakuEnglishToHankaku(text){
    return text.replace(/[Ａ-Ｚａ-ｚ]/, s => String.fromCharCode(s.charCodeAt(0) - 65248)); // 全角→半角
  }
  function romanToKana(text, tree){
    let str = text.toLowerCase();
    let result = '';
    let tmp = '';
    let index = 0;
    const len = str.length;
    let node = tree;
    const push = (char, toRoot = true) => {
      result += char;
      tmp = '';
      node = toRoot ? tree : node;
    };
    while (index < len) {
      const char = str.charAt(index);
      if (char.match(/[a-z]/)) { // 英数字以外は考慮しない
        if (char in node) {
          const next = node[char];
          if (typeof next === 'string') {
            push(next);
          } else {
            tmp += text.charAt(index);
            node = next;
          }
          index++;
          continue;
        }
        const prev = str.charAt(index - 1);
        if (prev && (prev === 'n' || prev === char)) { // 促音やnへの対応
          push(prev === 'n' ? 'ン' : 'ッ', false);
        }
        if (node !== tree && char in tree) { // 今のノードがルート以外だった場合、仕切り直してチェックする
          push(tmp);
          continue;
        }
      }
      push(tmp + char);
      index++;
    }
    tmp = tmp.replace(/n$/, 'ン'); // 末尾のnは変換する
    push(tmp);
    return result;
  }

  //textが英単語だったら
  function englishWordToKana(text, dictionary){
    const e2k = dictionary;//英単語をカナに変換する辞書
    let upper = text.toUpperCase();//英語は大文字に直しておく
    if(upper in e2k)return e2k[upper];
    else return text;
  }

  //
  function alphabetToKana(text, dictionary){
    const e2k = dictionary;
    text = text.toUpperCase();
    let found = text.match(/[A-Z]/g);//iは大文字小文字無視。
    if(found){
      for(let v of found){
        text = text.split(v).join(e2k[v]);
      }    
    }
    return text;
  }
  //英単語のみの文字列を入力
  function englishToKana(text, dictionary, tree){
    text = zenkakuEnglishToHankaku(text);
    text = englishWordToKana(text, dictionary);
    text = romanToKana(text, tree);
    text = alphabetToKana(text, dictionary);
    return text;  
  }
  
  function isFullmatch(text){
    return /^[a-zA-Z']+$/.test(text);
  }
  
  function tokenize(text,tokenizer){
    const strVal = AP.toString(text);
    //tokenize
    let tokens = tokenizer.tokenize(strVal);
    //let tokens2 = JSON.parse(JSON.stringify(tokens));
    //console.log("english",tokens2);
    
    //surfaceの修正、pronunciationの代入
    tokens = tokens.map(token=>{
      if(isFullmatch(token.surface_form)){
        //console.log("english fullmatched");
        token.surface_form = AP.toSign(token.surface_form);
        if(token.pronunciation === "*"){
          token.pronunciation = englishToKana(token.surface_form, DICTIONARY, TREE);          
        }
      }
      return token;
    });
    //tokens2 = JSON.parse(JSON.stringify(tokens));
    //console.log("english",tokens2);
    
    return tokens;
  }
  
  
  return {
    toKana: function(text){
      return englishToKana(text, DICTIONARY, TREE)
    },
    tokenize: function(text, tokenizer){
      return tokenize(text, tokenizer);
    },
    apostrophe: AP,
    isFullmatch: isFullmatch,
  }
}
"""
if __name__=="__main__":
  testcase = [
    "Hello",
    "I'm"
    ]
  print(RomanToKana.execute("konnichiwan"))