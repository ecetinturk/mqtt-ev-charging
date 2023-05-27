#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
"""
Creates multiple Connections to a broker 
and sends and receives messages. Support SSL and Normal connections
uses the loop_start and stop functions just like a single client
Shows number of thread used
"""
import paho.mqtt.client as mqtt
import time
import json
import threading
import logging
broker="127.0.0.1"
port =1884
ssl_port=8883 #ssl

Normal_connections=5
SSL_Connections=0 #no ssl connections illustration only
message="test message"
topic="BATTERY"
out_queue=[] #use simple array to get printed messages in some form of order
def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   time.sleep(1)
   msg="message received",str(message.payload.decode("utf-8"))
   #print(msg)
   out_queue.append(msg)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        client.subscribe(topic)
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  
def on_disconnect(client, userdata, rc):
   pass
   #print("client disconnected ok")
def on_publish(client, userdata, mid):
   time.sleep(1)
   print("In on_pub callback mid= "  ,mid)


def Create_connections(nclients,port,SSL_Flag=False):
   for i in range(nclients):
      if SSL_Flag:
         cname ="python-ssl"+str(i)
      else:
         cname ="python-"+str(i)
      client = mqtt.Client(cname)             #create new instance

      if SSL_Flag:
         client.tls_set('c:/python34/steve/MQTT-demos/certs/ca-pi.crt')
      #client.connected_flag=False #create flag in client

      client.connect(broker,port)           #establish connection
      #client.on_log=on_log #this gives getailed logging
      client.on_connect = on_connect
      client.on_disconnect = on_disconnect
      #client.on_publish = on_publish
      client.on_message = on_message
      clients.append(client)
      client.loop_start()
      while not client.connected_flag:
         time.sleep(0.05)


mqtt.Client.connected_flag=False #create flag in class
clients=[]
no_threads=threading.active_count()
print("current threads =",no_threads)
print("Creating Normal Connections ",Normal_connections," clients")
Create_connections(Normal_connections,port,False)
if SSL_Connections!=0:
   print("Creating SSL Connections ",SSL_Connections," clients")
   Create_connections(SSL_Connections,ssl_port,True)


print("All clients connected ")
time.sleep(5)
#
count =0
no_threads=threading.active_count()
print("current threads =",no_threads)
print("Publishing ")
Run_Flag=True
try:
   while Run_Flag:
      i=0
      for client in clients:
         counter=str(count).rjust(6,"0")
         msg="client "+ str(i) +  " "+counter+"XXXXXX "+message
         client.publish(topic,msg)
         time.sleep(0.1)
         print("publishing client "+ str(i))
         i+=1
      time.sleep(10)#now print messages
      print("queue length=",len(out_queue))
      for x in range(len(out_queue)):
         print(out_queue.pop())
      count+=1
      #time.sleep(5)#wait
except KeyboardInterrupt:
   print("interrupted  by keyboard")

#client.loop_stop() #stop loop
for client in clients:
   client.disconnect()
   client.loop_stop()
#allow time for allthreads to stop before existing
time.sleep(10)


