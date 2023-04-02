import classes
if __name__=='__main__':
    #t=input("do you wish to use space separated letters? (y/n)")
    t='n'
    e=classes.evaluator(t)
    while True:
        s=input().strip()
        if s.lower()=="stop":
            break
        print(e.eval(s))