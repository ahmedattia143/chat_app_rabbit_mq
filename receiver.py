import threading
import pika 
import tkinter as tk


# callbacks on consuming
def callback1(ch, method, properties, body):
    tx1.delete(1.0,'end')
    tx1.insert(1.0,body)

def callback2(ch, method, properties, body):
    tx2.delete(1.0,'end')
    tx2.insert(1.0,body)


# defining thread to consume 
def consume():
    channel.start_consuming()

# connection to queus
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='receiver1')
channel.queue_declare(queue='receiver2')

channel.basic_consume(queue='receiver2',
                      auto_ack=True,
                      on_message_callback=callback2)

channel.basic_consume(queue='receiver1',
                      auto_ack=True,
                      on_message_callback=callback1)




x1 = threading.Thread(target =consume )
    


# now define the gui for the sender 

root = tk.Tk()
root.title("receiver")

tx1 = tk.Text(root,height = 50,width = 30)
tx1.grid(row=0,column=0)

tx2 = tk.Text(root,height=50,width = 30)
tx2.grid(row=0,column=1)



#running thread to consume 
x1.start()

#looping 
root.mainloop()

#stop thread 
