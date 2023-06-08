class Client:
    def __init__(self, name, state):
        self.name = name
        self.state = state
        self.subscribed = []

    def subscribe(self, topic):
        self.subscribed.append(topic)
    
    def unsubscribe(self, topic):
        self.subscribed.remove(topic)
