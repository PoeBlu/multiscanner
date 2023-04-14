"""
A test module which requires no config and the result is the filename
"""
TYPE = "Test"
NAME = "test_1"


def check():
    return True


def scan(filelist):
    results = [(fname, fname) for fname in filelist]
    metadata = {"Name": NAME, "Type": TYPE, "Include": False}
    return results, metadata
