import threading

# Without using locks
# x = 0

# def increament():
#     global x
#     for i in range(1000000):
#         x += 1


# t1 = threading.Thread(target=increament)
# t2 = threading.Thread(target=increament)

# t1.start(); t2.start()
# t1.join(); t2.join()
# print(f"Final value of x: {x}")

# Using locks

# x = 0
# lock = threading.Lock()

# def increament():
#     global x
#     for i in range(1000000):
#         with lock:              # automatic lock.acquire() and lock.release()
#             x += 1

# t1 = threading.Thread(target=increament)
# t2 = threading.Thread(target=increament)

# t1.start(); t2.start()
# t1.join(); t2.join()
# print(f"Final value of x: {x}")


# Multiprocessing

# from multiprocessing import Process, Value

# def increment(shared_x):
#     for _ in range(1_000_000):
#         shared_x.value += 1  # Not protected! Can cause race condition

# if __name__ == "__main__":
#     x = Value('i', 0)  # Shared integer ('i' = int)

#     p1 = Process(target=increment, args=(x,))
#     p2 = Process(target=increment, args=(x,))

#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

#     print("Final value of x (race condition):", x.value)


# Above code gives wrong output which can be avoided by applying locks on the shared values

from multiprocessing import Value, Process

def increment(shared_x):
    for _ in range(1_000_000):    
        with shared_x.get_lock():
            shared_x.value += 1

if __name__ == "__main__":    
    x = Value("i", 0)

    p1 = Process(target=increment, args=(x,))
    p2 = Process(target=increment, args=(x,))
    p1.start() 
    p2.start()
    p1.join()
    p2.join()

    print(f"Final value of x is {x.value}")

