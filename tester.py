from importlib import import_module
import os

def tester():
    # get list() of test files in test dir
    tests = sorted(os.listdir('test'), reverse=True)

    passed_tests = list()
    failed_tests = list()
    # import each test file in test dir and run
    for test_file in tests:
        # remove the extension
        if not test_file.startswith('test_'):
            continue

        test_file = test_file.replace('.py', '')
        print(f'Testing: {test_file}')

        # e.g. import test.test_webconnection.py
        passed_test = import_module(f'test.{test_file}').test()
        if passed_test:
            passed_tests.append(test_file)
        else:
            failed_tests.append(test_file)

    if passed_tests:
        print(f'{len(passed_tests)} Test(s) Passed:')
        for test in passed_tests:
            print(test)

    if failed_tests:
        num_failed = len(failed_tests)
        print(f'{len(failed_tests)} Test(s) Failed:')
        for test in failed_tests:
            print(test)

if __name__ == '__main__':
    tester()
