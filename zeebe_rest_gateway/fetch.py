"""HTTP request handler"""
import string
from typing import Dict, Any

import aiohttp


async def fetch(method: str, url: str, headers: Dict[str, str], variables: Dict[str, str]) -> Any:
    url = string.Template(url).safe_substitute(variables)
    headers = {string.Template(key).safe_substitute(variables): string.Template(value).safe_substitute(variables)
               for key, value in headers.items()}
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, json=variables) as resp:
            return await resp.json()
