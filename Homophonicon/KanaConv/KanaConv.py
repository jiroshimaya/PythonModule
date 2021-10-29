import json
import os

VOWEL_PATH = os.path.join(os.path.dirname(__file__),"dict","vowel.json")
CONSONANT_PATH = os.path.join(os.path.dirname(__file__),"dict","consonant.json")

with open(VOWEL_PATH) as f:
  voweldict = json.load(f)
with open(CONSONANT_PATH) as f:
  consonantdict = json.load(f)

class KanaConv:
  @staticmethod
  def charToVowel(char):
    return voweldict.get(char[-1], None)
  @staticmethod
  def charToConsonant(char):
    return consonantdict.get(char[-1], None)
