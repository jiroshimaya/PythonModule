from re import S
import editdistance as ed
import csv
import os, copy
from typing import Optional, TypedDict, Union
from Morasep import Morasep

class WordDict(TypedDict):
  surface: str
  token: tuple[str,...]
class ScoreDict(TypedDict):
  score: Union[int, float]
  word: WordDict
  original: WordDict
class WordSeqDict(TypedDict):
  score: Union[int, float]
  words: list[ScoreDict]

class Homophonicon:

  @classmethod
  def execute(cls, text: str, wordlist) -> WordSeqDict:
    memo: dict[int, WordSeqDict] = {}
    
    def getWord(word: WordDict) -> ScoreDict:
      ranks: list[ScoreDict] = cls.getHomophonicRank(word, wordlist)
      if len(ranks) == 0:
        #return ScoreDict(score=float("inf"), word="")
        return ScoreDict(score=float("inf"), word="")
      else:
        return ranks[0]

    tokens = cls.tokenize(text)
    
    def dp(l) -> WordSeqDict:
      if l in memo:
        return memo[l]
      original = WordDict(surface=cls.detokenize(tokens[:l]), token=tokens[:l])
      dist = getWord(original)
      ws1 = WordSeqDict(
        score=dist["score"], 
        words=[dist]
      )
      if l <= 1:
        memo[l] = ws1
        return memo[l]
      results: list[WordSeqDict] = [ws1]
      for i in range(1,l):
        #deepcopyしないと直前のループで作ったリストも編集されてしまう
        ws1 = copy.deepcopy(dp(i))

        original = WordDict(surface=cls.detokenize(tokens[i:l]), token=tokens[i:l])
        w = getWord(original)
        ws1["score"] += w["score"]
        ws1["words"].append(w)
        results.append(ws1)
      
      if len(results) == 0:
        result = WordSeqDict(dist=float("inf"),words = [])
      else:
        result = sorted(results, key=lambda x: x["score"])[0]
      memo[l] = result
      return result 
    return dp(len(text)) 
  
  @classmethod
  def getHomophonicRank(cls, word: WordDict, wordlist: list[WordDict]) -> list[ScoreDict]:
    scores = []
    token1 = word["token"]
    for w in wordlist:
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
  def detokenize(token: tuple[str, ...]) -> str:
    return "".join(token)
  
  @staticmethod
  def getDistance(token1, token2)->int:
    dist = ed.eval(token1, token2)
    return dist

  
    
  @classmethod
  def getWordList(cls, path: str) -> list[WordDict]:
    with open(path) as f:
      reader = csv.reader(f)
      words = [row[0] for row in reader]
    words = [w.strip() for w in words]
    words = [WordDict(surface=w, token=Morasep.split(w)) for w in words]
    return words
  
  @staticmethod
  def getTestWord(path: str) -> list[str]:
    with open(path) as f:
      reader = csv.reader(f)
      words = [row[0] for row in reader]
    words = [w.strip() for w in words]
    return words

  
if __name__=="__main__":
  TESTCASE_PATH = os.path.join(os.path.dirname(__file__),"data","testtext.txt")
  testwords = Homophonicon.getTestWord(TESTCASE_PATH)

  PATH = os.path.join(os.path.dirname(__file__),"wordlist","pokemon.txt")
  pokemonlist = Homophonicon.getWordList(PATH)
  for w in testwords:
    result = Homophonicon.execute(w, pokemonlist)
    words = result["words"]
    original = [w["original"]["surface"] for w in words]
    converted = [w["word"]["surface"] for w in words]
    print(w)
    print(original)
    print(converted)
    print("")
