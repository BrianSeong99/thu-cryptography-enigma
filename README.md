# thu-cryptography Lab1

成镇宇 计76 2017080068

# Enigma

## Rejewski

该方法的主要突破口是德军的发密习惯：即每日都会发重复的两对三字母，如`XYZXYZ`，所以假设`XYZXYZ`给加密成`HGABLE`，则有X加密两次之后得到B，Y加密两次之后得到L，Z加密两次之后得到E，所以就可以得到所有可能的设置。得到之后剩下的就可以通过人工计算的方式来确认到底哪个才是正确的结论。以下是execute结果。

```bash
 jinwooseong@SEONGJINWOOs-MacBook-Pro  ~/Desktop/School/3-2/MC Modern Cryptography/HW/enigma/question_one   master ●  python3 enigma.py 
1: Encrypt
2: Rejewski
3: Turing
4: Turing Random Tests

Your Operation: 2

enter text to decode: HGABLE 
Found Rejewski Solution:
------------------------
Rotors In Use: (0, 1, 2)
Start Position: ('B', 'M', 'I')
Decoded Text: GXOGXO

Found Rejewski Solution:
------------------------
Rotors In Use: (0, 2, 1)
Start Position: ('D', 'D', 'T')
Decoded Text: LICLIC

Found Rejewski Solution:
------------------------
Rotors In Use: (0, 2, 1)
Start Position: ('Q', 'Q', 'G')
Decoded Text: AEOAEO

Found Rejewski Solution:
------------------------
Rotors In Use: (0, 2, 1)
Start Position: ('T', 'A', 'U')
Decoded Text: UDDUDD

Found Rejewski Solution:
------------------------
Rotors In Use: (1, 0, 2)
Start Position: ('D', 'D', 'G')
Decoded Text: RVRRVR

Found Rejewski Solution:
------------------------
Rotors In Use: (1, 0, 2)
Start Position: ('R', 'J', 'Z')
Decoded Text: WYSWYS

Found Rejewski Solution:
------------------------
Rotors In Use: (1, 2, 0)
Start Position: ('D', 'A', 'T')
Decoded Text: SHJSHJ

Found Rejewski Solution:
------------------------
Rotors In Use: (1, 2, 0)
Start Position: ('I', 'E', 'F')
Decoded Text: CJPCJP

Found Rejewski Solution:
------------------------
Rotors In Use: (1, 2, 0)
Start Position: ('J', 'F', 'F')
Decoded Text: CJPCJP

Found Rejewski Solution:
------------------------
Rotors In Use: (2, 0, 1)
Start Position: ('B', 'X', 'E')
Decoded Text: IWJIWJ
```

## Turing Bombe

自从德军给Enigma升级之后，Rejewski方法就不再适用。因此Turing就通过自动化遍历的方法，去进行破解。但效率并不高，后来Turing又发现德军每日会在同一时间点发送一个天气报，里面总会有重复的内容。这个就成为了`Crib`，用来猜测字母链。并且Enigma有一特征即它永远都不会把某一字母加密成自身。以上的这些性质帮助他们排除了很多不必要的搜索。从而实现了可以用的`Bombe`。以下是执行结果：

```bash
 jinwooseong@SEONGJINWOOs-MacBook-Pro  ~/Desktop/School/3-2/MC Modern Cryptography/HW/enigma/question_one   master ●  python3 enigma.py
1: Encrypt
2: Rejewski
3: Turing
4: Turing Random Tests

Your Operation: 3

cipher text to decode:  GCGXJKTDCQHIANREQOGMGGZFUQHRX
enter decoded result:  WEATHERREPORTOFTHEDAYYEAHHAHA
.
(0, 1, 2)
('A', 'A', 'B')
```

我还自己编写了一个测试脚本，运行方式如下：

```bash
python3 enigma.py
Your Operation: 4
```

脚本如下：

