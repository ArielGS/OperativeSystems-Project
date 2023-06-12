import copy
import grpc
import pickle
import threading
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as serverProto
from datetime import datetime
from concurrent import futures
from Logic.Client import Client
from Logic.Message import Message

cond = threading.Condition()
lockMain = threading.Lock()
lockTopicA = threading.Lock()
lockTopicB = threading.Lock()
lockTopicC = threading.Lock()
sessions = 0

def saveClients(clients):
    with open("Clients/clients.pickle", "wb") as file:
        pickle.dump(clients, file)

def addEventLog(event):
    previous = ""
    try:
        with open('Logs/log.txt', 'a') as file:
            file.write(previous + '\n' + event)
    except Exception as e:
        print("Error by adding event to the log:", str(e))

def saveMessagesQueue(queueMessages, topic):
    try:
        with open("ServerMessages/queueTopic" + topic + ".pickle", "wb") as file:
            pickle.dump(queueMessages, file)
    except Exception as e:
        print("Error by adding queue:", str(e))

def getTime():
    now = datetime.now()
    dateString = now.strftime("%Y-%m-%d - %H:%M:%S")
    return dateString

class Server(serverProto.LoginServiceServicer, serverProto.SubscribeServiceServicer, 
             serverProto.PostIntoTopicServiceServicer, serverProto.ListeningServiceServicer, 
             serverProto.StopListeningServiceServicer, serverProto.CallDequeueServiceServicer):
    def __init__(self):
        self.messagesTopicA = []
        self.messagesTopicB = []
        self.messagesTopicC = []
        self.clients = {}
        
        try:
            with open('Clients/clients.pickle', 'rb') as file:
                self.clients = pickle.load(file)
                for client in self.clients:
                    self.clients[client].listening = "None"       
        except (FileNotFoundError):
            pass
        
        try:
            with open("ServerMessages/queueTopicA.pickle", "rb") as file:
                self.messagesTopicA = pickle.load(file)
        except:
            pass

        try:
            with open("ServerMessages/queueTopicB.pickle", "rb") as file:
                self.messagesTopicB = pickle.load(file)
        except:
            pass

        try:
            with open("ServerMessages/queueTopicC.pickle", "rb") as file:
                self.messagesTopicC = pickle.load(file)
        except:
            pass

    def LoginIntoApp(self, request, context):
        global sessions
        if self.clients.get(request.username) is not None:
            lockMain.acquire()
            self.clients[request.username].state = True
            self.clients[request.username].idNumber = sessions
            sessions = sessions + 1
            
            addEventLog(" " + getTime() + ": Client " + request.username + " succesfully logged. \n")
            lockMain.release()
        else:
            lockMain.acquire()
            self.clients[request.username] = Client(request.username, True)
            self.clients[request.username].idNumber = sessions
            sessions = sessions + 1
            saveClients(self.clients)
            addEventLog(" " + getTime() + ": Client " + request.username + " succesfully registered and logged. \n")
            lockMain.release()
        return sender.LoginResponse(topics=self.clients[request.username].subscribed, idNumber=sessions-1)
    
    def SubcribeToTopic(self, request, context):
        if self.clients.get(request.client) is not None:
            lockMain.acquire()
            client = self.clients[request.client]
            client.subscribe(request.topic)
            saveClients(self.clients)
            addEventLog(" " + getTime() + ": Client " + request.client + " subscribed to topic " + request.topic + ".\n")
            lockMain.release()
            return sender.SubscribeResponse(subsResponse=True)
        return sender.SubscribeResponse(subsResponse=False)
    
    def PostIntoTopic(self, request, context):
        if self.clients.get(request.publisher) is not None:
            current = self.clients[request.publisher]
            if request.topic in current.subscribed:
                newMessage = Message(request.text, request.topic, request.publisher, None)
                if request.topic == "A":
                    if 100-len(self.messagesTopicA) >= len(self.clients):
                        if self.SendMessage(newMessage):
                            addEventLog(" " + getTime() + ": " + request.publisher + " posted in topic " + request.topic + ": " + request.text  + "\n")
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue. Try later")
                elif request.topic == "B":
                    if 100-len(self.messagesTopicB) >= len(self.clients):
                        if self.SendMessage(newMessage):
                            addEventLog(" " + getTime() + ": " + request.publisher + " posted in topic " + request.topic + ": " + request.text  + "\n")
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue.")
                elif request.topic == "C":
                    if 100-len(self.messagesTopicC) >= len(self.clients):
                        if self.SendMessage(newMessage):
                            addEventLog(" " + getTime() + ": " + request.publisher + " posted in topic " + request.topic + ": " + request.text  + "\n")
                            return sender.PostResponse(postedResponse = True, textResponse = " Successfully posted.")
                    else:
                        return sender.PostResponse(postedResponse = False, textResponse = " Not enough space in messages queue.")
            else:
                return sender.PostResponse(postedResponse = False, textResponse = " You are not subscribed to that topic.")
        return sender.PostResponse(postedResponse = False, textResponse = " Error. Try again.")

    def SendMessage(self, message):
            try:
                for client in self.clients:
                    client = self.clients[client]
                    if message.topic in client.subscribed:
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
                                copiedMessage = copy.copy(message)
                                self.messagesTopicA.append(copiedMessage)
                                saveMessagesQueue(self.messagesTopicA, "A")
                                lockTopicA.release()
                            elif message.topic == "B":
                                lockTopicB.acquire()
                                copiedMessage = copy.copy(message)
                                self.messagesTopicB.append(copiedMessage)
                                saveMessagesQueue(self.messagesTopicB, "B")
                                lockTopicB.release()
                            elif message.topic == "C":
                                lockTopicC.acquire()
                                copiedMessage = copy.copy(message)
                                self.messagesTopicC.append(copiedMessage)
                                saveMessagesQueue(self.messagesTopicC, "C")
                                lockTopicC.release()
                return True
            except (Exception):
                return False

    def DeQueueMessages(self, request):
        try:
            current = self.clients[request.username]
            if request.topic == "A":
                for i in range(len(self.messagesTopicA)):
                    lockTopicA.acquire()
                    message = self.messagesTopicA.pop(0)
                    if message.consumer == current.name and message.topic == current.listening:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                        try:
                            response = remoteCall.RecieveMessage(request)
                            if(response.reciResponse == "Success"):
                                addEventLog(" " + getTime() + ": Message from topic " + message.topic + " to client " + current.name + " has been dequeued.\n")
                        except (Exception):
                            self.messagesTopicA.append(message)
                    else:
                        self.messagesTopicA.append(message)
                    saveMessagesQueue(self.messagesTopicA, "A")
                    lockTopicA.release()
            elif request.topic == "B":
                for i in range(len(self.messagesTopicB)):
                    lockTopicB.acquire()
                    message = self.messagesTopicB.pop(0)
                    if message.consumer == current.name and message.topic == current.listening:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher + "\n")
                        try:
                            response = remoteCall.RecieveMessage(request)
                            if(response.reciResponse == "Success"):
                                addEventLog(" " + getTime() + ": " + request.publisher + " posted in topic " + request.topic + ": " + request.text + "\n")
                        except (Exception):
                            self.messagesTopicB.append(message)
                    else:
                        self.messagesTopicB.append(message)
                    saveMessagesQueue(self.messagesTopicB, "B")
                    lockTopicB.release()
            elif request.topic == "C":
                for i in range(len(self.messagesTopicC)):
                    lockTopicC.acquire()
                    message = self.messagesTopicC.pop(0)
                    if message.consumer == current.name and message.topic == current.listening:
                        port = f'localhost:{50052 + current.idNumber}'
                        channel = grpc.insecure_channel(port)
                        remoteCall = serverProto.RecieveMessageServiceStub(channel)
                        request = sender.RecieveMessageRequest(text=message.text, topic=message.topic, publisher=message.publisher)
                        try:
                            response = remoteCall.RecieveMessage(request)
                            if(response.reciResponse == "Success"):
                                addEventLog(" " + getTime() + ": " + request.publisher + " posted in topic " + request.topic + ": " + request.text + "\n")
                        except (Exception):
                            self.messagesTopicC.append(message)
                    else:
                        self.messagesTopicC.append(message)
                    saveMessagesQueue(self.messagesTopicC, "C")
                    lockTopicC.release()
        except (Exception):
            return False
        return True

    def ListenToTopic(self, request, context):
        lockMain.acquire()
        self.clients[request.username].listening = request.topic
        addEventLog(" " + getTime() + ": " + request.username + " is listening to Topic " + request.topic + " messages.\n")
        lockMain.release()
        return sender.ListenResponse(lisResponse = "Success")
    
    def StopListenToTopic(self, request, context):
        lockMain.acquire()
        self.clients[request.username].listening = None
        addEventLog(" " + getTime() + ": " + request.username + " stopped listening to any topic messages.\n")
        lockMain.release()
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
    addEventLog(" " + getTime() + ": " + "Initialized gRPC server in port 50051.\n")
    serverGrpc.wait_for_termination()

if __name__ == '__main__':
    runServer()





