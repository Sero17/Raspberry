__author__ = 'Raphael'

import logging
import socket

import GUI
import ClientGlobals
from sys import *

def noAction(event):
    print("NO ACTION")
    pass

def buttonleftclick(event):
    logging.debug('Button LEFT click')
    sendMessage('LEFT')
    globalVar.startTiming('LEFT')


def buttonrightclick(event):
    logging.debug('Button RIGHT click')
    sendMessage('RIGHT')
    globalVar.startTiming('RIGHT')


def buttonforwardclick(event):
    logging.debug('Button FORWARD click')
    sendMessage('FORWARD')
    globalVar.startTiming('FORWARD')


def buttonbackwardclick(event):
    logging.debug('Button BACKWARD click')
    sendMessage('BACKWARD')
    globalVar.startTiming('BACKWARD')


def stopMove(event):
    logging.debug('STOP !')
    sendMessage('STOP')

    #Draw line
    GUI.makeMove(globalVar.currentMoveType, globalVar.getDeltaT())


def updatepan(event):
    logging.debug('PAN slider changed :' + str(GUI.sliderpan.get()))
    sendMessage('PAN'+str(GUI.sliderpan.get()))

def updatetilt(event):
    logging.debug('TILT slider changed :' + str(GUI.slidertilt.get()))
    sendMessage('TILT'+str(GUI.slidertilt.get()))

def resetcamera(event):
    GUI.sliderpan.set(0)
    GUI.slidertilt.set(0)
    logging.debug('PAN and TILT reset')
    sendMessage('CAMERA RESET')

def buttontestclick(event):
    logging.debug('Button TEST click')
    GUI.buttonconnect["bg"] = "green"
    GUI.buttonconnect["text"] = "Connected"

def buttonconnectclick(event):
    logging.debug('Button CONNECT click')
    connectSocket()
    if isSocketConnected:
        GUI.buttonconnect["bg"] = "#80ff80"
        GUI.buttonconnect["text"] = "Connected"
    else:
        GUI.buttonconnect["bg"] = "red"
        GUI.buttonconnect["text"] = "Disconnected"

def connectSocket():
    global isSocketConnected
    if isSocketConnected == False:
        try:
            mySocket.connect((HOST, PORT))
            logging.debug('La connection au serveur est etablie')
            isSocketConnected = True
            enableButtons()
        except socket.error:
           logging.error('La connection au serveur a echoue : ' + str(socket.error.strerror))
           isSocketConnected = False
           disableButtons()
    else:
        mySocket.close()
        isSocketConnected = False
        disableButtons()
        logging.debug('La connection au serveur a ete interrompue')


def sendMessage(message):
    global isSocketConnected
    if isSocketConnected:
        message_encode = message.encode("utf_8")
        mySocket.send(message_encode)
        logging.debug("Message envoye : " + str(message_encode))
    else:
        logging.debug("Ce message n'a pas ete envoye : " + str(message))

def enableButtons():
    GUI.buttonleft.bind("<Button-1>", buttonleftclick)
    GUI.buttonright.bind("<Button-1>", buttonrightclick)
    GUI.buttonforward.bind("<Button-1>", buttonforwardclick)
    GUI.buttonbackward.bind("<Button-1>", buttonbackwardclick)
    GUI.buttonstop.bind("<Button-1>", stopMove)
    GUI.sliderpan.bind("<ButtonRelease-1>", updatepan)
    GUI.slidertilt.bind("<ButtonRelease-1>", updatetilt)
    GUI.buttonresetcamera.bind("<Button-1>", resetcamera)
    GUI.buttonleft.bind("<ButtonRelease-1>", stopMove)
    GUI.buttonright.bind("<ButtonRelease-1>", stopMove)
    GUI.buttonforward.bind("<ButtonRelease-1>", stopMove)
    GUI.buttonbackward.bind("<ButtonRelease-1>", stopMove)

    GUI.buttonleft.config(state="normal")
    GUI.buttonright.config(state="normal")
    GUI.buttonforward.config(state="normal")
    GUI.buttonbackward.config(state="normal")
    GUI.buttonstop.config(state="normal")
    GUI.buttonresetcamera.config(state="normal")

def disableButtons():
    GUI.buttonleft.unbind("<Button-1>")
    GUI.buttonright.unbind("<Button-1>")
    GUI.buttonforward.unbind("<Button-1>")
    GUI.buttonbackward.unbind("<Button-1>")
    GUI.buttonstop.unbind("<Button-1>")
    GUI.sliderpan.unbind("<ButtonRelease-1>")
    GUI.slidertilt.unbind("<ButtonRelease-1>")
    GUI.buttonresetcamera.unbind("<Button-1>")

    GUI.buttonleft.unbind("<ButtonRelease-1>")
    GUI.buttonright.unbind("<ButtonRelease-1>")
    GUI.buttonforward.unbind("<ButtonRelease-1>")
    GUI.buttonbackward.unbind("<ButtonRelease-1>")

    GUI.buttonleft.config(state="disabled")
    GUI.buttonright.config(state="disabled")
    GUI.buttonforward.config(state="disabled")
    GUI.buttonbackward.config(state="disabled")
    GUI.buttonstop.config(state="disabled")
    GUI.buttonresetcamera.config(state="disabled")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    # datefmt='%y-%m-%d %H:%M:%S:%',
                    filename='clientGUI.log')

logging.info('Demarrage application')

HOST = '192.168.1.50'  # IP Serveur
PORT = 10000

disableButtons()
# enableButtons()
globalVar = ClientGlobals.globalVar()
GUI.initGraph()

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isSocketConnected = False

GUI.buttonconnect.bind("<Button-1>", buttonconnectclick)

GUI.mainloop()
