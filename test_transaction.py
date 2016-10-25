import unittest

from atx import Transaction


class CA:
    def do(self):
        print("CA do")
        return True

    @staticmethod
    def sss():
        print("SSS")
        return True

def A(a,b):
    print("A",a,b)
    return True


def undo_A():
    print('undo A')
    return True


def B():
    print('B')
    return True


def undo_B():
    print("undo B")
    return True


tr = Transaction.Transaction()
ca = CA()
tr.add(CA.sss, ())
tr.add(ca.do)
tr.add(A, (1,2), undo_A, ())
tr.add(B, (), undo_B)
if tr.commit() == Transaction.PASS:
    tr.rollback()
else:
    print("Fail")
