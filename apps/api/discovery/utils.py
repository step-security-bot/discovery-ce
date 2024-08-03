import ipaddress
from re import compile, sub

import requests
from fastapi.routing import APIRoute


def custom_generate_unique_id(route: APIRoute):
    return f"{camel_case(route.name)}-{route.tags[0]}"


def camel_case(s: str):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def validate_domain(domain: str) -> bool:
    pattern = compile(
        r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\."
        r"([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$"
    )
    if pattern.match(domain):
        try:
            request = requests.get(
                "https://cloudflare-dns.com/dns-query",
                headers={"accept": "application/dns-json"},
                params={
                    "type": "A",
                    "name": domain,
                },
            )
            request.raise_for_status()
            response = request.json()
            if response["Status"] not in [0]:
                return False

            if isinstance(response["Answer"], list) and len(response["Answer"]) > 0:
                ip = ipaddress.ip_address(
                    response["Answer"][len(response["Answer"]) - 1]["data"]
                )
                return ip.is_global

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            return False

    return False
