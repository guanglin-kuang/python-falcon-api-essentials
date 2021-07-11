import falcon
import json
from laptops import Shop


def custom_json_serializer(obj):
    if isinstance(obj, Shop):
        return obj.to_dict()


class ResponseCleanerMiddleware(object):
    def process_response(self, req, resp, resource, req_succeeded):
        if resp.content_type == falcon.MEDIA_JSON:
            resp.text = json.dumps(resp.media, default=custom_json_serializer)
