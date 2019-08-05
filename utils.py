import os

import aiosqlite


async def fetch_async(fetch_type, query):
    async with aiosqlite.connect(os.getenv("MUSIC_DB")) as con:
        async with con.execute(query) as cur:
            if fetch_type == "one":
                row = await cur.fetchone()
            elif fetch_type == "all":
                row = await cur.fetchall()
    return row
