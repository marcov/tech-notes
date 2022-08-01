#!/usr/bin/env python3.7

'''
async run() and gather() requires python3.7+
'''

import asyncio
import time

msgs = ('ciao', 'belli', 'e', 'brutti')

async def printer(m):
    await asyncio.sleep(1)
    print(f'printer: {m}')
    return m

async def async_gather_example():
    await asyncio.gather(
            *map(printer, msgs)
    )

asyncio.run(async_gather_example())
print('i am done here ...')

'''
This should work on python3.6 too.
'''
async def async_as_completed_example():
    for task in asyncio.as_completed(map(printer, msgs)):
        result = await task
        print(f'result: {result}')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(async_as_completed_example())
print('i am done here ...')