```python
counter = 0
iterations = random.randint(20, 150)
rotor_list = list(permutations([0, 1, 2, 3, 4], 3))
start_positions = list(product(alphabet, alphabet, alphabet))
mini_length = random.randint(3, 15)
initial_time = time.time()
for i in range(mini_length, iterations):
  rotor_in_use = rotor_list[i*i*i*i*i%len(rotor_list)]
  start_position = start_positions[i*i*i*i*i%len(start_positions)]
  enigma = Enigma(list(rotor_in_use), list(start_position), "")
  plaintext = ''.join(random.choice(alphabet) for j in range(i))
  ciphertext = enigma.encode(plaintext)
  before_analyze = time.time()
  print("Iteration: ", i-mini_length)
  print("------------------")
  print("Plain Text: ", plaintext)
  print("Cipher Text: ", ciphertext)
  print("Rotor In Use: ", list(rotor_in_use))
  print("Start Position: ", list(start_position))
  turing = Turing(ciphertext, plaintext)
  ans = turing.run()
  print()
  if ans[0] == rotor_in_use and ans[1] == start_position:
    counter = counter + 1
    print("Correct?: ", True)
    else:
      print("Correct?: ", False)
    print("Analize Time: ", time.time()-before_analyze)
    print()
  
  print()
  print("--------------------------")
  print("Totol Correct Rate: ", float(counter / (iterations-mini_length)))
  print("Total Time: ", time.time()-initial_time)
```

测试结果可以看`./question_one/turing_test_result.txt`

测试结果解释：

```bash
Iteration:  13 # this number represent test sets
------------------
Plain Text:  WVKSRDYBDWVLIMHXJNRPO # randomly generated plain text
Cipher Text:  IQFPEIWOJQFPSRLOKVGLD # the cipher text from the plain text above
Rotor In Use:  [1, 4, 0] # enigma rotors setting for the above cipher text
Start Position:  ['J', 'O', 'V'] # enigma start position setting for the above cipher text
...................... # each dot represent a rotor combination try out
Correct?:  True # is the analized result correct?
Analize Time:  582.8648953437805 # time it took to decode the cipher text
```



# Textbook Questions

## Q1.5

程序在`./question_two/q1_5.py`，结果如下

```bash
 jinwooseong@SEONGJINWOOs-MacBook-Pro  ~/Desktop/School/3-2/MC Modern Cryptography/HW/enigma/question_two   master ●  python3 q1_5.py 
Key:  0
plaintext: BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD

Key:  1
plaintext: CFFBLGZEKYVRZIZKJRSZIUZKJRGCREVZKJJLGVIDRE

Key:  2
plaintext: DGGCMHAFLZWSAJALKSTAJVALKSHDSFWALKKMHWJESF

Key:  3
plaintext: EHHDNIBGMAXTBKBMLTUBKWBMLTIETGXBMLLNIXKFTG

Key:  4
plaintext: FIIEOJCHNBYUCLCNMUVCLXCNMUJFUHYCNMMOJYLGUH

Key:  5
plaintext: GJJFPKDIOCZVDMDONVWDMYDONVKGVIZDONNPKZMHVI

Key:  6
plaintext: HKKGQLEJPDAWENEPOWXENZEPOWLHWJAEPOOQLANIWJ

Key:  7
plaintext: ILLHRMFKQEBXFOFQPXYFOAFQPXMIXKBFQPPRMBOJXK

Key:  8
plaintext: JMMISNGLRFCYGPGRQYZGPBGRQYNJYLCGRQQSNCPKYL

Key:  9
plaintext: KNNJTOHMSGDZHQHSRZAHQCHSRZOKZMDHSRRTODQLZM

Key:  10
plaintext: LOOKUPINTHEAIRITSABIRDITSAPLANEITSSUPERMAN

Key:  11
plaintext: MPPLVQJOUIFBJSJUTBCJSEJUTBQMBOFJUTTVQFSNBO

Key:  12
plaintext: NQQMWRKPVJGCKTKVUCDKTFKVUCRNCPGKVUUWRGTOCP

Key:  13
plaintext: ORRNXSLQWKHDLULWVDELUGLWVDSODQHLWVVXSHUPDQ

Key:  14
plaintext: PSSOYTMRXLIEMVMXWEFMVHMXWETPERIMXWWYTIVQER

Key:  15
plaintext: QTTPZUNSYMJFNWNYXFGNWINYXFUQFSJNYXXZUJWRFS

Key:  16
plaintext: RUUQAVOTZNKGOXOZYGHOXJOZYGVRGTKOZYYAVKXSGT

Key:  17
plaintext: SVVRBWPUAOLHPYPAZHIPYKPAZHWSHULPAZZBWLYTHU

Key:  18
plaintext: TWWSCXQVBPMIQZQBAIJQZLQBAIXTIVMQBAACXMZUIV

Key:  19
plaintext: UXXTDYRWCQNJRARCBJKRAMRCBJYUJWNRCBBDYNAVJW

Key:  20
plaintext: VYYUEZSXDROKSBSDCKLSBNSDCKZVKXOSDCCEZOBWKX

Key:  21
plaintext: WZZVFATYESPLTCTEDLMTCOTEDLAWLYPTEDDFAPCXLY

Key:  22
plaintext: XAAWGBUZFTQMUDUFEMNUDPUFEMBXMZQUFEEGBQDYMZ

Key:  23
plaintext: YBBXHCVAGURNVEVGFNOVEQVGFNCYNARVGFFHCREZNA

Key:  24
plaintext: ZCCYIDWBHVSOWFWHGOPWFRWHGODZOBSWHGGIDSFAOB

Key:  25
plaintext: ADDZJEXCIWTPXGXIHPQXGSXIHPEAPCTXIHHJETGBPC
```



