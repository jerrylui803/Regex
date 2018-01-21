"""
# Copyright Jerry Lui, Nick Cheng, Brian Harrington, Danny Heap, 2013, 2014,
# 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

def is_regex(s):
    '''(str) -> bool
    Given a string s, return True iff the s is a valid regex
    defination of regex:
    - 4 types of length 1 regex: "0", "1", "2", "e"
    - if r is valid regex, then r + "*" is valid regex
    - if a and b are regex, then '
    '(' + r* + '|' + r* + ')'
    '(' + r* + '.' + r* + ')'
    is_regex('2')
    >>> True
    is_regex('a')
    >>> False
    '''
    # The following code assumes everything is True, but everything must
    # satisfy def of regex, if anything fails, return False
    result = None
    # Base case
    if (len(s) <= 1):
        # if length is shorter equal to one, it must be one of the following
        # characters
        result = True if s in {"0", "1", "2", "e"} else False
    # if it starts with a bracket and ends with a breaket, then it must be
    # made up of s1 and s2, where s1 and s2 are valid regex
    elif s[0] == "(" and (s[-1] == ")"):
        # use helper function to find the operator that separates the two
        # regex
        operator_index = find_operator_index(s)
        # break it down into two regex, if both of them are valid regex, then
        # the current regex must also be valie regex
        result = is_regex(s[1:operator_index]
                          ) and is_regex(s[operator_index + 1:-1])
    # this is the third elif statement, because it is not as likely to happen
    # as the pervious if statements
    # this removes the * behind any string if exists, because star should only
    # be added on valid regex, removing it will not change the result of this
    # function
    elif (s[-1] == "*"):
        result = is_regex(s[:-1])
    # else, the string does not start and end with a bracket and does not end
    # with a star. According to def of redex, this is not a redex
    else:
        result = False
    return result


def find_operator_index(s):
    '''(str) -> int
    Find that operator that is in the middle of the string
    By middle of the string, it means every open brecket has a corresponding
    closed brecket before. ( and must not be the first index)
    REQ: s must be a valid regex
    find_operator_index("(1.1)")
    >>> 4
    find_operator_index("(0|(1.1))")
    >>> 2
    '''
    # find len of the str to later use it as an index check
    str_len = len(s)
    # initilize variables
    operator_index = 1
    operator = {"|", "."}
    open_bracket_count = 0
    # while the operator is not being found, keep going to find the operator
    while operator_index < str_len and s[operator_index] not in operator:
        # if an ope bracket is found, if it is a valid regex, there must be a
        # close bracket, the inside of the brackets does not matter.
        if s[operator_index] == "(":
            # go to the next index, and count the number of open bracket
            operator_index += 1
            open_bracket_count += 1
            # Note: number of open bracket must be the same as close brackets
            # if it is a valid regex
            # while the number of open bractet is not the same is close
            # brackets
            while operator_index < str_len and open_bracket_count != 0:
                # every open bracket must be paired with a close bracket
                if s[operator_index] == "(":
                    open_bracket_count += 1
                elif s[operator_index] == ")":
                    open_bracket_count -= 1
                # check next index
                operator_index += 1
            # minus one because when the loop exits, the accumulator is at
            # the end
            operator_index -= 1
        # check next index of the string
        operator_index += 1
    return operator_index

# dictionary for all_regex_permutations to
# not compute the permutation of the same string multiple times
mydict = dict(); 

def all_regex_permutations(s):
    '''(str) -> set()
    given a random string s, returns all the permutations of s that are
    valid regex (this is the inefficient version of all_regex_permutations)
    all_regex_permutations("(11|)")
    >>> {'(1|1)'}
    all_regex_permutations("(11|2.())")
    >>> {'((1.1)|2)', '(1|(1.2))', '(1.(2|1))', '(2.(1|1))', '((2|1).1)',
        '((1.2)|1)', '(2|(1.1))', '(1.(1|2))', '((1|2).1)', '(1|(2.1))',
        '((1|1).2)', '((2.1)|1)'}
    '''
    # this is the efficient version of all_regex_permutations
    # initilize variables
    all_possible_char = {'0', '1', '2', 'e', '*', '|', '(', ')', '.'}
    open_bracket = 0
    close_bracket = 0
    short_regex = ""
    operators = ""
    star_num = 0
    result = ""
    # put the string into the corresponding lists or counters
    for next_ele in s:
        if next_ele not in all_possible_char:
            result = set()
        elif next_ele == "(":
            open_bracket += 1
        elif next_ele == ")":
            close_bracket += 1
        elif next_ele == "*":
            star_num += 1
        elif next_ele in {"0", "1", "2", "e"}:
            short_regex += next_ele
        elif next_ele in {"|", "."}:
            operators += next_ele
    # if it is in one of the following conditions, then it is an empty set
    if open_bracket != close_bracket:
        result = set()
    if len(operators) != open_bracket:
        result = set()
    if len(short_regex) != len(operators) + 1:
        result = set()
    # Check if the input failed already, because if it did, there is no point
    # of doing the permutations and will be more efficient
    if result != set():
        short_regex_perms = perms(short_regex)
        operators_perms = perms(operators)
        result = set()
        n_regex = len(short_regex)
        brecket_perms = perms_for_breckets(open_bracket, 's'*n_regex, 'o'*(n_regex-1), star_num)
        # now it must valid, find all the perms of the operators and regex
        for next_regex in short_regex_perms:
            for next_operator in operators_perms:
                for next_brecket in brecket_perms:
                    counter_regex = 0
                    counter_operator = 0
                    result_word = ''
                    for next_letter in next_brecket:
                        if next_letter == 's':
                            curr = next_regex[counter_regex]
                            counter_regex += 1
                        elif next_letter == 'o':
                            curr = next_operator[counter_operator]
                            counter_operator += 1
                        else:
                            curr = next_letter
                        result_word = result_word + curr
                    result.add(result_word)
    return result

def all_regex_permutations_ineff(s):
    '''(str) -> set()
    given a random string s, returns all the permutations of s that are
    valid regex (this is the inefficient version of all_regex_permutations)
    all_regex_permutations("(11|)")
    >>> {'(1|1)'}
    all_regex_permutations("(11|2.())")
    >>> {'((1.1)|2)', '(1|(1.2))', '(1.(2|1))', '(2.(1|1))', '((2|1).1)',
        '((1.2)|1)', '(2|(1.1))', '(1.(1|2))', '((1|2).1)', '(1|(2.1))',
        '((1|1).2)', '((2.1)|1)'}
    '''
    # this is the inefficient version of all_regex_permutations
    result = perms(s)
    remove_list = []
    for ele in result:
        if not is_regex(ele):
            remove_list.append(ele)
    for nex in remove_list:
        result.remove(nex)
    return result    


def perms_for_breckets(brecket_num, regex, operator, star_num):
    '''
    Helper function for all_regex_permutations
    Given a specific number of breckets, simple regex, operator, and number of
    stars, return all the possible permutations the regex by only rearranging
    the placements of the breckets and the stars. But leave the order of the
    simple regex and operators unchanged (It means the order of them occuring
    in the string).
    simple regex means the regex string is in the set of:
    {"0", "1", "2", "e"}
    operator means the operator string is in the set of:
    {"|", "."}
    perms_for_breckets(1,"12",".",2)
    >>> {'(1.2)**', '(1.2*)*', '(1*.2*)', '(1.2**)', '(1**.2)', '(1*.2)*'}
    perms_for_breckets(2,"123",".|",0)
    >>>{'((1.2)|3)', '(1.(2|3))'}
    '''
    key = str(brecket_num) + '#' + str(regex) + '#' + str(operator) + '#' + str(star_num) 
    if (key not in mydict):
        #print("the key is " , key, " and it is not in the dict")
        # initialize
        result = set()
        # Base Case, when there are no breckets, return the only regex character
        # left, alone with the number of stars since all stars must be included
        # in the permutation
        if brecket_num == 0:
            result = {regex[0] + "*" * star_num}
        # When the number of breckets is more than 0
        else:
            result1 = set()
            result2 = set()
            # The for loops are setup in a way such that star_count1, star_count1
            # ,and star_count3 will always have a sum of star_num, and it includes
            # all the combinations of getting that sum.
            # This will get all the combination of the stars' placement
            for star_count in range(star_num + 1):
                for star_count2 in range(star_num + 1 - star_count):
                    star_count3 = star_num - star_count - star_count2
                    # The case where the first part (one character before the end
                    # of the string) is a regex with breckets, find all the
                    # permutation of the breckets with this unique regex and
                    # operator order.
                    # the operator will be the first characterin the operator
                    # string. (because REQ)
                    for perm in perms_for_breckets(brecket_num - 1,
                                                   regex[:-1], operator[:-1],
                                                   star_count):
        
                        result1 = result1 | {"(" + perm + operator[-1] +
                                             regex[-1] + "*" * star_count3 +
                                             ")" + "*" * star_count2}
                    # Same as above, except:
                    # The case where the last part (everything except the first
                    # character of the string) is a regex with breckets, and the
                    # rest is just an one character regex string
                    for perm in perms_for_breckets(brecket_num - 1, regex[1:],
                                                   operator[1:], star_count):
                        result2 = result2 | {"(" + regex[0] + "*" * star_count3 +
                                             operator[0] + perm + ")" +
                                             "*" * star_count2}
            # Merge the 2 cases and return
            result = result1 | result2
        mydict[key] = result
        return result
    else:
        #print("I have the key !!! ", key)
        return mydict[key]

# dictionary for perms to not compute the permutation of the same string 
# multiple times
mydict2 = dict()

def perms(s):
    '''
    (str) -> set of str
    Return the set of all permutations of the string s.
    >>> actual = perms('abc')
    >>> actual == {'cba', 'bca', 'acb', 'abc', 'cab', 'bac'}
    '''
    if (s not in mydict2):
        # base case, returns nothing
        if len(s) == 0:
            return {''}
        result = set()
        # moving around the first letter to find all the perms
        for i in range(len(s)):
            # for each perm for each leading term
            for perm in perms(s[:i] + s[i+1:]):
                # append
                result.add(s[i] + perm)
        mydict2[s] = result
        return result
    else:
        return mydict2[s]

def regex_match(r, s):
    '''(regexTree, str) -> bool
    returns True iff the string matches the regex tree rooted at r
    REQ: r must be a valid root of regex tree
    a = build_regex_tree("(2|(2.1))*")
    regex_match(a, "221")
    >>> True
    a = build_regex_tree("(0|(2.1))*")
    regex_match(a, "221")
    >>> False
    '''
    # initialize the variables
    result = False
    children = r.get_children()
    # If no more children
    if children == []:
        # get the current symbol and compare to the string to see if its
        # valid
        r_symbol = r.get_symbol()
        if r_symbol == "e":
            return s == ""
        else:
            return r_symbol == s
    # If 1 child, must be star
    elif len(children) == 1:
        len_s = len(s)
        # if length is 0
        # then True
        if len_s == 0:
            result = True
        # If the length if the string is one, then compare the string
        # to the children
        elif len_s == 1:
            result = regex_match(children[0], s)
        # else: find all the combinations of serperating the string
        # into pieces such that the overall string is a valid regex
        else:
            ed_index = 1
            st_index = 0
            result_list = []
            # while not end of string, and not out of index
            while s != "" and ed_index < len(s) + 1:
                # break the string into pieces and then check if the indiviual
                # strings are valid regex
                result = regex_match(children[0], s[st_index:ed_index])
                # if it is valid regex and not the end of string, move the
                # index pointers to check for the next valid regex
                if result and s[ed_index:] != "":
                    # at the same time, although the last part of the string
                    # is valid, maybe including the next part of the string
                    # would still be valie, the next line is check that.
                    result_list.append(regex_match(children[0],
                                       s[st_index:ed_index + 1]))
                    # move the pointers to check the next range of index
                    st_index = ed_index
                    result = False
                # check next index
                ed_index += 1
            # if the result is already True, or there is one single True in
            # all the perms of the result list. Then it means there is at least
            # one combination that the string matches the regex
            if result or True in result_list:
                result = True
    # Else, must be 2 child if valid tree
    else:
        root_symbol = r.get_symbol()
        # if "|" then it is either left child or right children
        if (root_symbol == "|"):
            result = (regex_match(children[0], s) or
                      regex_match(children[1], s))
        # if "." then both sides must be true
        elif (root_symbol == "."):
            index = 0
            # do a loop to find all the possible ways to break down the
            # string while within the range
            # If result ever returns true, exit the loop right away
            while index <= len(s) and not result:
                # break down the string and return true when both side are
                # true
                result = (regex_match(children[0], s[:index]) and
                          regex_match(children[1], s[index:]))
                # next index
                index += 1
    return result

def build_regex_tree(regex):
    '''(str) -> RegexTree
    input a valid regex and output a regextree for it. then return the
    root of the tree
    REQ: regex is a valid regex
    build_regex_tree("(2|(2.1))*")
    >>>StarTree(BarTree(Leaf('2'), DotTree(Leaf('2'), Leaf('1')))).
    build_regex_tree("(0.1)*")
    >>>StarTree(DotTree(Leaf('0'), Leaf('1')))
    '''
    result = None
    # Base case
    if (len(regex) <= 1):
        # if length is shorter equal to one, it must be one of the following
        # characters
        result = Leaf(regex)
    # if it starts with a bracket and ends with a breaket, then it must be
    # made up of s1 and s2, where s1 and s2 are valid regex
    elif regex[0] == "(" and (regex[-1] == ")"):
        # use helper function to find the operator that separates the two
        # regex
        operator_index = find_operator_index(regex)
        operator = regex[operator_index]
        if operator == "|":
            result = BarTree(build_regex_tree(regex[1:operator_index]),
                             build_regex_tree(regex[operator_index+1:-1]))
        elif operator == ".":
            result = DotTree(build_regex_tree(regex[1:operator_index]),
                             build_regex_tree(regex[operator_index+1:-1]))
    # this is the third elif statement, because it is not as likely to happen
    # as the pervious if statements
    # this removes the * behind any string if exists, because star should only
    # be added on valid regex, removing it will not change the result of this
    # function
    elif (regex[-1] == "*"):
        result = StarTree(build_regex_tree(regex[:-1]))
    # else, the string does not start and end with a bracket and does not end
    # with a star. According to def of redex, this is not a redex
    return result

if __name__ == '__main__':
    print("(1.(1|2)*)** is_regex: " + str(is_regex("(1.(1|2)*)**")))
    print("(1.**(122)*)** is_regex: " + str(is_regex("(1.**(122)*)**")))
    print()
    print("All valid regex permutations of (1|2.()): ")
    print(all_regex_permutations("(1|2.(e))"))
    print()
    print("build_regex_tree(\"(2|(2.1))*\") will give you: ")
    print(build_regex_tree("(2|(2.1))*"))
    print()
    print("and you can use the regex tree we just built to regex match:")
    print("regex_match(build_regex_tree(\"(2|(2.1))*\"), \"221\") " + 
          "will give you: " + 
          str(regex_match(build_regex_tree("(2|(2.1))*"), "221")))
    
    print("Note that you can run all_regex_permutations on much longer " + 
          "strings upto 30 characters, and if the strings contains " +
          "duplicates, it will run reasonably fast upto 50 characters\n" +
          "Uncomment the following lines to see result")
    #print(all_regex_permutations("(1.1)().1().1()()().2()...111*"))
    #print(all_regex_permutations("(1.1)().1().1()()().2()...1112|()"))
    #print(all_regex_permutations("(1|1)()|1()|1()()()|1()|||1111|()|||111((()))||11()()|1()"))
