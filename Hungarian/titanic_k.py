import random


surviveStatus = False

while (surviveStatus == False):

    x = random.randint(1,2200)

    if x <= 700:
        print('You survived')
        surviveStatus = True
    else:
        print('You died')
        
