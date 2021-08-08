"""Dependency Injection containers."""
import grpc
from dependency_injector import containers, providers

from zeebe_rest_gateway.settings import Settings
from zeebe_rest_gateway.spec.gateway_pb2_grpc import GatewayStub
from zeebe_rest_gateway.zeebe.client import ZeebeClient
from zeebe_rest_gateway.zeebe.worker import ZeebeWorker


def create_gateway_stub(settings: Settings) -> GatewayStub:
    """Factory method for creating gRPC gateway stub"""
    channel = grpc.aio.insecure_channel(f'{settings.zeebe_hostname}:{settings.zeebe_port}')
    return GatewayStub(channel)


class Container(containers.DeclarativeContainer):
    """Dependency Injection container"""
    settings: providers.Provider[Settings] = providers.Singleton(
        Settings
    )
    gateway_stub: providers.Provider[GatewayStub] = providers.Factory(
        create_gateway_stub,
        settings=settings,
    )
    zeebe_client: providers.Provider[ZeebeClient] = providers.ThreadLocalSingleton(
        ZeebeClient,
        settings=settings,
        gateway_stub=gateway_stub,
    )
    zeebe_worker: providers.Provider[ZeebeWorker] = providers.ThreadLocalSingleton(
        ZeebeWorker,
        settings=settings,
        gateway_stub=gateway_stub,
    )
