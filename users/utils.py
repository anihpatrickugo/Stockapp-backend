import random
import math


# this generates a 6 digit code on registration
def generate_activation_code():
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

    ## initializing a string
    random_str = ""

    ## we can generate any lenght of string we want
    for i in range(6):
    ## generating a random index
    ## if we multiply with 10 it will generate a number between 0 and 10 not including 10
    ## multiply the random.random() with length of your base list or str
      index = math.floor(random.random() * 10)

      random_str += str(digits[index])

    ## displaying the random string
    return(random_str)