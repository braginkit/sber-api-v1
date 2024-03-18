
import json
import types

from time import time
from http import HTTPStatus
from aiohttp.web import View, Response
from marshmallow import fields
from webargs.aiohttpparser import parser

from database.query import add_new_urls

RESPONSE_CONTENT_TYPE = 'application/json'

POST_ARGS = types.MappingProxyType({
    'links': fields.List(
        fields.URL,
        required=False,
    )
})


class VisitedLinks(View):
    async def post(self):
        request_time = int(time())
        args = await parser.parse(
            argmap=POST_ARGS,
            req=self.request,
        )

        await add_new_urls(
            db=self.request.app.db,
            urls=args.get('links'),
            time=request_time,
        )

        response = {'status': 'ok'}
        return Response(
            text=json.dumps(response),
            status=HTTPStatus.OK,
            content_type=RESPONSE_CONTENT_TYPE,
        )
