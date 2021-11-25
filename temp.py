import asyncio
from threading import Thread
import time

def abc():
    print("Run..")
    time.sleep(1)
    print("Done")

async def b():
    a = Thread(target=abc, args=[], group=None)
    b = Thread(target=abc, args=[], group=None)
    c = Thread(target=abc, args=[], group=None)
    d = Thread(target=abc, args=[], group=None)
    e = Thread(target=abc, args=[], group=None)
    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    a.join()
    b.join()
    c.join()
    d.join()
    e.join()



asyncio.run(b())