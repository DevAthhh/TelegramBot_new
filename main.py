import asyncio

from src import writting_repository as wr
from src import message_handler as mh
# async def writting_repository():
#     wr.wr_main()


async def waiting_user():
    mh.mh_main()
    
async def main():
    await asyncio.gather(waiting_user())

asyncio.run(main())