import pickle
import grpc
import threading
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as serverProto
from concurrent import futures
from Logic.Client import Client
from Logic.Message import Message

cond = threading.Condition()
lockMain = threading.Lock()
lockTopicA = threading.Lock()
lockTopicB = threading.Lock()
lockTopicC = threading.Lock()
activeUsers = 0

def saveClients(clients):
    with open("clients.pickle", "wb") as file:
        pickle.dump(clients, file)

class Server(serverProto.LoginServiceServicer, serverProto.SubscribeServiceServicer, 
             serverProto.PostIntoTopicServiceServicer, serverProto.ListeningServiceServicer, serverProto.StopListeningServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = {}
        try:
            with open('clients.pickle', 'rb') as file:
                self.clients = pickle.load(file)
        except (FileNotFoundError):
            self.clients["First"] = Client("First", False)
            saveClients(self.clients)

    def LoginIntoApp(self, request, context):
        global activeUsers
        if self.clients.get(request.username) is not None:
            lockMain.acquire()
            self.clients[request.username].state = True
            self.clients[request.username].idNumber = activeUsers
            activeUsers = activeUsers + 1
            lockMain.release()
        else:
            lockMain.acquire()
            self.clients[request.username] = Client(request.username, True)
            self.clients[request.username].idNumber = activeUsers
            activeUsers = activeUsers + 1
            saveClients(self.clients)
            lockMain.release()
        return sender.LoginResponse(topics=self.clients[request.username].subscribed, idNumber=activeUsers-1)
    
    def SubcribeToTopic(self, request, context):
        if self.clients.get(request.client) is not None:
            lockMain.acquire()
            client = self.clients[request.client]
            client.subscribe(request.topic)
            lockMain.release()
            return sender.SubscribeResponse(subsResponse=True)
        return sender.SubscribeResponse(subsResponse=False)
    
    def PostIntoTopic(self, request, context):
        if self.clients.get(request.publisher) is not None:
            current = self.clients[request.publisher]
            if request.topic in current.subscribed:
                newMessage = Message(request.text, request.topic, request.publisher, None)
                if request.topic == "A":
                    lockTopicA.acquire()
                    self.messagesTopicA.append(newMessage)
                    lockTopicA.release()
                elif request.topic == "B":
                    lockTopicB.acquire()
                    self.messagesTopicB.append(newMessage)
                    lockTopicB.release()
                elif request.topic == "C":
                    lockTopicC.acquire()
                    self.messagesTopicC.append(newMessage)
                    lockTopicC.release()
                #Enviar el msj.
                print(" New Message posted: " + request.text)
                return sender.PostResponse(postedResponse = True, textResponse = "Successfully posted.")
            else:
                return sender.PostResponse(postedResponse = False, textResponse = "You are not subscribed to that topic.")
        return sender.PostResponse(postedResponse = False, textResponse = "Error. Try again.")
    
    def SendMessage(self, message):
        return 0

    def ListenToTopic(self, request, context):
        return sender.ListenResponse(lisResponse = "Success")
    
    def StopListenToTopic(self, request, context):
        return sender.StopListenResponse(stopLisResponse = "Success")

def runServer():
    serverInstance = Server()
    serverGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    serverProto.add_SubscribeServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_PostIntoTopicServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_LoginServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_ListeningServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_StopListeningServiceServicer_to_server(serverInstance, serverGrpc)
    serverGrpc.add_insecure_port('[::]:50051')
    serverGrpc.start()
    print(" Initialized gRPC server in port 50051")
    serverGrpc.wait_for_termination()

if __name__ == '__main__':
    runServer()





