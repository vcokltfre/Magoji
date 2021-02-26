from aiohttp import ClientSession
from os import getenv

headers = {"Authorization": "token " + getenv("GIST_TOKEN")}


async def create(sess: ClientSession, filename: str, desc: str, data: str) -> dict:
    json = {"description": desc, "public": True, "files": {filename: {"content": data}}}

    async with sess.post(
        "https://api.github.com/gists", json=json, headers=headers
    ) as resp:
        resp.raise_for_status()
        return await resp.json()
