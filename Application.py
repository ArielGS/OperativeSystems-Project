from Logic.Topic import Topic
from Logic.Client import Client
from Logic.Message import Message
import gRPC.connection_pb2 as sender
import gRPC.connection_pb2_grpc as server
import os
import time
import grpc

messages = []
currentClient = Client("", "Offline")
channel = grpc.insecure_channel('localhost:50051')

def login():
    success = False
    username = ""

    while not success:
        print("\n ---------- LOGIN CLIENT ----------")
        print("    Please enter your username       ")
        username = input("\n    Username: ")
        os.system('cls')

        if not username == "":
            success = True
            currentClient.name = username
            currentClient.state = "Online"
            remoteCall = server.LoginServiceStub(channel)
            request = sender.LoginRequest(username=currentClient.name)
            response = remoteCall.LoginIntoApp(request)
            if not response == None:
                currentClient.subscribed = response.topics
                print("\n ---------- LOGIN CLIENT ----------")
                print("       Succesfully logged in.  \n")

                input("       Press Enter to continue...      ")
                mainMenu()
            else:
                print(" Incorrect username. Try again.  ")
                input(" Press Enter to continue...      ")
                os.system('cls')
        else:
            print(" Incorrect username. Try again.  ")
            input(" Press Enter to continue...      ")
            os.system('cls')

def logout():
    currentClient.state = "Offline"
    #Enviar señal a servidor para apagar hilo y
    #desactivar el worker / hilo 
    print("Leaving Session...")

def topicsMenu():
    print("\n ----- CHOOSE A TOPIC -----")

    print("       1. TOPIC A            ")
    print("       2. TOPIC B            ")
    print("       3. TOPIC C            ")
    print("       4. Exit               ")

def subscribeMenu():
    topicsMenu()
    option = input("\n      Option:    ")
    topicSelected = ""
    os.system('cls')

    if   option == "1": topicSelected = "A"
    elif option == "2": topicSelected = "B"
    elif option == "3": topicSelected = "C"
    elif option == "4": return
    else:
        print(" Unvalid option. Try again.")
        input(" Press Enter to continue...")
        return

    currentClient.subscribe(topicSelected)
    remoteCall = server.SubscribeServiceStub(channel)
    request = sender.SubscribeRequest(topic=topicSelected, client=currentClient.name)
    response = remoteCall.SubcribeToTopic(request)

    if(response.subsResponse == True):
        print("Successfully subscribed to TOPIC " + topicSelected)
    else:
        print("Something went wrong. Try again.")
        
    time.sleep(2)

def postInTopic():
    exit = ""
    topicSelected = ""
    message = ""

    while exit != "y":
        topicsMenu()
        option = input("\n      Option:    ")
        
        os.system('cls')

        if   option == "1": topicSelected = "A"
        elif option == "2": topicSelected = "B"
        elif option == "3": topicSelected = "C"
        elif option == "4": return
        else:
            print(" Unvalid option. Try again.")
            input(" Press Enter to continue...")
            continue
        
        print("\n ----- POST IN TOPIC " + topicSelected + " -----")
        message = input("\n Post message: ")
       
        remoteCall = server.PostIntoTopicServiceStub(channel)
        request = sender.PostRequest(text=message, topic=topicSelected, publisher=currentClient.name)
        response = remoteCall.PostIntoTopic(request)
        
        print(response.textResponse)
        
        exit = input("\n Exit? y/n : ")

        os.system('cls')

def watchTopicPosts():
    exit = ""
    topicSelected = ""
    while exit != "y":
        topicsMenu()
        option = input("\n      Option:    ")
        
        os.system('cls')

        if   option == "1": topicSelected = "A"
        elif option == "2": topicSelected = "B"
        elif option == "3": topicSelected = "C"
        elif option == "4": return
        else:
            print(" Unvalid option. Try again.")
            input(" Press Enter to continue...")
            continue
        
        print("\n ----- POSTS IN TOPIC" + topicSelected + " -----")
            # Se piden los posts de un topico y se pone a a escuchar 
            # si llegan nuevos mensajes (hay que usar hilos)
        exit = input("\n Exit? y/n : ")

        os.system('cls')

def mainMenu():
    while currentClient.state == "Online":
        os.system('cls')
        print("\n ----------- MAIN MENU ------------")
        print("      1. Subscribe into topic        ")
        print("      2. Post into a topic           ")
        print("      3. View topic posts            ")
        print("      4. Log out                     ")

        option = input("\n      Option: ")
        os.system('cls')

        if option == "1":
            subscribeMenu()

        elif option == "2":
            postInTopic()

        elif option == "3":
            watchTopicPosts()

        elif option == "4":
            logout()
            print(" Exiting the application...")
            input(" Press Enter to continue...")
            break

        else:
            print(" Unvalid option. Try again.")
            input(" Press Enter to continue...")

if __name__ == "__main__":
    os.system('cls')
    login()