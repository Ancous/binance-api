import asyncio
import time

import aiofiles


data = "qwerty\n" * 1000


async def write_files(number_files, date):
    async with aiofiles.open(f"my_aiofiles-{number_files}.txt", "w") as file:
        await file.write(date)


async def main(write_data):
    task_1 = asyncio.create_task(write_files(1, write_data))
    task_2 = asyncio.create_task(write_files(2, write_data))
    task_3 = asyncio.create_task(write_files(3, write_data))

    await task_1
    await task_2
    await task_3


if __name__ in "__main__":
    start = time.time()
    asyncio.run(main(data))
    print(f"Асинхронное время выполнения: {time.time() - start} секунд.")
