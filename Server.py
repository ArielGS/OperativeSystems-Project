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
             serverProto.PostIntoTopicServiceServicer, serverProto.ListeningServiceServicer, 
             serverProto.StopListeningServiceServicer, serverProto.CallDequeueServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = {}
        try:
            with open('clients.pickle', 'rb') as file:
                self.clients = pickle.load(file)
        except (FileNotFoundError):
            pass

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
                    if 100-len(self.messagesTopicA) >= len(self.clients)-activeUsers:
                        if self.SendMessage(newMessage):
                            print(" New Message posted: " + request.text)
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue. Try later")
                elif request.topic == "B":
                    if 100-len(self.messagesTopicB) >= len(self.clients)-activeUsers:
                        if self.SendMessage(newMessage):
                            print(" New Message posted: " + request.text)
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue.")
                elif request.topic == "C":
                    if 100-len(self.messagesTopicC) >= len(self.clients)-activeUsers:
                        if self.SendMessage(newMessage):
                            print(" New Message posted: " + request.text)
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue.")
            else:
                return sender.PostResponse(postedResponse = False, textResponse = " You are not subscribed to that topic.")
        return sender.PostResponse(postedResponse = False, textResponse = " Error. Try again.")

    def SendMessage(self, message):
            for client in self.clients:
                client = self.clients[client]
                message.consumer = client.name
                if client.listening == message.topic:
                    port = f'localhost:{50052 + client.idNumber}'
                    channel = grpc.insecure_channel(port)
                    remoteCall = serverProto.RecieveMessageServiceStub(channel)
                    request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                    response = remoteCall.RecieveMessage(request)
                    
                else:
                    if message.topic == "A":
                        lockTopicA.acquire()
                        self.messagesTopicA.append(message)
                        lockTopicA.release()
                    elif message.topic == "B":
                        lockTopicB.acquire()
                        self.messagesTopicB.append(message)
                        lockTopicB.release()
                    elif message.topic == "C":
                        lockTopicC.acquire()
                        self.messagesTopicC.append(message)
                        lockTopicC.release()
            return True

    def DeQueueMessages(self, request):
        try:
            current = self.clients[request.username]
            if request.topic == "A":
                for i in range(len(self.messagesTopicA)):
                    lockTopicA.acquire()
                    message = self.messagesTopicA.pop()
                    if message.consumer == current.name:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                        try:
                            response = remoteCall.RecieveMessage(request)
                        except (Exception):
                            self.messagesTopicA.append(message)
                    else:
                        self.messagesTopicA.append(message)
                    lockTopicA.release()
            elif request.topic == "B":
                for i in range(len(self.messagesTopicA)):
                    lockTopicA.acquire()
                    message = self.messagesTopicA.pop()
                    if message.consumer == current.name:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                        try:
                            response = remoteCall.RecieveMessage(request)
                        except (Exception):
                            self.messagesTopicA.append(message)
                    else:
                        self.messagesTopicA.append(message)
                    lockTopicA.release()
            elif request.topic == "C":
                for i in range(len(self.messagesTopicA)):
                    lockTopicA.acquire()
                    message = self.messagesTopicA.pop()
                    if message.consumer == current.name:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                        try:
                            response = remoteCall.RecieveMessage(request)
                        except (Exception):
                            self.messagesTopicA.append(message)
                    else:
                        self.messagesTopicA.append(message)
                    lockTopicA.release()
        except (Exception):
            return False
        return True

    def ListenToTopic(self, request, context):
        self.clients[request.username].listening = request.topic
        return sender.ListenResponse(lisResponse = "Success")
    
    def StopListenToTopic(self, request, context):
        self.clients[request.username].listening = None
        return sender.StopListenResponse(stopLisResponse = "Success")
    
    def CallDequeueMessages(self, request, context):
        if self.DeQueueMessages(request):
            return sender.ListenResponse(lisResponse = "Success")
        else:
            return sender.ListenResponse(lisResponse = "Failed")

def runServer():
    serverInstance = Server()
    serverGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    serverProto.add_SubscribeServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_PostIntoTopicServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_LoginServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_ListeningServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_StopListeningServiceServicer_to_server(serverInstance, serverGrpc)
    serverProto.add_CallDequeueServiceServicer_to_server(serverInstance, serverGrpc)
    serverGrpc.add_insecure_port('[::]:50051')
    serverGrpc.start()
    print(" Initialized gRPC server in port 50051")
    serverGrpc.wait_for_termination()

if __name__ == '__main__':
    runServer()





