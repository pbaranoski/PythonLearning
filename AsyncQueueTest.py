import queue

#pip install codetiming --> a codetiming module

def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for x in range(count):
                total += 1
            print(f"Task {name} total: {total}")

def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = queue.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put(work)

    # Create some synchronous tasks
    # task is a function
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]

    # Run the tasks
    for t, n, q in tasks:
        # can call function 't' in each tuple in list
        t(n, q)

        # Create some tasks
    print("\nList of functions")
    tasks = [task("One", work_queue), task("Two", work_queue)]    
    for taskF in tasks:
        taskF

if __name__ == "__main__":
    main()