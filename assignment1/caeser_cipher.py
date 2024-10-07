alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def break_cipher(text):
  vowel_sum = 5*text.count("E") + 4*text.count("T") + 3*text.count("A") + 2*text.count("O") + text.count("I")
  output = text
  text = list(text)
  for i in range(1, 26):
    new_text = text
    for n in range(len(new_text)):
      if alphabet.index(new_text[n]) + 1 > 25: new_text[n] = alphabet[(alphabet.index(text[n]) + 1) - 26]
      else: new_text[n] = alphabet[alphabet.index(new_text[n]) + 1]
    new_sum = 5*new_text.count("E") + 4*new_text.count("T") + 3*new_text.count("A") + 2*new_text.count("O") + new_text.count("I")
    if new_sum > vowel_sum:
      vowel_sum = new_sum
      output = "".join(new_text)
  return (output)

print(break_cipher("GOODBYE"))