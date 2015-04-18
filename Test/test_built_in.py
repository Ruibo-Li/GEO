from Built_in_Functions.built_in_functions import *


def main():
    Window(100, 100)


def test(name, module, function_name, input, output):
    methodToCall = getattr(module, function_name)