import os

class Homophonicon:

  @classmethod
  def getHomophonicWord(cls, word, wordlist):
    dists = []
    for w in wordlist:
      dist = cls.getDistance(word, w)
      dists.append([w, dist]) #単語と距離をセットで格納
    
    dists.sort(key=lambda x:x[-1]) #距離の短い順にソート
    
    return dists[0][0]
  
  @staticmethod
  def getDistance(word1, word2):
    dist = 0
    assert len(word1) == len(word2)
    for c1,c2 in zip(word1,word2):
      if c1 != c2: dist += 1
    return dist
    
  @classmethod
  def getWordList(cls, path):
    with open(path) as f:
      wordlist = f.read().strip().splitlines()
    wordlist = [w.strip() for w in wordlist if w] #空文字を除く、前後の空白を除く
    
    return wordlist
  
if __name__=="__main__":
  cases = [
    "サトウ",
    "スズキ",
    "タカハシ",
    "タナカ",
    "イトウ",
    "ワタナベ",
    "ヤマモト"
    ]
  PATH = os.path.join(os.path.dirname(__file__),"wordlist","pokemon.txt")
  pokemonlist = Homophonicon.getWordList(PATH)
  for c in cases:
    print(c, Homophonicon.getHomophonicWord(c, pokemonlist))
