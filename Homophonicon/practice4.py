import editdistance as ed
import csv
import os, copy
from typing import Optional, TypedDict, Union
from Morasep import Morasep
import random, datetime


class TokenDict(TypedDict):
  surface: str
  token: tuple[str,...]
class WordDict(TokenDict):
  id: int
class ScoreDict(TypedDict):
  score: Union[int, float]
  word: WordDict
  original: TokenDict
class WordSeqDict(TypedDict):
  score: Union[int, float]
  words: list[ScoreDict]

class Homophonicon:

  @classmethod
  def execute(cls, text: str, wordlist) -> WordSeqDict:
    memo: dict[(int,int), WordSeqDict] = {}
    #usedWordId = set()
    
    def getWord(word: WordDict, usedWordId: set[int]) -> ScoreDict:
      ranks: list[ScoreDict] = cls.getHomophonicRank(word, wordlist)
      for r in ranks:
        id = r["word"]["id"]
        if id in usedWordId: continue
        #usedWordId.add(id)
        return r
      return ScoreDict(score=float("inf"), word=WordDict(surface="",token=(),id=-1), original=word)

    tokens = cls.tokenize(text)
    

    def dp(s,e, usedWordId: set[int]) -> WordSeqDict:
      #他の関数への影響を与えないように値コピーする
      
      if (s,e) in memo:
        return memo[s,e]
      
      original = WordDict(surface=cls.detokenize(tokens[s:e]), token=tokens[s:e])
      dist = getWord(original, usedWordId)
      ws1 = WordSeqDict(
          score=dist["score"], 
          words=[dist]
        )

      if e-s == 1:
        memo[s,e] = ws1
        return ws1
      
      results = []
      if ws1["score"] < float("inf"):
        results.append(ws1)
      for i in range(s+1,e):
        ws2 = copy.deepcopy(dp(s,i))
        ws3 = copy.deepcopy(dp(i,e))

        ws2["score"] += ws3["score"]
        ws2["words"] += ws3["words"]
        if ws2["score"] == float("inf"):
          continue
        results.append(ws2)
      
      if len(results) == 0:
        result = WordSeqDict(score=float("inf"),words = [])
      else:
        result = sorted(results, key=lambda x: x["score"])[0]
      memo[s,e] = result
      #print(l,result)
      return result 
      
    return dp(0,len(text)) 
  
  @classmethod
  def getHomophonicRank(cls, word: TokenDict, wordlist: dict[int, list[WordDict]]) -> list[ScoreDict]:
    scores = []
    token1 = word["token"]
    for w in wordlist.get(len(token1),[]):
      token2 = w["token"]
      s = cls.getDistance(token1,token2)
      score = ScoreDict(score=s, word=w, original=word)
      scores.append(score) #単語と距離をセットで格納
    
    scores.sort(key=lambda x:x["score"]) #距離の短い順にソート
    return scores
  @staticmethod
  def tokenize(text: str) -> tuple[str, ...]:
    return Morasep.split(text)
  @staticmethod
  def detokenize(token: tuple[str, ...]):
    return "".join(token)
  
  @staticmethod
  def getDistance(token1, token2)->int:
    dist = ed.eval(token1, token2)
    return dist

  @classmethod
  def getWordList(cls, path: str) -> dict[int, list[WordDict]]:
    with open(path) as f:
      reader = csv.reader(f)
      words = [row[0] for row in reader]
    words = [w.strip() for w in words]
    words = [WordDict(surface=w, token=Morasep.split(w), id=i) for i,w in enumerate(words)]
    wordsobj = {}
    for w in words:
      length = len(w["token"])
      if length not in wordsobj:
        wordsobj[length] = []
      wordsobj[length].append(w)
    return wordsobj
  
def getTestWord(path: str) -> list[str]:
  with open(path) as f:
    reader = csv.reader(f)
    words = [row[0] for row in reader]
  words = [w.strip() for w in words]
  return words

  
if __name__=="__main__":
  TESTCASE_PATH = os.path.join(os.path.dirname(__file__),"data","testtext.txt")
  testwords = getTestWord(TESTCASE_PATH)

  PATH = os.path.join(os.path.dirname(__file__),"wordlist","pokemon.txt")
  pokemonlist = Homophonicon.getWordList(PATH)
  for w in testwords:
    result = Homophonicon.execute(w, pokemonlist)
    words = result["words"]
    original = [w["original"]["surface"] for w in words]
    converted = [w["word"]["surface"] for w in words]
    print(w)
    print(result["score"])
    print(original)
    print(converted)
    print("")
