from collections import defaultdict
import re

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ciphertext = 'EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCKQPKUGKMGOLICGINCGACKSNISACYKZSCKXECJCKSHYSXCGOIDPKZCNKSHICGIWYGKKGKGOLDSILKGOIUSIGLEDSPWZUGFZCCNDGYYSFUSZCNXEOJNCGYEOWEUPXEZGACGNFGLKNSACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNCIACZEJNCSHFZEJZEGMXCYHCJUMGKUCY'

frequency = defaultdict(int)

for letter in ciphertext:
  frequency[letter] += 1

print("FREQUENCY STATS:")
for letter in alphabet:
  print(letter + ": " + str(frequency[letter]), end="\t")
print()
print("----------------")
print()

letter_used_ranking = ["E","A","R","I","O","T","N","S","L","C","U","D","P","M","H","G","B", "Y","W","K","V","X","Z","J","Q"] 
# got it from https://www.lexico.com/explore/which-letters-are-used-most
# F is being removed due to the known property, F->W

plaintext = list("-"*len(ciphertext))

def get_current_highest_frequency():
  max_value = max(frequency.values())  # maximum value
  if max_value == 0:
    exit(0)
  max_key = [k for k, v in frequency.items() if v == max_value][0] # getting all keys containing the `maximum`

  frequency[max_key] = 0
  return max_key

custom_flag = False
custom_letter = ''

for i, letter in enumerate(ciphertext):
  if letter == 'F':
    plaintext[i] = 'W'

for current_rank_letter in letter_used_ranking:
  current_max_key = get_current_highest_frequency()
  current_substitue_letter = current_rank_letter
  if current_max_key == 'F':
    pass
  
  for i, letter in enumerate(ciphertext):
    if letter == current_max_key:
      plaintext[i] = "_"
  print(''.join(plaintext))
  print("Action: _ ->", current_substitue_letter)

  if input("Would you like to Try a Custom Letter? Y/N ").lower() == 'y':
    current_substitue_letter = input("Please Type the Letter: ").upper()

  for i, letter in enumerate(ciphertext):
    if letter == current_max_key:
      plaintext[i] = current_substitue_letter
  print("Substitude Letter: ", current_max_key, "->", current_substitue_letter)
  print()

print()
print(''.join(plaintext))
