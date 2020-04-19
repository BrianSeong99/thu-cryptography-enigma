import numpy as np

ciphertext = 'BEEAKFYDJXUQYHYJIQRYHTYJIQFBQDUYJIIKFUHCQD'

for key in range(26):
  print("Key: ", key)
  plaintext = ""
  for letter in ciphertext:
    plaintext += chr((ord(letter) - ord('A') + key) % 26 + ord('A'))
  print("plaintext: " + plaintext)
  print()