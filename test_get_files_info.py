# calculator/tests.py

import unittest
from functions.get_files_info import get_files_info

class TestFileInfo(unittest.TestCase):
    def test_Period(self):
        result = get_files_info("calculator", ".")
        print("Result for current directory:")
        print(result)
    
    def test_Pkg(self):
        result = get_files_info("calculator", "pkg")
        print("Result for 'pkg' directory:")
        print(result)
    
    def test_Bin(self):
        result = get_files_info("calculator", "/bin")
        print("Result for '/bin' directory:")
        print(result)

    def test_PeriodPeriodBackSlash(self):
        result = get_files_info("calculator", "../")
        print("Result for '../' directory:")
        print(result)

if __name__ == "__main__":
    unittest.main()