from itertools import permutations, product
from collections import defaultdict
from copy import copy
import random
import time

rotors = [
  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
  "VZBRGITYUPSDNHLXAWMJQOFECK"
]
rotor_notches = ["Q", "E", "V", "J", "Z"]
reflector = {"A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D","E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I","J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T","V":"W","W":"V"}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Enigma:
  def __init__(self, rotors_in_use, ring_position, plugboard):
    self.rotors_in_use = rotors_in_use
    self.ring_position = ring_position
    self.pb_connections = plugboard.upper().split(" ")
    self.pb_dict = {}
    for pair in self.pb_connections:
      if len(pair)==2:
        self.pb_dict[pair[0]] = pair[1]
        self.pb_dict[pair[1]] = pair[0]

  def get_rotor(self, index):
    return rotors[self.rotors_in_use[index]]

  def get_rotor_notch(self, index):
    return rotor_notches[index]

  def rotate(self, index):
    self.ring_position[index] = alphabet[
      (alphabet.index(self.ring_position[index])+1) % 26
    ]

  def rotate_and_check_next_rotate(self, index):
    flag = False
    if self.ring_position[index] == self.get_rotor_notch(self.rotors_in_use[index]):
      flag = True
    self.rotate(index)
    return flag

  def rotor_encrypt(self, encryptedLetter, index, offset):
    pos = alphabet.index(encryptedLetter)
    char = self.get_rotor(index)[(pos+offset)%26]
    pos = alphabet.index(char)
    return alphabet[(pos-offset+26)%26]

  def rotor_encrypt_reflect(self, encryptedLetter, index, offset):
    pos = alphabet.index(encryptedLetter)
    char = alphabet[(pos+offset)%26]
    pos = self.get_rotor(index).index(char)
    return alphabet[(pos-offset+26)%26]

  def encode(self, plaintext):
    ciphertext = ""
    plaintext = plaintext.upper()
    for char in plaintext:
      encryptedLetter = char

      if char in alphabet:
        # rotate rotors
        if self.rotate_and_check_next_rotate(2): # check if need to rotate the second rotor
          if self.rotate_and_check_next_rotate(1):
            self.rotate_and_check_next_rotate(0)
        elif self.ring_position[1] == self.get_rotor_notch(1): # check double step sequence
          self.rotate(1)
          self.rotate(0)
          
        if char in self.pb_dict.keys():
          if self.pb_dict[char]!="":
            encryptedLetter = self.pb_dict[char]

        # encrypt
        offset = []
        for i in range(3):
          offset.append(alphabet.index(self.ring_position[i]))
    
        for i in range(3):
          encryptedLetter = self.rotor_encrypt(encryptedLetter, 2-i, offset[2-i])

        if encryptedLetter in reflector.keys():
          if reflector[encryptedLetter] != "" :
            encryptedLetter = reflector[encryptedLetter]
        
        for i in range(3):
          encryptedLetter = self.rotor_encrypt_reflect(encryptedLetter, i, offset[i])

        if encryptedLetter in self.pb_dict.keys():
          if self.pb_dict[encryptedLetter]!="":
            encryptedLetter = self.pb_dict[encryptedLetter]
        
      ciphertext = ciphertext + encryptedLetter
    return ciphertext

class Rejewski:
  def rejewski_analyse(self, ciphertext):
    rotor_list = list(permutations([0, 1, 2], 3))
    start_positions = list(product(alphabet, alphabet, alphabet))
    
    for rotor_combination in rotor_list:
      for start_position in start_positions:
        enigma = Enigma(list(rotor_combination), list(start_position), "")
        decoded = enigma.encode(ciphertext)
        if decoded[0]==decoded[3] and decoded[1]==decoded[4] and decoded[2]==decoded[5]:
          print("Found Rejewski Solution:")
          print("------------------------")
          print("Rotors In Use: "+str(rotor_combination))
          print("Start Position: "+str(start_position))
          print("Decoded Text: "+str(decoded))
          print()

