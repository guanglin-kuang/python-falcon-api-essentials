import falcon
import json


class Shop:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def to_dict(self):
        return {"shop_name": self.name, "shop_number": self.number}


laptops = [
    {
        "id": 1,
        "name": "HP EliteBook 820 G2",
        "price": 8842.0,
        "shop": Shop("Amazon", "123"),
    },
    {
        "id": 2,
        "name": "Lenovo ThinkPad T480s",
        "price": 18886.0,
        "shop": Shop("Bestbuy", "456"),
    },
    {
        "id": 3,
        "name": "Apple MacBook Air",
        "price": 16795.0,
        "shop": Shop("AliExpress", "789"),
    },
]


def validate_laptop_input(req, resp, resource, params):
    try:
        laptop = json.load(req.bounded_stream)
    except json.decoder.JSONDecodeError:
        raise falcon.HTTPBadRequest(
            title="Bad request", description="Bad input, must be valid json."
        )

    if "name" not in laptop:
        raise falcon.HTTPBadRequest(
            title="Bad request", description="Bad input, name must be provided."
        )

    req.context["data"] = laptop


class LaptopsResource:
    def on_get(self, req, resp):
        resp.media = laptops
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    @falcon.before(validate_laptop_input)
    def on_post(self, req, resp):
        laptop = req.context.data
        laptops.append(laptop)
        resp.text = "Laptop added successfully."
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_TEXT

    def on_get_laptop(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        resp.media = filtered_laptops
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_put_laptop(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        new_data = json.load(req.bounded_stream)

        for laptop in filtered_laptops:
            laptop.update(new_data)

        resp.media = filtered_laptops
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_delete_laptop(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        ids_removed = [x["id"] for x in filtered_laptops]

        for laptop in filtered_laptops:
            laptops.remove(laptop)

        resp.text = f"Laptop with id {ids_removed} is removed."
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_TEXT


class LaptopResource:
    def on_get(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        resp.media = filtered_laptops
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_put(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        new_data = json.load(req.bounded_stream)

        for laptop in filtered_laptops:
            laptop.update(new_data)

        resp.media = filtered_laptops
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON

    def on_delete(self, req, resp, _id):
        filtered_laptops = list(filter(lambda x: x["id"] == int(_id), laptops))
        ids_removed = [x["id"] for x in filtered_laptops]

        for laptop in filtered_laptops:
            laptops.remove(laptop)

        resp.text = f"Laptop with id {ids_removed} is removed."
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_TEXT
