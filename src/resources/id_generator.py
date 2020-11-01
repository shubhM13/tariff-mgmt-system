import random

def generate(label):
    n = 4
    min = pow(10, n-1)
    max = pow(10, n) - 1
    id = label.upper() + str(random.randint(min, max))
    return id