## Q1.16

### a).

| x             | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    |
| ------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| $\pi^{-1}(x)$ | 2    | 4    | 6    | 1    | 8    | 3    | 5    | 7    |

### b).

GENTLEMENDONOTREADEACHOTHERSMAIL



## Q1.21

### a).

实现了一个可以通过测量frequency并提供用户选择替换letter的程序。

1. 首先ciphertext中最高频率的letter会被E换掉（因为语言学）
2. 用户选择用默认语言学ranking的字母替换还是用自己想到的字母替换
3. 直到程序结束为止

自己实验结果如下

```bash
 jinwooseong@SEONGJINWOOs-MacBook-Pro  ~/Desktop/School/3-2/MC Modern Cryptography/HW/enigma/question_two   master ● ?  python3 q1_21_1.py
FREQUENCY STATS:
A: 5    B: 0    C: 37   D: 8    E: 12   F: 9    G: 24   H: 5    I: 15   J: 7    K: 18   L: 7    M: 5    N: 13   O: 10   P: 6    Q: 1    R: 0    S: 20   T: 0  U: 14    V: 0    W: 5    X: 7    Y: 15   Z: 13
----------------

--------_---_-----W---W_-----------_-------_------------_---_--_------_----_---_-_------_-------_-----_---------------------------------W-__------W---_------_-------------_--W------_-----_--_--_---_W-__------W------_--_W-__-_--_----_--W--------_--_------_-
Action: _ -> E
Would you like to Try a Custom Letter? Y/N n
Substitude Letter:  C -> E

--_-----E_--E-----W---WE--------_--E-------E-----_--_---E_--E_-E------E----E---E-E------E_------E-----E_---_--_-_-------_-----_--------_W-EE--_---W---E------E_----------_-E_-W_-----E-_---E--E--E---EW-EE--_---W------E--EW-EE-E--E----E--W-----_--E--E---_--E-
Action: _ -> A
Would you like to Try a Custom Letter? Y/N n
Substitude Letter:  G -> A

--A--_--EA--E-_--_W--_WE--------A--E---_---E-----A--A---EA--EA-E-_--_-E---_E---E-E-_--_-EA------E--_--EA---A--A-A---_---A---_-A---_----AW-EE--A--_W-_-E------EA----------A-EA-WA---_-E-A---E--E--E---EW-EE--A--_W------E_-EW-EE-E--E----E_-W-----A--E--E---A--E-
Action: _ -> R
Would you like to Try a Custom Letter? Y/N 

.........
```

