from dataclasses import dataclass
import requests
from requests.adapters import HTTPAdapter, Retry
import typing as t
import orjson

from src.api.models import Entity


@dataclass
class ApiClient:
    endpoint: str = "http://probook.local/v1"
    session_token: t.Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

        retries = Retry(
            total=10, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504]
        )

        self.session.mount("http://", HTTPAdapter(max_retries=retries))

    def authorize(self, username, password):
        r = requests.post(
            f"{self.endpoint}/user/login",
            json={
                "username": username,
                "password": password,
            },
        )
        self.session_token = r.text.strip().strip('"')
        print(self.session_token)

    def upload_entity(self, entity: Entity):

        r = self.session.post(
            f"{self.endpoint}/entity",
            data=orjson.dumps(entity).decode("utf-8"),
            headers={"apiKey": self.session_token, "Content-Type": "application/json"},
        )
        print(entity.wikidata_id, "-->", r.json())
