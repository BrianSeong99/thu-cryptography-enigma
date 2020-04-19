from collections import defaultdict

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ciphertext = 'KQEREJEBCPPCJCRKIEACUZBKRVPKRBCIBQCARBJCVECUPKRIOFKPACUZQEPBKRXPEIIEABDKPBCPFCDCCAFIEABDKPBCPFEQPKAZBKRHAIBKAPCCIBURCCDKDCCJCIDFUIXPAFFERBICZDFKABICBBENEFCUPJCVKABPCYDCCDPKBCOCPERKIVKSCPICBRKIJPKABI'

frequency = defaultdict(int)

for letter in ciphertext:
  frequency[letter] += 1

print("FREQUENCY STATS:")
for letter in alphabet:
  print(letter + ": " + str(frequency[letter]), end="\t")
print()