class Client:
    def __init__(self, name, state):
        self.name = name
        self.state = state
        self.subscribed = []
        self.idNumber = 0
        self.listening = None

    def subscribe(self, topic):
        self.subscribed.append(topic)
    
    def unsubscribe(self, topic):
        self.subscribed.remove(topic)

    def listenTopic(self, topic):
        self.listening = topic
    
    def stopListen(self):
        self.listening = None