
import json
import sys

from http import HTTPStatus
from aiohttp.web import View, Response
from marshmallow import fields
from webargs.aiohttpparser import use_args
from urllib.parse import urlparse

from database.query import get_urls

RESPONSE_CONTENT_TYPE = 'application/json'
FROM = 'from'
TO = 'to'

GET_ARGS = {
    FROM: fields.Int(
        required=True,
        default=0,
        validate=lambda val: val >= 0,
    ),
    TO: fields.Int(
        required=True,
        default=sys.maxsize,
        validate=lambda val: val >= 0 and val <= sys.maxsize,
    ),
}


class VisitedDomains(View):
    @use_args(GET_ARGS, location='querystring')
    async def get(self, args):
        urls = await get_urls(
            db=self.request.app.db,
            start_time=args.get(FROM),
            end_time=args.get(TO),
        )
        domains = list(set([urlparse(url).netloc for url in urls]))
        response = {
            'domains': domains,
            'status': 'ok'
        }
        return Response(
            text=json.dumps(response),
            status=HTTPStatus.OK,
            content_type=RESPONSE_CONTENT_TYPE,
        )
