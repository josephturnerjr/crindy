import time

class EventScheduler(object):
    def __init__(self, sleep_func = time.sleep):
        self.sleep_func = sleep_func
        self._queue = []

    def __len__(self):
        return len(self._queue)

    def clear(self):
        self._queue = []

    def clear_tagged(self, tag):
        self._queue = filter(lambda x: x[3] != tag, self._queue)

    def add_event(self, timeout_secs, to_call, args=[], tag=None):
        self._queue.append([timeout_secs, to_call, args, tag])
        self._queue.sort(key=lambda x: x[0])

    def sleep_til_next(self):
        """
        Sleeps until the next callback is ready
        """
        if not self._queue:
            return
        sleep_time = self._queue[0][0]
        self.sleep_func(sleep_time)
        for item in self._queue:
            item[0] -= sleep_time

    def run_next(self):
        """
        Sleeps as needed then runs exactly one callback        
        """
        if not self._queue:
            return None
        self.sleep_til_next()
        # Call the item
        item = self._queue[0]
        res = item[1](*item[2])
        # Remove items from the queue
        del self._queue[:1]
        return res

    def run_next_set(self):
        """
        Sleeps as needed then runs all of the next set of callable objects,
        i.e. all of the ones with time 0 after the sleep
        """
        if not self._queue:
            return None
        self.sleep_til_next()
        to_run = filter(lambda x: x[0] <= 0, self._queue)
        res = []
        for item in to_run:
            # Call the item and append to results set
            res.append(item[1](*item[2]))
        # Remove items from the queue
        del self._queue[:len(to_run)]
        return res

    def run(self):
        while self:
            self.run_next_set()

_scheduler = EventScheduler()

def set_default_scheduler(sched):
    _scheduler = sched

def clear():
    _scheduler.clear()

def clear_tagged(tag):
    _scheduler.clear_tagged(tag)

def add_event(timeout_secs, to_call, args=[], tag=None):
    _scheduler.add_event(timeout_secs, to_call, args, tag)

def run():
    _scheduler.run()

