import os, sys, typing

from typing import List

SANCTIONED_THRESHOLD_PERCENTAGE = 0.75

def distance(s_a:str ,s_b:str)->float:
    '''Calculates distance between both strings based on how far off one is from the other.'''
    if  s_a == None:
        raise ValueError("First argument provided was None!")
    
    if  s_b == None:
        raise ValueError("Second argument provided was None!")
    
    if s_a == s_b:
        return 0.0

    # if len(s_a) == 0 or len(s_b) == 0:
    #     return max(len(s_a), len(s_b))

    if len(s_a) == 0:

        if len(s_b) == 0:
            return len(s_b)
        else:
            return 1

    if len(s_b) == 0:

        if len(s_a) == 0:
            return len(s_a)
        else:
            return 1
    
    
    

    weight_b = [0 for i in range(len(s_b) +1)] 
    weight_a = [ i for i in range(len(s_b)+1)]

    for i in range(len(s_a)):

        weight_b[0] = i+1

        for j in range(len(s_b)):
            cost = 1

            if s_a[i] == s_b[j]:
                cost = 0
            
            weight_b[j+1] = min(weight_b[j]+1 , weight_a[j+1]+1 , weight_a[j]+ cost)
        weight_a , weight_b = weight_b, weight_a

    return weight_a[len(s_b)]

def distance_help(s_a:str, s_b:str)-> float:
    
    if s_a == None:
        raise ValueError("First argument provided was None!")
    
    if s_b == None:
        raise ValueError("Second argument provided was None!")
    
    if s_a == s_b:
        if s_a == '' and s_b == '':
            return 0.0
        max_len = max(len(s_a), len(s_b))

        if max_len == 0:
            return 1.0

        return 0.0

    max_len = max(len(s_a), len(s_b))

    if max_len == 0:
        return 1.0

    return distance(s_a,s_b) / max_len

#1.0 ~ 100%
def str_similarity(s_a:str,s_b:str)->float:
    '''Returns a value in the range [0,1] representing the decimal percentage of similarity between both strings.
        Wherein a 1 indicates a perfect match between both arguments, and a 0 no correlation.'''
    return 1.0 - distance_help(s_a,s_b)

def sanctioned_names():
    '''Opens a connection to internal Sanctioned entities database.
        Returns a Generator object referencing a view of the database with read only priviliges.'''
    # try:
    with open('sanctioned_parties.txt','r') as sanctioned:

        for line in sanctioned:

            yield line
    # raise Exception as e:
    #     print(e)


def sanction_list_probability(name:str, sanctioned_names:List[str]=[])->float:
    '''Determines if the provided name argument, or any variant, is found within the sanctioned database.
        Returns a similarity probability in the range of [0,1].'''
    
    match_from_list = ''
    similarity = 0.0

    for nam in sanctioned_names:
        if str_similarity(name, nam) > similarity:
            similarity = str_similarity(name, nam)

    return similarity

def is_sanctioned(name:str, sanctioned_names=sanctioned_names()):
    '''Verifies if provided name argument is inside the sanction list database or resembles any inside it.
        Returns a tuple with types Bool[sanction status],Float[probability]'''
    
    sanc_prob = sanction_list_probability(name, sanctioned_names)
    
    if sanc_prob >= SANCTIONED_THRESHOLD_PERCENTAGE:
        return True, sanc_prob

    return  False, sanc_prob


# def debug():
#     '''Main input loop for verifying if provided argument is sanctioned or not.'''
    
#     input_ln =''
#     while True and input_ln.lower().strip() != 'quit':

#         input_ln = input('\nEnter name to view if sanctioned(\'quit\' to exit shell):').strip()

#         if input_ln and input_ln !='quit':
#             cl_input = input_ln[:].lower()# done to avoid modifying OG string
#             if is_sanctioned(name=cl_input)[0]:
#                 print(f'[!]HIT:{input_ln} with percentage {is_sanctioned(name=cl_input)[1]}\n')
#             else:
#                 print(f'No Hit:{input_ln} with percentage {is_sanctioned(name=cl_input)[1]}\n')
#     return

# if __name__ == "__main__":
#     debug()