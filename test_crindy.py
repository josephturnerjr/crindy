import unittest
from crindy import EventScheduler


class TestEventScheduler(unittest.TestCase):
    def setUp(self):
        pass

    def mock_sleep(self, sleep_time):
        self.last_sleep = sleep_time

    def mock_callable(self, *args):
        self.last_args = args

    def test_sleep_func(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        a.add_event(5, lambda: None)
        a.run_next_set()
        self.assertTrue(self.last_sleep == 5)

    def test_len(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertTrue(len(a) == 0)
        a.add_event(5, lambda: None)
        self.assertTrue(len(a) == 1)
        a.run_next_set()
        self.assertTrue(len(a) == 0)

    def test_bool(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertFalse(a)
        a.add_event(5, lambda: None)
        self.assertTrue(a)
        a.run_next_set()
        self.assertFalse(a)

    def test_clear(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertTrue(len(a) == 0)
        a.clear()
        self.assertTrue(len(a) == 0)
        a.add_event(5, lambda: None)
        self.assertTrue(len(a) == 1)
        a.clear()
        self.assertTrue(len(a) == 0)

    def test_clear_tagged(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertTrue(len(a) == 0)
        a.clear_tagged(None)
        self.assertTrue(len(a) == 0)
        a.add_event(5, lambda: None)
        a.add_event(5, lambda: None)
        a.add_event(5, lambda: None)
        a.add_event(5, lambda: None)
        self.assertTrue(len(a) == 4)
        a.clear_tagged(None)
        self.assertTrue(len(a) == 0)
        a.add_event(5, lambda: None, tag=1)
        a.add_event(5, lambda: None, tag=1)
        a.add_event(5, lambda: None)
        a.add_event(5, lambda: None)
        self.assertTrue(len(a) == 4)
        a.clear_tagged(None)
        self.assertTrue(len(a) == 2)
        a.clear_tagged(1)
        self.assertTrue(len(a) == 0)

    def test_add_event(self):
        a = EventScheduler(sleep_func=self.mock_sleep)
        a.add_event(5, self.mock_callable)
        a.add_event(6, self.mock_callable, [1, 2, 3])
        a.add_event(1, self.mock_callable, [1, 2, 3, 4])
        a.run_next_set()
        self.assertTrue(len(self.last_args) == 4)
        a.run_next_set()
        self.assertTrue(len(self.last_args) == 0)
        a.run_next_set()
        self.assertTrue(len(self.last_args) == 3)

    def test_run_next(self):
        # Insertion order should be preserved (STABLE SORT SON)
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertTrue(None == a.run_next())
        a.add_event(6, self.mock_callable, [1, 2, 3])
        a.add_event(6, self.mock_callable)
        a.add_event(5, self.mock_callable)
        a.add_event(5, self.mock_callable, [1, 2, 3])
        a.run_next()
        self.assertTrue(len(self.last_args) == 0)
        a.run_next()
        self.assertTrue(len(self.last_args) == 3)
        a.run_next()
        self.assertTrue(len(self.last_args) == 3)
        a.run_next()
        self.assertTrue(len(self.last_args) == 0)

    def test_run_set(self):
        # Insertion order should be preserved (STABLE SORT SON)
        a = EventScheduler(sleep_func=self.mock_sleep)
        self.assertTrue(None == a.run_next())
        a.add_event(6, self.mock_callable)
        a.add_event(5, self.mock_callable)
        a.add_event(5, self.mock_callable, [1, 2, 3])
        ret = a.run_next_set()
        self.assertTrue(len(ret) == 2)
        self.assertTrue(len(self.last_args) == 3)
        ret = a.run_next_set()
        self.assertTrue(len(ret) == 1)
        self.assertTrue(len(self.last_args) == 0)

if __name__ == "__main__":
    unittest.main()
