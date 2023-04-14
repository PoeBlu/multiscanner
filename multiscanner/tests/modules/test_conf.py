"""
A test module which tests that config handling works
"""
TYPE = "Test"
NAME = "test_conf"
DEFAULTCONF = {'a': 'b', 'c': 'd'}


def check(conf=DEFAULTCONF):
    return True


def scan(filelist, conf=DEFAULTCONF):
    results = []

    metadata = {"Name": NAME, "Type": TYPE, 'conf': conf}
    return results, metadata
