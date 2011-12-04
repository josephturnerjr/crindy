import crindy
import time

def c0():
    print "c0 called at time %s" % (time.time(),)

def c1(a, b, c):
    print "c2 called at time %s with values %s %s %s" % (time.time(), a, b, c)
    crindy.add_event(1, c2, [666])

def c2(a):
    print "c2 called at time %s with value %s" % (time.time(), a)

if __name__ == "__main__":
    crindy.add_event(0, c0)
    crindy.add_event(2, c0)
    crindy.add_event(4, c0)
    crindy.add_event(1, c1, ["yes", "no", "maybe"])
    crindy.run()
