"""
based on <https://stackoverflow.com/a/56696955/1876709>
"""

from random import random
import time, asks, trio


snd_input, rcv_input = trio.open_memory_channel(0)
snd_output, rcv_output = trio.open_memory_channel(0)

async def read_entries():
    async with snd_input:
        for key_entry in range(10):
            print( f'reading key `{key_entry}`' )
            await snd_input.send(key_entry)
            # await trio.sleep(1)

## original
# async def work(n):
#     async for key_entry in rcv_input:
#         print(f"w{n} {time.monotonic()} posting", key_entry)
#         r = await asks.post(f"https://httpbin.org/delay/{5 * random()}")
#         await snd_output.send((r.status_code, key_entry))

## passing worker-number to output
async def work(n):
    print( f'rcv_input, `{rcv_input}`; worker, `{n}`' )
    async for key_entry in rcv_input:
        # print( f'rcv_input currently, `{rcv_input}`' )  # not useful, just the addresses of the same channel and buffer; don't know if contents can be viewed on-the-fly
        print( f'posting key `{key_entry}` from worker `{n}` at time `{time.monotonic()}`' )
        r = await asks.post(f"https://httpbin.org/delay/{5 * random()}")
        # await snd_output.send( ( f'wrkr_`{n}`', f'code_`{r.status_code}`', f'key_`{key_entry}`', f'time_`{time.monotonic()}`' ) )
        await snd_output.send( f'sending output from response... key, `{key_entry}`; response-code, `{r.status_code}`; worker, `{n}`; time, `{time.monotonic()}`' )

async def save_entries():
    async for entry in rcv_output:
        # print( "saving", entry )
        print( f'saving entry `{entry}`' )

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(read_entries)
        nursery.start_soon(save_entries)
        async with snd_output:
            print( f'snd_output, `{snd_output}`' )
            async with trio.open_nursery() as workers:
                for n in range(3):
                    print( f'worker `{n}` instantiated' )
                    workers.start_soon(work, n)

trio.run(main)