通过各种尝试，最后得出substitution表：

```python
sub = {'A':'v', 'B':'x', 'C':'e', 'D':'b', 'E':'i', 'F':'w', 'G':'a', 'H':'f', 'I':'d', 'J':'c', 'K':'s', 'L':'y', 'M':'m', 'N':'l', 'O':'n', 'P':'u', 'Q':'j', 'R':'k', 'S':'o', 'T':'z', 'U':'t', 'V':'q', 'W':'g', 'X':'p', 'Y':'r', 'Z':'h'}
```

内容如下：

```
i may not be able to grow flowers but my garden produces just as many dead leaves old over shoes pieces of rope and bushels of dead grass as anybodys and today i bought a wheel barrow to help in clearing it up i have always loved and respected the wheel barrow it is the one wheeled vehicle of which i am perfect master
```

### b).

重合指数法

m=1 => 0.041

m=2 => 0.038, 0.047

m=3 => 0.055, 0.048, 0.048

m=4 => 0.037, 0.043, 0.038, 0.049

m=5 => 0.043,0.043, 0.033, 0.035, 0.043

m=6 => 0.063, 0.084, 0.049, 0.065, 0.043, 0.073

当m=6时与0.65较接近

所以密钥是 2, 17, 24, 15, 19, 14

明文是：

```
i learned how to calculate the amount of paper needed for a room when i was at school you multiply the square footage of the walls by the cubic contents of the floor and ceiling combined and double it you then allow half the total for openings such as windows and doors then you allow the other half for matching the pattern then you double the whole thing again to give a margin of error and then you order the paper
```

### c).

统计频数为：

```bash
FREQUENCY STATS:
A: 13   B: 21   C: 32   D: 9    E: 14   F: 9    G: 0    H: 1    I: 16   J: 6    K: 20   L: 0    M: 0    N: 1    O: 2    P: 20   Q: 4    R: 12   S: 1    T: 0  U: 6     V: 4    W: 0    X: 2    Y: 1    Z: 4
```

所以C加密为E

设ax+b(mod 26)

则有4a+b=2(mod 26)，其中4时E的index，2时C的index

其他的字母则直接通过暴力遍历，与上一题的方法类似，也是求到m近似0.065。最后求的密钥19，4

明文是：

```
o canada
terre de nos aieux
ton front est ceint de faeurons glorieux
car ton bras sait porter lepee
il sait porter la croix
ton histoire est une epopee
des plus brillants exploits
et ta valeur de foi trempee
protegera nos foyers et nos droits
```

### d).

```bash
FREQUENCY STATS:
A: 17   B: 17   C: 18   D: 9    E: 21   F: 16   G: 16   H: 17   I: 16   J: 12   K: 13   L: 23   M: 21   N: 4    O: 7    P: 8    Q: 6    R: 15   S: 23   T: 12 U: 12    V: 21   W: 11   X: 9    Y: 22   Z: 7
```

采用以上的几种方法，最后发现时维吉尼亚加密，结果如下：

key：19, 7, 4, 14, 17, 24

```
i grew up among slow talkers men in particular who dropped words a few at a time like beans in a hill and when i got to minneapolis where people took a lake wobegon comma to mean the end of a story i couldnt speak a whole sentence in company and was considered not too briaht so i enrolled in a speech couqse taught by orvilles and the founder of reflexive relaxology a self hypnotic technique that enabled a person to speak up to three hundred words per minute
```



## Q1.26

### a).

将密文写成m*n的矩阵，随后按行构成明文

### b).

```python
ciphertext = 'MYAMRARUYIQTENCTORAHROYWDSOYEOUARRGDERNOGW'

def decrypt(m, x, y):
  plaintext = ""
  for i in range(m):
    counter = 0
    for col in range(y):
      for row in range(x):
        plaintext += ciphertext[i*x*y + y*row + col]
  return plaintext.lower()

print(decrypt(7, 3, 2))
```

执行结果：

```bash
python3 q1_26.py
marymaryquitecontraryhowdoesyourgardengrow
```

