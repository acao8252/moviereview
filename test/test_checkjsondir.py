import os

def test():
    jsons = os.listdir('../json')
    if len(jsons) > 0:
        return True
    return False