# Group #: B42
# Student names: Saranga Varma, Mfon Mkono

import threading
import queue
import time
import random

# config
NUM_P = 4
NUM_C = 5
ITEMS_PER_P = 5

# timing
PROD_RATE = (0.1, 0.4)
CON_RATE = (0.1, 0.5)

# sentinel value
STOP = None

def consumerWorker (queue):
    """target worker for a consumer thread"""
    while True:
        job = queue.get()
        
        if job is STOP:
            print(f"{threading.current_thread().name} shutting down")
            queue.task_done()
            break

        # simulate work
        print(f"{threading.current_thread().name} handled {job}")
        time.sleep(random.uniform(*CON_RATE))
        queue.task_done()

def producerWorker(queue):
    """target worker for a producer thread"""
    for i in range(1, ITEMS_PER_P + 1):
        thing = f"{threading.current_thread().name}-Item{i}"
        queue.put(thing)
        print(f"{threading.current_thread().name} created {thing}")
        time.sleep(random.uniform(*PROD_RATE))



if __name__ == "__main__":
    
    # shared buffer
    buffer = queue.Queue()
    producers = []
    consumers = []

    # consumers first so they are ready
    for i in range(NUM_C):
        t = threading.Thread(target=consumerWorker,
                             args=(buffer,),
                             daemon=True,
                             name=f"Con-{i+1}")
        consumers.append(t)
        t.start()

    # producers
    for i in range(NUM_P):
        t = threading.Thread(target=producerWorker,
                             args=(buffer,),
                             name=f"Prod-{i+1}")
        producers.append(t)
        t.start()

    # wait for production
    for p in producers:
        p.join()

    # send stop signals
    for _ in range(NUM_C):
        buffer.put(STOP)

    # wait for queue to clear
    buffer.join()
    print("All items consumed.")
