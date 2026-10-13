import basic 
import unittest

class ListTest(unittest.TestCase):

    def test_list(self):
        l = basic.LinkedList()
        s = 'aoeuhtns'
        for i in s:
            l.append(i)
        assert str(l) == ','.join(list(s)), print(str(l)) 
        assert l[3] == 'u', l[3]
        l.remove(3)
        assert l[3] == 'h', l[3]
        assert len(l) == 7
        assert str(l) == ','.join(list('aoehtns')), print(str(l)) 
        assert l[-1] == 's',( l[-1], str(l))

    def test_dl(self):
        l = basic.DoublyLinkedList()
        s = 'aoeuhtns'
        for i in s:
            l.append(i)
        assert str(l) == ','.join(list(s)), str(l) 
        assert l[3] == 'u', l[3]
        l.remove(3)
        assert l[3] == 'h', l[3]
        assert len(l) == 7
        assert str(l) == ','.join(list('aoehtns')), str(l) 
        assert l[-1] == 's',( l[-1], str(l))

    def test_deque(self):
        l = basic.Deque()
        s = 'aoeuhtns'
        for i in s:
            l.append(i)
        for i in s:
            l.appendleft(i)


        assert str(l) == ','.join([*reversed(s),*s]), str(l)
        assert l[3] == 'h', l[3]
        l.remove(3)
        assert l[3] == 'u', l[3]
        assert len(l) == 15
        assert str(l) == ','.join([*reversed('aoeutns'),*s]), str(l)



if __name__ == '__main__':
    unittest.main()

