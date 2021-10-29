from re import S
import editdistance as ed
import csv
import os, copy
from typing import Optional, TypedDict, Union


class ScoreDict(TypedDict):
  score: Union[int, float]
  word: str
  original: str
class WordSeqDict(TypedDict):
  score: Union[int, float]
  words: list[ScoreDict]

class Homophonicon:

  @classmethod
  def execute(cls, text, wordlist) -> WordSeqDict:

    memo: dict[int, WordSeqDict] = {}
    
    def getWord(token: str) -> ScoreDict:
      ranks: list[ScoreDict] = cls.getHomophonicRank(token, wordlist)
      if len(ranks) == 0:
        return ScoreDict(dist=float("inf"), word="")
      else:
        return ranks[0]

    def dp(l) -> WordSeqDict:
      if l in memo:
        return memo[l]
      if l == 1:
        dist = getWord(text[:l])
        memo[l] = WordSeqDict(
          score=dist["score"], 
          words=[dist]
          )
        return memo[l]
      results: list[WordSeqDict] = []
      for i in range(1,l):
        #deepcopyしないと直前のループで作ったリストも編集されてしまう
        ws1 = copy.deepcopy(dp(i))

        w = getWord(text[i:l])
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
  def getHomophonicRank(cls, word: str, wordlist) -> list[ScoreDict]:
    dists = []
    for w in wordlist:
      dist = cls.getDistance(word, w)
      d = ScoreDict(score=dist, word=w, original=word)
      dists.append(d) #単語と距離をセットで格納
    
    dists.sort(key=lambda x:x["score"]) #距離の短い順にソート
    return dists
  
  @staticmethod
  def getDistance(word1: str, word2: str)->int:
    dist = ed.eval(word1, word2)
    return dist
    
  @classmethod
  def getWordList(cls, path: str):
    with open(path) as f:
      reader = csv.reader(f)
      words = [row[0] for row in reader]
    words = [w.strip() for w in words]
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
    original = [w["original"] for w in words]
    converted = [w["word"] for w in words]
    print(w)
    print(original)
    print(converted)
    print("")
