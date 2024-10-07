import random
import math

def estimate_pi(precision):
  n_hits = 0
  n_miss = 0
  latest_pi = 3
  while True:
    x = random.random()
    y = random.random()
    dist_center = math.sqrt((0.5 - x)**2 + (0.5 - y)**2)
    in_circle = True if dist_center < 0.5 else False
    if in_circle: n_hits += 1
    else: n_miss += 1
    latest_pi = (n_hits/(n_hits+n_miss))*4
    if len(str(latest_pi).split(".")[1]) == precision: return latest_pi

print(estimate_pi(5))