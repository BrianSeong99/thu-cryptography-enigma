rotorsInUse = [0, 1, 2]
rotors = [
  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
  "VZBRGITYUPSDNHLXAWMJQOFECK"
]
rotorNotches = ["Q", "E", "V", "J", "Z"]
reflector = {"A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D","E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I","J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T","V":"W","W":"V"}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ringPosition = ["H","D","X"]
plugboard = ""

plugboardConnections = plugboard.upper().split(" ")
plugboardDict = {}
for pair in plugboardConnections:
  if len(pair)==2:
    plugboardDict[pair[0]] = pair[1]
    plugboardDict[pair[1]] = pair[0]

rotorsInUse = [rotors[0], rotors[1], rotors[2]]

def getRotor(index):
  return rotors[index]

def getRotorNotch(index):
  return rotorNotches[index]

def rotate(index):
  ringPosition[index] = alphabet[
    (alphabet.index(ringPosition[index])+1) % 26
  ]

def rotateAndCheckNextRotate(index):
  flag = False
  if ringPosition[index] == getRotorNotch(index):
    flag = True
  rotate(index)
  return flag

def rotorEncrypt(encryptedLetter, index, offset):
  pos = alphabet.index(encryptedLetter)
  char = getRotor(index)[(pos+offset)%26]
  pos = alphabet.index(char)
  return alphabet[(pos-offset+26)%26]

def rotorEncryptReflect(encryptedLetter, index, offset):
  pos = alphabet.index(encryptedLetter)
  char = alphabet[(pos+offset)%26]
  pos = getRotor(index).index(char)
  return alphabet[(pos-offset+26)%26]

def encode(plaintext):
  ciphertext = ""
  plaintext = plaintext.upper()
  for char in plaintext:
    encryptedLetter = char





    if char in alphabet:
      # rotate rotors
      if rotateAndCheckNextRotate(2): # check if need to rotate the second rotor
        if rotateAndCheckNextRotate(1):
          rotateAndCheckNextRotate(0)
      elif ringPosition[1] == getRotorNotch(1): # check double step sequence
        rotate(1)
        rotate(0)
        
      if char in plugboardDict.keys():
        if plugboardDict[char]!="":
          encryptedLetter = plugboardDict[char]

  

      # encrypt
      offset = []
      for i in range(3):
        offset.append(alphabet.index(ringPosition[i]))
  



      for i in range(3):
    
    
    
        encryptedLetter = rotorEncrypt(encryptedLetter, 2-i, offset[2-i])
      
  
  
  

      if encryptedLetter in reflector.keys():
        if reflector[encryptedLetter] != "" :
          encryptedLetter = reflector[encryptedLetter]
      
      for i in range(3):
    
    
    
        encryptedLetter = rotorEncryptReflect(encryptedLetter, i, offset[i])
      
  
  
  

      if encryptedLetter in plugboardDict.keys():
        if plugboardDict[encryptedLetter]!="":
          encryptedLetter = plugboardDict[encryptedLetter]
      
    ciphertext = ciphertext + encryptedLetter
  return ciphertext




if __name__ == "__main__":
  plaintext = input("enter text to code: ")
  ciphertext = encode(plaintext)
  print(ciphertext)