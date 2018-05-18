import datetime, logging
import requests, trio


logging.basicConfig(
    # filename=os.environ['TRIO__LOG_PATH'],
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    )
log = logging.getLogger(__name__)
log.debug( 'log starting' )


def run_code():
    """ Runner.
        Called by ```if __name__ == '__main__':``` """
    start = datetime.datetime.now()
    trio.run(parent, start)
    end = datetime.datetime.now()
    print( 'run_code complete, that took `%s`' % str( end-start ) )


async def child1( some_holder_dct ):
    some_holder_dct['child1'] = 'aa'
    print("  child1: started! sleeping now...")
    await trio.sleep(2)
    print("  child1: exiting!")

async def child2( some_holder_dct ):
    some_holder_dct['child2'] = 'bb'
    print("  child2: started! sleeping now...")
    await trio.sleep(2)
    print("  child2: exiting!")

async def parent( start_time ):
    some_holder_dct = {}
    print("parent: started!")
    async with trio.open_nursery() as nursery:
        print("parent: spawning child1...")
        nursery.start_soon(child1, some_holder_dct)

        print("parent: spawning child2...")
        nursery.start_soon(child2, some_holder_dct)

        print("parent: waiting for children to finish...")

        # -- we exit the nursery block here --
        interim = datetime.datetime.now() - start_time
        log.debug( 'interim, `%s`' % str(interim) )
    log.debug( 'some_holder_dct, outside of nursery, `%s`' % some_holder_dct )
    print("parent: all done!")


if __name__ == '__main__':
    log.debug( '__main__ startng' )
    run_code()
    log.debug( '__main__ complete' )
