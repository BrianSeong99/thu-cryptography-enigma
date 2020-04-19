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