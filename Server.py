import grpc
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as serverProto
from concurrent import futures
from Logic.Client import Client

class Server(serverProto.SubscribeServiceServicer, serverProto.PostIntoTopicServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = [Client("Ariel", True), Client("Pepe", True)]
    
    def SubcribeToTopic(self, request, context):
        for client in self.clients:
            if client.name == request.client:
                client.subscribe(request.topic)
                return sender.SubscribeResponse(subsResponse=True)
        return sender.SubscribeResponse(subsResponse=False)
    
    def PostIntoTopic(self, request, context):
        print("New Message posted: " + request.text)
        return sender.PostResponse(postedResponse = True, textResponse = "Successfully posted")

def run_server():
    serverInstance = Server()
    serverGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    serverProto.add_SubscribeServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_PostIntoTopicServiceServicer_to_server(serverInstance, serverGrpc)
    serverGrpc.add_insecure_port('[::]:50051')
    serverGrpc.start()
    print("Initialized gRPC server in port 50051")
    serverGrpc.wait_for_termination()

if __name__ == '__main__':
    run_server()





