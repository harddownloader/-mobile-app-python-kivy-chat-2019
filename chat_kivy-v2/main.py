from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from datetime import datetime
import time
import socket

from kivy.lang import Builder

import request

Builder.load_string("""
#:kivy 1.10.0
 
<BoxWidget>:
    orientation: 'vertical'
    display: display
    chat: chat
    gethost: gethost
    getport: getport
    Label:
        id: display
        text: 'Hello Player'
    TextInput:
        id: gethost
        size_hint: None, None
        size: 125, 35
        text: '127.0.0.1'
    TextInput:
        id: getport
        size_hint: None, None
        size: 125, 35
        text: '5000'
    TextInput:
        id: chat
        size_hint_y: None
        size_y: 20
    BoxLayout:
        Button:
            text: 'Connect'
            on_press: root.connect()
        Button:
            text: 'Listen'
            on_press: root.listen_bind()
        Button:
            text: 'Send'
            on_press: root.send()
""")
class BoxWidget(BoxLayout):
    display = ObjectProperty()
    chat = ObjectProperty()
    gethost = ObjectProperty()
    getport = ObjectProperty()
 
    # If set to true, this will create an AttributeError because its partner self.client hasn't been set while receive() was called
    is_server = False
 
    # These values are user-entered from the kivy text inputs
    host = ''
    port = ''                
    socket = socket.socket()
 
    # The connection is returned to this if acting as a server
    client = None
 
 
    def connect(self):
        '''Connecting as a Client'''
 
        # Setting self to Client
        self.is_server = False
 
        # Grabbing host & port from user input
        self.host = self.gethost.text
        self.port = self.getport.text
 
        # Error will occur if port text isn't converted to int from str.
        self.port = int(self.port)
 
        # Connecting
        self.socket.connect((self.host, self.port))
       
 
        # Receiving Confirmation of connection from Server
        confirmation = self.socket.recv(1024).decode()
        self.display.text = str(confirmation)
 
        # Set socket to nonblocking in preparation for a method that checks for data to receive every second. Has to be called after the confirmation message since it isn't wrapped in a try
        self.socket.setblocking(0)
 
           
       
    def listen_bind(self):
        '''Set self to Server. Bind self to host, port, then call listen. This is the function called by the listen button press'''
 
        # Sets self as Server
        self.is_server = True
 
        # Sets socket to nonblocking for future use
        self.socket.setblocking(0)
 
        # Get host, port from user input
        self.host = self.gethost.text
        self.port = self.getport.text
 
        # Convert getport.text to int to again prevent an error occuring
        self.port = int(self.port)
 
        # Bind socket. We call this here so we don't try to repeatedly bind it in in the try of the listen method
        self.socket.bind((self.host, self.port))
 
        # After bound, call listen()
        self.listen()
 
    def listen(self):
        '''Listen as Server'''
        self.socket.listen(1)
       
        try:
           
            # Try to get connection and address of incoming socket
            connection, address = self.socket.accept()
           
            # Confirmation of Connection
            self.display.text = 'Connection from: ' + str(address)
 
            # Send confirmation to connected Client
            confirmation = 'Thank you for connecting'
            connection.send(confirmation.encode())
            # self.receive()
 
            # Set self.client as reference to active connection, so it can be called outside of the listen method
            self.client = connection
           
        except:
            # Print Error Message if failed
            print('Failed')
            print('Trying again')
 
            # Try again in half a second
            time.sleep(.5)
            self.listen()
       
    def send(self):
        '''Called by a Kivy Button. Sends a Message to the connected Machine'''
 
        # if self is Server, execute this:
        if self.is_server:
           
            # Define mail as text in Chat TextInput Box
            mail = self.chat.text
 
            # Set display.text to previous messages + your message with your name in front of it
            self.display.text = self.display.text + '\nYou: ' + self.chat.text
 
            # Encode mail and send it to the Client
            self.client.send(mail.encode())
 
            # Clear the chat text box allowing for faster messaging
            self.chat.text = ''
 
            # print confirmation of sending mail
            print('Mail sent to Client!')
           
        # if self is Client, execute this:
        elif not self.is_server:
           
            # Define as Text in chat TextInputBox
            mail = self.chat.text
 
            # Set display.text to previous messages + your message with your name in front of it
            self.display.text = self.display.text + '\nYou: ' + self.chat.text
 
            # Encode mail and send it to the Server
            self.socket.send(mail.encode())
 
            # Clear the chat text box allowing for faster messaging
            self.chat.text = ''
 
            # print confirmation of sending mail
            print('Mail Sent to Server!')
 
            # Exists to check if the is_server flag has failed totally
        else:
            print('Flag Check Failed')
 
    def receive(self):
        '''Called repeatedly by the Update function using Kivy's internal clock and dt (delta-time) of the time module. This is the reason for nonblocking sockets'''
 
        # if self is Server, execute this
        if self.is_server:
           
            try:
                # Try to decode mail if there is any
                mail = self.client.recv(1024).decode()
 
                # Add mail followed by Client's name to the display screen
                self.display.text = self.display.text + '\nOpp: ' + str(mail)
 
            # If no mail, pass and wait for the next call
            except socket.error:
                pass
 
        # if self is Client, execute this
        elif not self.is_server:
           
            try:
 
                # Try to decode mail if there is anyway
                mail = self.socket.recv(1024).decode()
 
                # Add mail followed by the Server's name
                self.display.text = self.display.text + '\nOpp: ' + str(mail)
 
            # if no mail, pass and wait for the next call
            except socket.error:
                pass
 
        # Just in case the flags somehow broke all together
        else:
            print('Not Connected?')
 
   
    def update(self, dt):
        '''Called by Kivy's internal Clock repeatedly with dt from time passed as an argument, then calls receive to check for any data from the connected machine'''
        self.receive()
 
class P2PApp(App):
 
    def build(self):
        Box = BoxWidget()
        Clock.schedule_interval(Box.update, 1)
        return Box
 
if __name__ == '__main__':
    P2PApp().run()