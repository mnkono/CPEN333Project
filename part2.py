# Group #: B42
# Student names: Mfon Nkono and Saranga Varma
 
import threading
import queue
import time, random

# Easy-to-change constants
NUM_PRODUCERS = 4
NUM_CONSUMERS = 5
ITEMS_PER_PRODUCER = 5

PRODUCER_DELAY_MIN = 0.1
PRODUCER_DELAY_MAX = 0.4
CONSUMER_DELAY_MIN = 0.1
CONSUMER_DELAY_MAX = 0.5

STOP_ITEM = None   # special value used to stop consumers


def consumerWorker(buffer: queue.Queue) -> None:
    """Target worker for a consumer thread."""
    while True:
        # Get the next item from the shared queue
        item = buffer.get()

        # If the item is the stop signal, this consumer should end
        if item == STOP_ITEM:
            print(f"{threading.current_thread().name} received stop signal and is ending.")
            buffer.task_done()
            break

        # Simulate consuming the item
        print(f"{threading.current_thread().name} consumed {item}")
        time.sleep(random.uniform(CONSUMER_DELAY_MIN, CONSUMER_DELAY_MAX))

        # Tell the queue this item has been fully processed
        buffer.task_done()


def producerWorker(buffer: queue.Queue) -> None:
    """Target worker for a producer thread."""
    for itemNumber in range(1, ITEMS_PER_PRODUCER + 1):
        # Create an item label so the output is easy to follow
        item = f"{threading.current_thread().name}-Item{itemNumber}"

        # Put the new item into the queue
        buffer.put(item)
        print(f"{threading.current_thread().name} produced {item}")

        # Sleep for a random short time to simulate irregular production
        time.sleep(random.uniform(PRODUCER_DELAY_MIN, PRODUCER_DELAY_MAX))


if __name__ == "__main__":
    # Shared FIFO buffer
    buffer = queue.Queue()

    producerThreads = []
    consumerThreads = []

    # Start consumer threads first so they are ready to take items
    for i in range(NUM_CONSUMERS):
        consumer = threading.Thread(
            target=consumerWorker,
            args=(buffer,),
            daemon=True,
            name=f"Consumer-{i + 1}"
        )
        consumerThreads.append(consumer)
        consumer.start()

    # Start producer threads
    for i in range(NUM_PRODUCERS):
        producer = threading.Thread(
            target=producerWorker,
            args=(buffer,),
            name=f"Producer-{i + 1}"
        )
        producerThreads.append(producer)
        producer.start()

    # Wait for all producers to finish producing items
    for producer in producerThreads:
        producer.join()

    # After all producers are done, add one stop signal per consumer
    for _ in range(NUM_CONSUMERS):
        buffer.put(STOP_ITEM)

    # Wait until all items in the queue have been processed
    buffer.join()

    print("All produced items have been consumed. Program ending.")
