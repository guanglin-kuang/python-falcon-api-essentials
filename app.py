import falcon

from hello_world_api import HelloWorldResource
from laptops import LaptopResource, LaptopsResource
from response_cleaner_middleware import ResponseCleanerMiddleware

app = application = falcon.App(middleware=[ResponseCleanerMiddleware()])

# Dummpy hellow word API.
app.add_route("/hello_world", HelloWorldResource())

# Laptops API
app.add_route("/laptops", LaptopsResource())

# Laptop API with a common resource using the suffix feature.
app.add_route("/laptops/{_id}", LaptopsResource(), suffix="laptop")

# Laptop API with separte resource
# app.add_route("/laptops/{_id}", LaptopResource())
