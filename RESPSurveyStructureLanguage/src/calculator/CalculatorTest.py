'''
Created on Jul 7, 2016

@author: ei-student
'''

def _evaluate(math_string, scope=globals()):
    """
    Evaluates math_string with access to variables in scope
    
    :param math_string: string containing math with rules:
        -values and operators are separated by spaces with 
            the exception of brackets and variable signs
        -evaluates to a single value
        -only uses the following operators (separated by order of ops):
            ( ... ) traditional parentheses
            | ... |  absolute value brackets
            
            +x, -x  variable signs
            
            x ^ y  powers
            
            x * y  multiplication
            x / y  division
            x // y  integer division    # only yield integers
            x % y  modulo function
            
            x + y  addition
            x - y  subtraction
            
            # only yield booleans
            x > y  greater than
            x >= y  greater than or equal to
            x == y  compares if equal
            x <= y  less than or equal to
            x < y  less than
            
            # can only apply to booleans
            not x  logical NOT
            x and y  logical AND
        -reserves keywords:
            not
            and
            or
            true
            false
    
    :param scope: dictionary of variables which mathString can access
    :return: returns numerical or boolean value of evaluated string
    """
    math_list = math_string.split(" ")
    print(math_list)
    
    new_list = []
    for i in range(0, len(math_list)):
        # TODO transform string into list of terms
        pass

if __name__ == '__main__':
    math_str = "8 * |-var + 4| % 3 >= 0 and var ^ 2 == 36"
    scp = {"var" : 6}
    
    # Should yield True
    print(_evaluate(math_str, scp))