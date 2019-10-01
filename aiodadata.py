import aiohttp
from typing import Iterable, List


class DaDataClient:
    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret

    async def addresses_standartization(self, *addresses: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/address",
            json=list(addresses),
            need_secret=True,
        )

    async def phones_standartization(self, *phones: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/phone",
            json=list(phones),
            need_secret=True,
        )

    async def passports_standartization(self, *passports: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/passport",
            json=list(passports),
            need_secret=True,
        )

    async def names_standartization(self, *names: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/name",
            json=list(names),
            need_secret=True,
        )

    async def emails_standartization(self, *emails: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/email",
            json=list(emails),
            need_secret=True,
        )

    async def dates_standartization(self, *dates: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/birthdate",
            json=list(dates),
            need_secret=True,
        )

    async def cars_standartization(self, *cars: Iterable[str]):
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean/vehicle",
            json=list(cars),
            need_secret=True,
        )

    async def record_standartization(self, *records: dict):
        data = []
        structure = {}
        for record in records:
            structure.update(record.keys())
        structure = list(structure)
        for record in records:
            row = []
            for key in structure:
                row.append(record.get(key))
            data.append(row)
        return await self.request(
            method="POST",
            url="https://cleaner.dadata.ru/api/v1/clean",
            json={
                "data": data,
                "structure": structure, 
            },
            need_secret=True,
        )

    async def name_hint(self, query: str, count: int=10, parts: (List[str], None)=None,
                        gender: str="UNKNOWN"):
        data = {"query": query, "count": count, "gender": gender}
        if parts is not None: data["parts"] = parts
        return await self.request(
            method="POST",
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/fio",
            json=data,
            need_secret=False,
        )

    async def address_hint(self, query: str, count: int=10, locations: (List[dict], None)=None,
                           locations_boost: (List[dict], None)=None, from_bound: (dict, None)=None,
                           to_bound: (dict, None)=None):
        data = {"query": query, "count": count}
        if locations is not None: data["locations"] = locations
        if locations_boost is not None: data["locations_boost"] = locations_boost
        if from_bound is not None: data["from_bound"] = from_bound
        if to_bound is not None: data["to_bound"] = to_bound
        return await self.request(
            method="POST",
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
            json=data,
            need_secret=False,
        )

    async def party_hint(self, query: str, count: int=10, active: bool=True,
                         liquidating: bool=True, liquidated: bool=True, individual: bool=True,
                         legal: bool=True, locations: (List[dict], None)=None,
                         locations_boost: (List[dict], None)=None):
        status = []
        if active: status.append("ACTIVE")
        if liquidating: status.append("LIQUIDATING")
        if liquidated: status.append("LIQUIDATED")
        type = []
        if individual: type.append("INDIVIDUAL")
        if legal: type.append("LEGAL")
        data = {"query": query, "count": count, "status": status, "type": type}
        if locations is not None: data["locations"] = locations
        if locations_boost is not None: data["locations_boost"] = locations_boost
        return await self.request(
            method="POST",
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party",
            json=data,
            need_secret=False,
        )

    async def party_hint_by_inn(self, query: str, main: bool=True, branch: bool=True,
                                individual: bool=True, legal: bool=True, kpp: (str, None)=None):
        branch_type = []
        if main: branch_type.append("MAIN")
        if branch: branch_type.append("BRANCH")
        type = []
        if individual: type.append("INDIVIDUAL")
        if legal: type.append("LEGAL")
        data = {"query": query, "branch_type": branch_type, "type": type}
        if kpp is not None: data["kpp"] = kpp
        return await self.request(
            method="POST",
            url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party",
            json=data,
            need_secret=False,
        )

    # NEED MORE HINTS

    # NEED MORE SPRAVOCHNIKI

    async def address_by_geoposition(self, latitude: float, longitude: float, count: int=10,
                                     radius: int=100, method: str="POST"):
        data = {"lat": latitude, "lon": longitude, "count": count, "radius_meters": radius}
        if method.upper() == "GET":
            return await self.request(
                method="GET",
                url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address",
                params=data,
                need_secret=False,
            )
        elif method.upper() == "POST":
            return await self.request(
                method="POST",
                url="https://suggestions.dadata.ru/suggestions/api/4_1/rs/geolocate/address",
                json=data,
                need_secret=False,
            )

    # NEED MORE OTHER METHODS

    async def request(self, method: str, url: str, data=None, params=None, json=None,
                      need_secret: bool=False):
        headers = {"Authorization": "Token %s" % self.token, "Accept": "application/json"}
        if need_secret:
            headers["X-Secret"] = self.secret
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                data=data,
                params=params,
                json=json,
                headers=headers,
            ) as response:
                return await response.json()
