import random
# generate random number


def randomNum():
    return random.random()


def randomInt(min, max):
    return random.randint(min, max)


# list operation functions
def createList():
    return list()


def listAppend(ls, x):
    ls.append(x)
    return None


def listExtend(ls1, ls2):
    ls1.extend(ls2)
    return None


def listInsert(ls, i, x):
    ls.insert(i, x)
    return None


def listRemove(ls, x):
    ls.remove(x)
    return None


def listPop(ls, i=0):
    return ls.pop(i)


def listIndex(ls, x):
    return ls.index(x)


def listCount(ls, x):
    return ls.count(x)


def listSort(ls):
    ls.sort()
    return None


def listReverse(ls):
    ls.reverse()
    return None


def listGet(ls, i):
    return ls[i]


def listSet(ls, i, x):
    ls[i] = x
    return None


def printf(st):
    print st,
    return None


def printl(st):
    print st
    return None


def split(st, sep=' '):
    return st.split(sep)


def strip(st, sep=' '):
    return st.strip(sep)


def replaceString(st, old, new):
    return st.replace(old, new)


def findSubstring(st, sub):
    return st.find(sub)


def encode(st, encoding):
    return st.encode(encoding)


def index(st, sub):
    return st.index(sub)


def isDigit(st):
    return st.isdigit()


def isUpper(st):
    return st.isupper()


def isLower(st):
    return st.islower()


def lower(st):
    return st.lower()


def upper(st):
    return st.upper()


def joinString(sep, iterable):
    return sep.join(iterable)


def partition(st, sep):
    return st.partition(sep)


def isNumeric(st):
    return st.isnumeric()


def isDecimal(st):
    return st.isdecimal()


def RGB2Str(r, g, b):
    s1 = str(hex(r))[2:].upper()
    if len(s1) == 1:
        s1 = '0' + s1
    s2 = str(hex(g))[2:].upper()
    if len(s2) == 1:
        s2 = '0' + s2
    s3 = str(hex(b))[2:].upper()
    if len(s3) == 1:
        s3 = '0' + s3
    return s1 + s2 + s3


def getR(str):
    v1 = ord(str[0])
    if not 48 <= v1 <= 57:
        v1 -= 55
    else:
        v1 -= 48
    v2 = ord(str[1])
    if not 48 <= v2 <= 57:
        v2 -= 55
    else:
        v2 -= 48
    return v1 * 16 + v2


def getG(str):
    v1 = ord(str[2])
    if not 48 <= v1 <= 57:
        v1 -= 55
    else:
        v1 -= 48
    v2 = ord(str[3])
    if not 48 <= v2 <= 57:
        v2 -= 55
    else:
        v2 -= 48
    return v1 * 16 + v2


def getB(str):
    v1 = ord(str[4])
    if not 48 <= v1 <= 57:
        v1 -= 55
    else:
        v1 -= 48
    v2 = ord(str[5])
    if not 48 <= v2 <= 57:
        v2 -= 55
    else:
        v2 -= 48
    return v1 * 16 + v2