class Turing:
  def __init__(self, ciphertext, plaintext):
    self.rotor_list = list(permutations([0, 1, 2, 3, 4], 3))
    self.start_positions = list(product(alphabet, alphabet, alphabet))
    self.plaintext = plaintext
    self.ciphertext = ciphertext
    self.rings = []

  def find_rings(self, index, stack):
    # to find the rings
    for i in range(len(self.plaintext)):
      if index == 0:
        stack.append(i)
        self.find_rings(index+1, stack)
        stack.pop()
      elif self.ciphertext[stack[-1]] == self.plaintext[i] and i not in stack:
        stack.append(i)
        plain_letter = self.plaintext[stack[0]]
        cipher_letter = self.ciphertext[i]
        if plain_letter == cipher_letter:
          self.find_rings(index+1, stack)
          self.rings.append(copy(stack))
        elif index != len(self.plaintext)-1:
          self.find_rings(index+1, stack)
        stack.pop()
    
  def eliminate_duplicates(self):
    rings = []
    for ring in self.rings:
      next_i = ring[0]
      current_i = 0
      for index, letter_index in enumerate(ring):
        if next_i > letter_index:
          current_i = index
          next_i = ring[0]
    for ring in self.rings:
      if ring not in rings:
        rings.append(ring)
    self.rings = rings

  def check_if_encrypt_to_same_letter(self, rotor_in_use, start_position, ring, letter):
    ans = " "
    current_letter = letter
    current_position = start_position

    for letter in ring:
      changed_position = (ord(current_position[2])-ord('A')+letter) % 26
      current_position = [start_position[0], start_position[1], chr(changed_position+ord('A'))]
      enigma = Enigma(rotor_in_use, current_position, "")
      current_letter = enigma.encode(current_letter)
    
    return letter == current_letter

  def run(self):
    self.find_rings(0, [])
    self.eliminate_duplicates()

    for rotor_in_use in self.rotor_list:
      print(".", end="", flush=True)
      for start_position in self.start_positions:
        all_ring_true = True
        for ring in self.rings:
          for letter in alphabet:
            if self.check_if_encrypt_to_same_letter(list(rotor_in_use), list(start_position), ring, letter):
              all_ring_true = False
              break
          if not all_ring_true:
            break
        if all_ring_true:
          enigma = Enigma(list(rotor_in_use), list(start_position), "")
          ans = enigma.encode(self.plaintext)
          if ans == self.ciphertext:
            return [rotor_in_use, start_position]

if __name__ == "__main__":
  
  selection = input("1: Encrypt\n2: Rejewski\n3: Turing\n4: Turing Random Tests\n\nYour Operation: ")
  
  if selection == "1":
    plaintext = input("enter text to encode: ")
    rotors_in_use = [0, 1, 2]
    ring_position = ["H","D","X"]
    plugboard = ""
    enigma = Enigma(rotors_in_use, ring_position, plugboard)
    ciphertext = enigma.encode(plaintext)
    print(ciphertext)
  
  elif selection == "2":
    plaintext = input("enter text to decode: ") # HGABLE
    analizer = Rejewski()
    analizer.rejewski_analyse(plaintext)
  
  elif selection == "3":
    ciphertext = "GCGXJKTDCQHIANREQOGMGGZFUQHRX"
    plaintext = "WEATHERREPORTOFTHEDAYYEAHHAHA"
    print("cipher text to decode: ", ciphertext)
    print("enter decoded result: ", plaintext)
    turing = Turing(ciphertext, plaintext)
    ans = turing.run()
    print(ans[0])
    print(ans[1])
  
  elif selection == "4":
    counter = 0
    iterations = random.randint(50, 150)
    rotor_list = list(permutations([0, 1, 2, 3, 4], 3))
    start_positions = list(product(alphabet, alphabet, alphabet))
    mini_length = random.randint(3, 20)
    initial_time = time.time()
    print()
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

