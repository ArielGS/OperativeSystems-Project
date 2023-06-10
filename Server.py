import pickle
import grpc
import threading
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as serverProto
from concurrent import futures
from Logic.Client import Client
from Logic.Message import Message

cond = threading.Condition()
lock = threading.Lock()
activeUsers = 0

def saveClients(clients):
    with open("clients.pickle", "wb") as file:
        pickle.dump(clients, file)

class Server(serverProto.LoginServiceServicer, serverProto.SubscribeServiceServicer, 
             serverProto.PostIntoTopicServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = {}
        try:
            with open('clients.pickle', 'rb') as archivo:
                self.clients = pickle.load(archivo)
        except (FileNotFoundError):
            self.clients["First"] = Client("First", False)
            saveClients(self.clients)

    def LoginIntoApp(self, request, context):
        global activeUsers
        if self.clients.get(request.username) is not None:
            lock.acquire()
            self.clients[request.username].state = True
            self.clients[request.username].idNumber = activeUsers
            activeUsers = activeUsers + 1
            lock.release()
        else:
            lock.acquire()
            self.clients[request.username] = Client(request.username, True)
            self.clients[request.username].idNumber = activeUsers
            activeUsers = activeUsers + 1
            saveClients(self.clients)
            lock.release()
        return sender.LoginResponse(topics=self.clients[request.username].subscribed, idNumber=activeUsers-1)
    
    def SubcribeToTopic(self, request, context):
        if self.clients.get(request.client) is not None:
            lock.acquire()
            client = self.clients[request.client]
            client.subscribe(request.topic)
            lock.release()
            return sender.SubscribeResponse(subsResponse=True)
        return sender.SubscribeResponse(subsResponse=False)
    
    def PostIntoTopic(self, request, context):
        if self.clients.get(request.publisher) is not None:
            current = self.clients[request.publisher]
            if request.topic in current.subscribed:
                newMessage = Message(request.text, request.topic, request.publisher, None)
                if request.topic == "A":
                    self.messagesTopicA.append(newMessage)
                elif request.topic == "B":
                    self.messagesTopicB.append(newMessage)
                elif request.topic == "C":
                    self.messagesTopicC.append(newMessage)
                #Enviar el msj.
                print("New Message posted: " + request.text)
                return sender.PostResponse(postedResponse = True, textResponse = "Successfully posted.")
            else:
                return sender.PostResponse(postedResponse = False, textResponse = "You are not subscribed to that topic.")
        return sender.PostResponse(postedResponse = False, textResponse = "Error. Try again.")
    
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





