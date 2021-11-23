import os

def test():
    numOfJSONs = len(os.listdir('../json'))
    os.chdir("..")
    os.system("python3 manager.py")
    print(len(os.listdir('json')))
    if (numOfJSONs + 1 == len(os.listdir('json'))):
        return True
    else:
        return False
