for i in range(100):
  print("FizzBuzz" if (i+1) % 15 == 0 else "Fizz" if (i+1) % 3 == 0 else "Buzz" if (i+1) % 5 == 0 else (i+1))