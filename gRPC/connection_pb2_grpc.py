# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from gRPC import connection_pb2 as gRPC_dot_connection__pb2


class SubscribeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubcribeToTopic = channel.unary_unary(
                '/connection.SubscribeService/SubcribeToTopic',
                request_serializer=gRPC_dot_connection__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=gRPC_dot_connection__pb2.SubscribeResponse.FromString,
                )


class SubscribeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SubcribeToTopic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SubscribeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubcribeToTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.SubcribeToTopic,
                    request_deserializer=gRPC_dot_connection__pb2.SubscribeRequest.FromString,
                    response_serializer=gRPC_dot_connection__pb2.SubscribeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'connection.SubscribeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SubscribeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SubcribeToTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connection.SubscribeService/SubcribeToTopic',
            gRPC_dot_connection__pb2.SubscribeRequest.SerializeToString,
            gRPC_dot_connection__pb2.SubscribeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class PostIntoTopicServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PostIntoTopic = channel.unary_unary(
                '/connection.PostIntoTopicService/PostIntoTopic',
                request_serializer=gRPC_dot_connection__pb2.PostRequest.SerializeToString,
                response_deserializer=gRPC_dot_connection__pb2.PostResponse.FromString,
                )


class PostIntoTopicServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PostIntoTopic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PostIntoTopicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PostIntoTopic': grpc.unary_unary_rpc_method_handler(
                    servicer.PostIntoTopic,
                    request_deserializer=gRPC_dot_connection__pb2.PostRequest.FromString,
                    response_serializer=gRPC_dot_connection__pb2.PostResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'connection.PostIntoTopicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PostIntoTopicService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PostIntoTopic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connection.PostIntoTopicService/PostIntoTopic',
            gRPC_dot_connection__pb2.PostRequest.SerializeToString,
            gRPC_dot_connection__pb2.PostResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class LoginServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LoginIntoApp = channel.unary_unary(
                '/connection.LoginService/LoginIntoApp',
                request_serializer=gRPC_dot_connection__pb2.LoginRequest.SerializeToString,
                response_deserializer=gRPC_dot_connection__pb2.LoginResponse.FromString,
                )


class LoginServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LoginIntoApp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LoginServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LoginIntoApp': grpc.unary_unary_rpc_method_handler(
                    servicer.LoginIntoApp,
                    request_deserializer=gRPC_dot_connection__pb2.LoginRequest.FromString,
                    response_serializer=gRPC_dot_connection__pb2.LoginResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'connection.LoginService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LoginService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LoginIntoApp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connection.LoginService/LoginIntoApp',
            gRPC_dot_connection__pb2.LoginRequest.SerializeToString,
            gRPC_dot_connection__pb2.LoginResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
