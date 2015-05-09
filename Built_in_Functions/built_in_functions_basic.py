import random
# generate random number
def randomNum():
    return random.random()

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
    return ls[0]

def listSet(ls, i, x):
    ls[i] = x
    return None

# string operation functions
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


