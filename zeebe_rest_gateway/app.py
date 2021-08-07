"""
Zeebe REST gateway.

Translates Zeebe gRPC calls to REST requests and vice versa.
"""
from fastapi import FastAPI

from zeebe_rest_gateway import endpoints
from zeebe_rest_gateway.containers import Container

container = Container()
container.wire(modules=[endpoints])

app = FastAPI()
app.include_router(endpoints.router)
