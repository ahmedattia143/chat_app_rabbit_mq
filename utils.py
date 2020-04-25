import pika
import tkinter as tk
#defining customized text to detect any modification on text 

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


#function to send when <TextModified> event generated
def send_to_rabbit(x,sender):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=sender)
    
    channel.basic_publish(exchange='',
                        routing_key=sender,
                        body=x)

    connection.close()

#function to read from kyou

"""def read_rabbit(kyou):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=kyou)
    

    channel.basic_consume(queue=kyou,
                      auto_ack=True,
                      on_message_callback=callback1)"""



#connect to N qeues

"""def connect_kyouz(kyouz):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    for kyou in kyouz:
        channel.queue_declare(queue=kyou)"""
