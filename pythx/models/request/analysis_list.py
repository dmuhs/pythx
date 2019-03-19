import json
from datetime import datetime
from typing import Any, Dict, List

import dateutil.parser

from pythx.models.exceptions import RequestDecodeError, RequestValidationError
from pythx.models.request.base import BaseRequest
from pythx.models.util import dict_delete_none_fields

ANALYSIS_LIST_KEYS = ("offset", "dateFrom", "dateTo")


class AnalysisListRequest(BaseRequest):
    def __init__(self, offset: int, date_from: datetime, date_to: datetime):
        self.offset = offset
        self.date_from = date_from
        self.date_to = date_to

    @property
    def endpoint(self):
        return "v1/analyses"

    @property
    def method(self):
        return "GET"

    @property
    def headers(self):
        return {}

    @property
    def parameters(self):
        return self.to_dict()

    @property
    def payload(self):
        return {}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        if not all(k in d for k in ANALYSIS_LIST_KEYS):
            raise RequestDecodeError(
                "Not all required keys {} found in data {}".format(
                    ANALYSIS_LIST_KEYS, d
                )
            )
        req = cls(
            offset=d["offset"],
            date_from=dateutil.parser.parse(d["dateFrom"]),
            date_to=dateutil.parser.parse(d["dateTo"]),
        )

        return req

    def to_dict(self):
        return {
            "offset": self.offset,
            "dateFrom": self.date_from.isoformat() if self.date_from else None,
            "dateTo": self.date_to.isoformat() if self.date_to else None,
        }
