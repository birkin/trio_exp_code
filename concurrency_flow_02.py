"""
based on <https://stackoverflow.com/a/56694314/1876709>

Comments...

- nice example of CapacityLimiter usage
    - see line ```print( f'sub_dct, ```{sub_dct}```; limit, `{limit}`' )``` for queue build-up
    - see line ```print( f'limit currently `{limit}`' )``` for queue processing
- doesn't show usage of saving data synchronously along the way, for that see `concurrency_flow_01.py`
"""

import pprint, time
from random import random

import asks, trio


async def process_file():

    ## load the file synchronously
    # with open(input_file) as fd:
    #     data = json.load(fd)

    ## load the file synchronously
    data = {}
    for i in range(10):
        data[str(i)] = { 'updated': None, 'response_code': None }
    print( f'data, ```{pprint.pformat(data)}```' )

    ## poster
    async def post_update( sub_dct, limit ):
        print( f'sub_dct, ```{sub_dct}```; limit, `{limit}`' )
        key, val = list(sub_dct.items())[0]
        async with limit:
            print( f'limit currently `{limit}`' )
            r = await asks.post( f"https://httpbin.org/delay/{5 * random()}" )
            sub_dct[key]['response_code'] = r.status_code
            sub_dct[key]['updated'] = 'yes'

    ## saver
    def save_file( data ):
        print( f'saved_data, ```{pprint.pformat(data)}```' )

    ## iterate over your dict asynchronously
    limit = trio.CapacityLimiter( 3 )
    async with trio.open_nursery() as nursery:
        for key, sub in data.items():
            print( f'key, `{key}`; sub, `{sub}`' )
            if sub['updated'] is None:
                sub['updated'] = 'in_progress'
                nursery.start_soon(post_update, {key: sub}, limit)

    ## save your result json synchronously
    # save_file(data, input_file)
    save_file( data )

    # limit = trio.CapacityLimiter(10)
    # # iterate over your dict asynchronously
    # async with trio.open_nursery() as nursery:
    #     for key, sub in data.items():
    #         if sub['updated'] is None:
    #             sub['updated'] = 'in_progress'
    #             nursery.start_soon(post_update, {key: sub}, limit)


trio.run( process_file )
