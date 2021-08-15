"""
Zeebe REST gateway.

Translates Zeebe gRPC calls to REST requests and vice versa.
"""
import asyncio
from typing import Callable

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from zeebe_rest_gateway import endpoints
from zeebe_rest_gateway.containers import Container
from zeebe_rest_gateway.zeebe.worker import ZeebeWorker


class App(FastAPI):
    """A FastAPI application"""

    def __init__(self, container_factory: Callable[[], Container] = Container):
        container = container_factory()
        container.wire(modules=[endpoints])

        super().__init__()
        self.container = container
        self.include_router(endpoints.router)
        self.mount('/webui', StaticFiles(directory='webui/public', html=True), name='static')


def create_app() -> App:
    """A FastAPI app factory"""
    app = App()
    zeebe_worker: ZeebeWorker = app.container.zeebe_worker.provided()

    async def start_zeebe_worker():
        asyncio.ensure_future(zeebe_worker.start())

    app.add_event_handler('startup', start_zeebe_worker)
    app.add_event_handler('shutdown', zeebe_worker.stop)
    return app
