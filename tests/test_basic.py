import basic 
import unittest

class ListTest(unittest.TestCase):

        
    def test_list(self):
        l = basic.LinkedList()
        s = 'aoeuhtns'
        for i in s:
            l.append(i)
        assert str(l) == ','.join(list(s)), print(str(l)) 
        assert str(l) == ','.join(list(s)), print(str(l)) 


if __name__ == '__main__':
    unittest.main()

