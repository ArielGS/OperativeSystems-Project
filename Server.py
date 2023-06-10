import grpc
import threading
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as serverProto
from concurrent import futures
from Logic.Client import Client

cond = threading.Condition()
lock = threading.Lock()
activeUsers = 0

class Server(serverProto.LoginServiceServicer, serverProto.SubscribeServiceServicer, 
             serverProto.PostIntoTopicServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = {}
        self.clients["Ariel"] = {"client":Client("Ariel", True), "idNumber": 0}

    def LoginIntoApp(self, request, context):
        global activeUsers
        if not self.clients[request.username] == None:
            lock.acquire()
            self.clients[request.username]["client"].state = True
            self.clients[request.username]["idNumber"] = activeUsers
            activeUsers = activeUsers + 1
            lock.release()
        else:
            lock.acquire()
            self.clients[request.username] = {"client":Client(request.username, True), "idNumber":activeUsers}
            activeUsers = activeUsers + 1
            lock.release()
        return sender.LoginResponse(topics=self.clients[request.username]["client"].subscribed, idNumber=activeUsers-1)
    
    def SubcribeToTopic(self, request, context):
        if not self.clients[request.name] == None:
            lock.acquire()
            self.clients[request.name].subscribe(request.topic)
            lock.release()
            return sender.SubscribeResponse(subsResponse=True)
        return sender.SubscribeResponse(subsResponse=False)
    
    def PostIntoTopic(self, request, context):
        #crear mensaje y meterlo en la cola. Luego al enviarlo, eliminarlo.
        print("New Message posted: " + request.text)
        return sender.PostResponse(postedResponse = True, textResponse = "Successfully posted")
    

def run_server():
    serverInstance = Server()
    serverGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    serverProto.add_SubscribeServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_PostIntoTopicServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_LoginServiceServicer_to_server(serverInstance, serverGrpc)
    serverGrpc.add_insecure_port('[::]:50051')
    serverGrpc.start()
    print("Initialized gRPC server in port 50051")
    serverGrpc.wait_for_termination()

if __name__ == '__main__':
    run_server()





