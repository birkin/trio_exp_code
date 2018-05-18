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


async def child1():
    print("  child1: started! sleeping now...")
    await trio.sleep(2)
    print("  child1: exiting!")
    return 'a'

async def child2():
    print("  child2: started! sleeping now...")
    await trio.sleep(2)
    print("  child2: exiting!")
    return 'b'

async def parent( start_time ):
    print("parent: started!")
    async with trio.open_nursery() as nursery:
        print("parent: spawning child1...")
        foo = nursery.start_soon(child1)

        print("parent: spawning child2...")
        bar = nursery.start_soon(child2)

        print("parent: waiting for children to finish...")

        log.debug( 'foo, within nursery, `%s`' % foo )

        # -- we exit the nursery block here --
        interim = datetime.datetime.now() - start_time
        log.debug( 'interim, `%s`' % str(interim) )
    log.debug( 'foo, outside of nursery, `%s`' % foo )
    print("parent: all done!")


if __name__ == '__main__':
    log.debug( '__main__ startng' )
    run_code()
    log.debug( '__main__ complete' )
