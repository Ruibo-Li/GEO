import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
a_1 = (10 < 20) == (10 < 30)
b_1 = (10 < 20) == (10 < 30) == ("sdkfjasd" <= "sdfasd")
c_1 =  not ((10 < 20) == (10 < 30) == ("sdkfjasd" <= "sdfasd"))