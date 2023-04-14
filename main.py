import time
from threading import Thread

# class worker(Thread):
#     def run(self):
#         for x in range(0,11):
#             print(x)
#             time.sleep(1)
#
# class waiter(Thread):
#     def run(self):
#         for x in range(100,103):
#             print(x)
#             time.sleep(5)
#
# worker().start()
# waiter().start()

def foo():
    for _ in range(5):
        time.sleep(2)
        print('foo')


def bar():
    for _ in range(5):
        time.sleep(3)
        print('bar')

t1 = Thread(target=bar)
t2 = Thread(target=foo)

t1.start()
t2.start()