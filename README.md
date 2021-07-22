# PythonModule
Repository for original moudules of python

Basically, needed packages in each module are managed via pipenv.
You can check the output and test result of each modules using commands like following

```
% cd [module directory]
% pipenv run start #check the output of the function
% pipenv run test  #execute test program
```

Included modules as follows
# IndependentWord
module for extract independent words from Japanese text as follows:

```
>>>from IndependentWord as IndependentWord
>>>iw = IndependentWord()
>>>iw.extract("あらゆる現実が私の方に捻じ曲げられたのだ")
["現実",'捻じる', '曲げる']
```

