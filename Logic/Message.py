class Message:
    def __init__(self, text, topic, publisher, consumer):
        self.text = text
        self.topic = topic
        self.publisher = publisher
        self.consumer = consumer
