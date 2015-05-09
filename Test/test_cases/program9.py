import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
a_1 = "this is"
b_1 = " a"
c_1 = a_1 + b_1 + " test  "
printf(c_1)
printl(c_1)
l1_1 = split(c_1, " ")
d_1 = strip(c_1, " ")
printl(d_1)
e_1 = replaceString(c_1, "test", "Test")
printl(e_1)
f_1 = findSubstring(c_1, "test")
printl("Substring: " + str(f_1))
g_1 = "12344"
h_1 = isDigit(g_1)
i_1 = isUpper(c_1)
j_1 = isLower(c_1)
k_1 = lower(d_1)
printl(k_1)
l_1 = upper(c_1)
printl(l_1)
m_1 = []
listAppend(m_1, "hello")
listAppend(m_1, "world!")
n_1 = joinString(" ", m_1)
printl(n_1)