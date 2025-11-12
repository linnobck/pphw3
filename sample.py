import random

def sample(items, number, rate=0.2):

    '''
    Inputs: items is any type of iterable. It may be any type of iterable, including a generator.
            number is a number of items to collect for the sample.
            rate is a floating point number indicating the sample rate.
    
    The function observes items one at a time from items, with a rate probability of returning any given item. (By default: 20%)

    Output: Function ceases once number items have been returned.
    '''
    # counter for number of items collected so far
    count = 0

    # used to see if I need the special case code to pass tests
    # if 0 items are requested, exit
    #if number <= 0 or rate <= 0:
    #    return

    # loop through all items
    for i in items:
        if count == number:
            break
        # 'apply' sample rate 
        if random.random() < rate:
            yield i
            count += 1



