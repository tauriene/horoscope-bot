import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup


class HoroscopeApiClient:
    def __init__(self):
        self.session: ClientSession | None = None

    async def connect(self):
        self.session = ClientSession()

    async def close(self):
        await self.session.close()

    async def _fetch_html(self, link: str) -> str:
        async with self.session.get(link) as response:
            if response.status != 200:
                raise Exception()
            else:
                return await response.text()

    async def get_horoscope_text(self, zdc_sign: str) -> str:
        link = f"https://horo.mail.ru/prediction/{zdc_sign}/today/"
        content = await self._fetch_html(link)

        soup = BeautifulSoup(markup=content, features="lxml")
        horoscope = [
            e.text
            for e in soup.find("main", attrs={"itemprop": "articleBody"}).find_all("p")
        ]

        return "\n\n".join(horoscope)

    async def get_compatibility_text(
        self, female_zdc_sign: str, male_zdc_sign: str
    ) -> tuple[str, str, str, str]:
        link = f"https://1001goroskop.ru/sovmestimost/?wom={female_zdc_sign}&man={male_zdc_sign}"

        content = await self._fetch_html(link)
        soup = BeautifulSoup(markup=content, features="lxml")

        main_center_div = soup.find("div", id="maincenter")
        main_center_p = main_center_div.find_all("p")

        relationship_type = main_center_div.find_all("h1")[-1].text.split(":")[-1]
        love, marriage = re.findall(r"\d+", main_center_p[0].text)
        description = "\n".join(e.text for e in main_center_p[1:3])

        return relationship_type, love, marriage, description
