# import asyncio

# async def download_file(name, delay):
#     print(f"Download file {name}")
#     await asyncio.sleep(delay)
#     print(f"Finished downloading {name}")
#     return name

# async def main():
#     tasks = [
#         asyncio.create_task(download_file("file 1", 2)),
#         asyncio.create_task(download_file("file 2", 2))
#     ]
#     results = await asyncio.gather(*tasks)
#     print("Final result->", results)


# asyncio.run(main())

import asyncio
import time
 
async def simulate_io_operation(task_id, delay):
    print(f"Task {task_id}: Starting operation (simulated delay: {delay}s)")
    # Following line tell your interpreter to wait for 6 seconds
    # time.sleep(delay)
    # Following line tells event loop to switch to other tasks instead waiting
    await asyncio.sleep(delay)
    print(f"Task {task_id}: Finished operation")
    return f"Data from Task {task_id}"

async def main():
    """
        Main function to orchestrate multiple simulated I/O tasks concurrent.
    """
    start_time = time.perf_counter()
    tasks_to_run = [
        simulate_io_operation(1, 3),
        simulate_io_operation(2, 1),
        simulate_io_operation(3, 2),
        simulate_io_operation(4, 1.5)
    ]
    # tasks_to_run = [
    #     asyncio.create_task(simulate_io_operation(1, 3)),
    #     asyncio.create_task(simulate_io_operation(2, 1)),
    #     asyncio.create_task(simulate_io_operation(3, 2)),
    #     asyncio.create_task(simulate_io_operation(4, 1.5))
    # ]
 
    # Run all tasks concurrently and wait for them to complete
    results = await asyncio.gather(*tasks_to_run)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("\n--- All tasks completed ---")
    print(f"Results: {results}")
    print(f"Total elapsed time: {elapsed_time:.2f} seconds")
 
if __name__ == "__main__":
    asyncio.run(main())