import asyncio
#from codetiming import Timer

#######################################################################
# If you have a list of requests/records to process where each 
# request/record takes a while to process --> 
# consider processing the requests asynchronously instead of syncronously.
# 
# The requests/records become a share resource to process
# as several separate tasks asynchronously. When a task completes a request
# it processes the next available request.
#######################################################################

async def task(name, work_queue):
    #timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    print(f"task {name} started")

    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        #timer.start()
        await asyncio.sleep(delay)
        #timer.stop()

    print(f"task {name} ended")

async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    print(work_queue.qsize())    

    # Run the tasks
    #with Timer(text="\nTotal elapsed time: {:.1f}"):
    await asyncio.gather(
        asyncio.create_task(task("One", work_queue)),
        asyncio.create_task(task("Two", work_queue)),
    )

if __name__ == "__main__":
    asyncio.run(main())