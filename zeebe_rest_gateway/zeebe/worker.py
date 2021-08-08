"""Zeebe gRPC listener"""
from asyncio import sleep

from fastapi.logger import logger
from grpc.aio import AioRpcError

from zeebe_rest_gateway.settings import Settings
from zeebe_rest_gateway.spec.gateway_pb2 import ActivateJobsRequest
from zeebe_rest_gateway.spec.gateway_pb2_grpc import GatewayStub


class ZeebeWorker:
    """Zeebe task listener"""

    def __init__(self, *, settings: Settings, gateway_stub: GatewayStub):
        self.settings = settings
        self.gateway_stub = gateway_stub
        self.stopped = False

    async def start(self):
        """Starts listening to incoming Zeebe job requests"""
        try:
            next_delay_ms = self.settings.zeebe_worker_delay_after_error_ms
            while not self.stopped:
                request = ActivateJobsRequest(type='rest', worker=f'{self.__class__.__name__}[{id(self)}]',
                                              timeout=self.settings.rest_job_timeout_ms,
                                              maxJobsToActivate=self.settings.rest_job_timeout_ms, fetchVariable=[],
                                              requestTimeout=0)
                try:
                    responses = self.gateway_stub.ActivateJobs(request)
                    async for response in responses:
                        next_delay_ms = self.settings.zeebe_worker_delay_after_error_ms
                        logger.debug(response)
                except AioRpcError as err:
                    logger.error('gRPC exception: %s. Retrying in %d ms', err, next_delay_ms)
                    await sleep(next_delay_ms / 1000)
                    next_delay_ms = min(60000, next_delay_ms * 2)
                    continue
        except Exception as err:
            logger.exception('Unhandled exception')
            raise err

    def stop(self):
        """Stops listening to Zeebe job events"""
        self.stopped = True
