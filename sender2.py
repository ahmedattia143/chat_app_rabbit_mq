from utils import send_to_rabbit,CustomText
import tkinter as tk
import threading 
import pika 

#callback when sender 2 change something 
def callback(ch, method, properties, body):
    text2.delete(1.0,'end')
    text2.insert(1.0,body)

    """tx2.delete(1.0,'end')
    tx2.insert(1.0,body)

"""
def onmodif(event):
    arg1 = text1.get(1.0,'end')
    send_to_rabbit(arg1,"sender1")
    send_to_rabbit(arg1,"receiver2")



root = tk.Tk()
root.title("sender2")
text1 = CustomText(root,height = 10,width = 50)
text1.grid(row=0,column=0)
text1.bind("<<TextModified>>", lambda e: onmodif(e) )





#field text for the other user 
text2 = tk.Text(root,height=10,width = 50)
text2.grid(row=1,column=0)
text2.bind("<Key>", lambda e: "break")




# connection to queus
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sender2')
channel.basic_consume(queue='sender2',
                      auto_ack=True,
                      on_message_callback=callback)



# defining thread to consume 
def consume():
    channel.start_consuming()
x1 = threading.Thread(target =consume )


    

#running thread to detect changes 
x1.start()


#looping 
root.mainloop()