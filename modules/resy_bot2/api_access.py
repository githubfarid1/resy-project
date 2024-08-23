from datetime import datetime
from requests import Session, HTTPError
from typing import Dict, List
from resy_bot2.constants import RESY_BASE_URL, ResyEndpoints
from resy_bot2.logging import logging
from resy_bot2.models import (
    ResyConfig,
    AuthRequestBody,
    AuthResponseBody,
    FindRequestBody,
    FindResponseBody,
    Slot,
    DetailsRequestBody,
    DetailsResponseBody,
    BookRequestBody,
    BookResponseBody,
    VenueBody,
)
from user_agent import generate_user_agent
# import os
# import sys
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(os.path.dirname(current))
# sys.path.append(parent)
# from settings import PROXIES

logger = logging.getLogger(__name__)
logger.setLevel("ERROR")


def build_session(config: ResyConfig) -> Session:

    session = Session()
    headers = {
        "Authorization": config.get_authorization(),
        "X-Resy-Auth-Token": config.token,
        "X-Resy-Universal-Auth": config.token,
        "Origin": "https://resy.com",
        "X-origin": "https://resy.com",
        "Referrer": "https://resy.com/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": generate_user_agent(),
        'Cache-Control': "no-cache",
    }
    session.headers.update(headers)
    if config.http_proxy != '':
        proxies = {
            'http': config.http_proxy,
            'https': config.https_proxy,
        }
        session.proxies.update(proxies)
        logger.info("Proxy Updated")
    
    return session


class ResyApiAccess:
    @classmethod
    def build(cls, config: ResyConfig) -> "ResyApiAccess":
        session = build_session(config)
        return cls(session)

    def __init__(self, session: Session):
        self.session = session
    #frd
    def find_venue_id(self, params: VenueBody):
        find_url = RESY_BASE_URL + ResyEndpoints.VENUE.value
        logger.info(
            f"{datetime.now().isoformat()} Sending request to find venue_id"
        )
        
        resp = self.session.get(find_url, params=params.dict())
        logger.info(f"{datetime.now().isoformat()}: Received response for ")
        if not resp.ok:
            raise HTTPError(
                f"Failed to find booking venue_id: {resp.status_code}, {resp.text}"
            )
        return resp.json()['id']['resy']

    def auth(self, body: AuthRequestBody) -> AuthResponseBody:
        auth_url = RESY_BASE_URL + ResyEndpoints.PASSWORD_AUTH.value

        resp = self.session.post(
            auth_url,
            data=body.dict(),
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        if not resp.ok:
            raise HTTPError(f"Failed to get auth: {resp.status_code}, {resp.text}")

        return AuthResponseBody(**resp.json())

    def find_booking_slots(self, params: FindRequestBody) -> List[Slot]:
        find_url = RESY_BASE_URL + ResyEndpoints.FIND.value

        logger.info(
            f"{datetime.now().isoformat()} Sending request to find booking slots"
        )

        resp = self.session.get(find_url, params=params.dict())
        logger.info(f"{datetime.now().isoformat()}: Received response for ")

        if not resp.ok:
            #frd
            if resp.status_code == 500:
                logger.info(self.get_ip_used().strip())
            #----
            raise HTTPError(
                f"Failed to find booking slots: {resp.status_code}, {resp.text}"
            )

        parsed_resp = FindResponseBody(**resp.json())
        #frd
        if len(parsed_resp.results.venues) == 0:
            raise IndexError("Date or vanue is not available")
        else:
            return parsed_resp.results.venues[0].slots
        # return parsed_resp.results.venues[0].slots

    def get_booking_token(self, params: DetailsRequestBody) -> DetailsResponseBody:
        details_url = RESY_BASE_URL + ResyEndpoints.DETAILS.value

        resp = self.session.get(details_url, params=params.dict())

        if not resp.ok:
            raise HTTPError(
                f"Failed to get selected slot details: {resp.status_code}, {resp.text}"
            )

        return DetailsResponseBody(**resp.json())
    
    def _dump_book_request_body_to_dict(self, body: BookRequestBody) -> Dict:
        """
        requests lib doesn't urlencode nested dictionaries,
        so dump struct_payment_method to json and slot that in the dict
        """
        payment_method = body.struct_payment_method.json().replace(" ", "")
        body_dict = body.dict()
        body_dict["struct_payment_method"] = payment_method
        return body_dict

    def book_slot(self, body: BookRequestBody) -> str:
        book_url = RESY_BASE_URL + ResyEndpoints.BOOK.value

        body_dict = self._dump_book_request_body_to_dict(body)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://widgets.resy.com",
            "X-Origin": "https://widgets.resy.com",
            "Referrer": "https://widgets.resy.com/",
            "Cache-Control": "no-cache",
        }

        resp = self.session.post(
            book_url,
            data=body_dict,
            headers=headers,
        )

        if not resp.ok:
            raise HTTPError(f"Failed to book slot: {resp.status_code}, {resp.text}")

        logger.info(resp.json())
        parsed_resp = BookResponseBody(**resp.json())

        return parsed_resp.resy_token
    #frd
    def get_ip_used(self):
        response = self.session.get("http://whatismyip.akamai.com/")
        if response.status_code == 200:
            return response.text.strip()
    
