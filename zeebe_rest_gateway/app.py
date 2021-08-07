"""
Zeebe REST gateway.

Translates Zeebe gRPC calls to REST requests and vice versa.
"""
from typing import Callable

from fastapi import FastAPI

from zeebe_rest_gateway import endpoints
from zeebe_rest_gateway.containers import Container


class App(FastAPI):
    """A FastAPI application"""

    def __init__(self, container_factory: Callable[[], Container] = Container):
        super().__init__()
        self.container = container_factory()
        self.container.wire(modules=[endpoints])
        self.include_router(endpoints.router)
