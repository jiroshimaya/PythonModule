from re import S
import editdistance as ed
import csv
import os

#型エイリアスの作成。型がややこしくなるのできちんと管理する。
WORDLIST = list[str]
class Homophonicon:

  @classmethod
  def execute(cls, word: str, wordlist: WORDLIST) -> str:
    ranks = cls.getHomophonicRank(word, wordlist)
    return ranks[0][0]
  
  @classmethod
  def getHomophonicRank(cls, word: str, wordlist: WORDLIST) -> list[tuple[dict, int]]:
    dists = []
    for w in wordlist:
      dist = cls.getDistance(word, w)
      dists.append((w, dist)) #単語と距離をセットで格納
    
    dists.sort(key=lambda x:x[-1]) #距離の短い順にソート
    return dists
  
  @staticmethod
  def getDistance(word1: str, word2: str)->int:
    dist = ed.eval(word1, word2)
    return dist
    
  @classmethod
  def getWordList(cls, path: str) -> WORDLIST:
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
  TESTCASE_PATH = os.path.join(os.path.dirname(__file__),"data","testword.txt")
  testwords = Homophonicon.getTestWord(TESTCASE_PATH)

  PATH = os.path.join(os.path.dirname(__file__),"wordlist","pokemon.txt")
  pokemonlist = Homophonicon.getWordList(PATH)
  for w in testwords:
    print(w, Homophonicon.execute(w, pokemonlist))
