import aiohttp


async def fetch_url_post(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"}
        ) as response:
            try:
                return await response.json()
            except aiohttp.ClientError:
                return None
