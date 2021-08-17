"""Zeebe gRPC listener"""
import json
from asyncio import sleep

import aiohttp
from fastapi.logger import logger
from grpc.aio import AioRpcError

from zeebe_rest_gateway.fetch import fetch
from zeebe_rest_gateway.settings import Settings
from zeebe_rest_gateway.spec.gateway_pb2 import ActivateJobsRequest, FailJobRequest
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
                    async for response in self.gateway_stub.ActivateJobs(request):
                        next_delay_ms = self.settings.zeebe_worker_delay_after_error_ms
                        for job in response.jobs:
                            logger.debug("Request to activate job:\n%s", job)
                            try:
                                variables = json.loads(job.variables)
                            except json.JSONDecodeError as err:
                                await self.__fail(job.key, f'Failed to JSON decode variables: {err}')
                                continue

                            try:
                                headers = json.loads(job.customHeaders)
                            except json.JSONDecodeError as err:
                                await self.__fail(job.key, f'Failed to JSON decode headers: {err}')
                                continue

                            try:
                                response = await fetch(**variables, **headers)
                            except TypeError as err:
                                await self.__fail(job.key, f'Failed to perform HTTP request: {err}')
                                continue
                            except aiohttp.ClientError:
                                # TODO: handle job error. Reduce retry count etc
                                pass

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

    async def __fail(self, job_key: int, error_message: str) -> None:
        logger.error('Job failed: %s', error_message)
        await self.gateway_stub.FailJob(
            FailJobRequest(jobKey=job_key, retries=0, errorMessage=error_message))
