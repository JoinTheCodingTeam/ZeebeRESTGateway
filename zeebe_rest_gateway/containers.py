"""Dependency Injection containers."""
import grpc
from dependency_injector import containers, providers

from zeebe_rest_gateway.settings import Settings
from zeebe_rest_gateway.spec.gateway_pb2_grpc import GatewayStub
from zeebe_rest_gateway.zeebe.client import ZeebeClient


def create_gateway_stub(settings: Settings) -> GatewayStub:
    """Factory method for creating gRPC gateway stub"""
    channel = grpc.aio.insecure_channel(f'{settings.zeebe_hostname}:{settings.zeebe_port}')
    return GatewayStub(channel)


class Container(containers.DeclarativeContainer):
    """Dependency Injection container"""
    settings = providers.Singleton(
        Settings
    )
    gateway_stub = providers.Factory(
        create_gateway_stub,
        settings=settings,
    )
    zeebe_client = providers.Factory(
        ZeebeClient,
        settings=settings,
        gateway_stub=gateway_stub,
    )
