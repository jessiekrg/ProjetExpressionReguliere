from automate import *
a1 = concatenation(etoile(union(automate("a"),automate("b"))),automate("c"))
a2 = union(concatenation(etoile(automate("a")),automate("c")),concatenation(etoile(automate("b")),automate("c")))
if egal(a1,a2):
    print('EGAL')
else:
    print('NON EGAL')
