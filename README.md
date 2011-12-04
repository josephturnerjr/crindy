# Crindy: dead-simple eventloop programming for Python

Crindy was born out of my frustration with trying to write applications 
in Python that have several timer-based loops running at different 
frequencies. My initial approach used Python threads, but that approach 
is nasty for a number of reasons, the most pertinent being that these
eventloops aren't really doing any concurrent processing other that
sleeping and that there is no mechanism for killing threads. Even if 
there were, there isn't a good, Pythonic equivalent of destructors, so 
I was left propagating kill flags to all of the encapsulated threads. 
Blech.

Enter crindy. Crindy exposes a simple interface similar to Javascript's
setTimeout call and has a built-in message pump. As a result, creating 
applications with crindy is similar to creation applications in node.js:
when modules are created, they register their first timeout and
callback, which then registers other callbacks as appropriate. When the
message pump runs dry, the application is over.

## Stupid example

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

This will output the following:

    c0 called at time 1323020603.55
    c2 called at time 1323020604.55 with values yes no maybe
    c0 called at time 1323020605.55
    c2 called at time 1323020605.55 with value 666
    c0 called at time 1323020607.56
