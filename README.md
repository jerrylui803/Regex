# Regex
This is a project I completed in 2016 about regular expressions in python.

This is a stripped-down simplied regular expression form that contains all the essential principles.
The alphabet is {0, 1, 2} and we have the following operators/symbols:
’e’ 
’|’ bar
’.’ dot
’*’ star
’(’ left parenthesis, or left
’)’ right parenthesis, or right

and it contains the following functions:

is_regex(s): which takes a string s and produces True if it is a valid regular expression (according
to the characterization in the introduction of this handout), but False otherwise.

all_regex permutations(s): which takes a string s and produces the set of permutations of s
that are also valid regular expressions (according to the characterization in the introduction
of this handout)

regex_match(r, s): which returns True if and only if string s matches the regular expression
tree rooted at r.

build_regex_tree(regex): which takes a valid regular expression string regex, builds the corresponding
regular expression tree, and returns its root.


If it is still not clear, there are detailed documentations in the code
