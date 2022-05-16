from tkinter import *
from tkinter import ttk
from client import Client
import threading

class UI:
    def __init__(self):
        self.client = Client()
        self.client.clientStartConnection()
        self.client.clientHandshake()
        self.mainWindow = Tk()
        self.mainWindow.withdraw()
        self.usernameWindow = Toplevel()
        self.usernameWindow.title("Enter username")
        self.usernameWindow.configure(width = 200, height = 100)
        self.usernameEntry = Entry(self.usernameWindow)
        self.usernameEntry.place(relwidth = 1, relheight = 0.2)
        self.usernameEntry.focus()
        self.startButton = Button(self.usernameWindow, text = "Start", command = lambda: self.goToMainWindow(self.usernameEntry.get()))
        self.startButton.place(relx = 0.5, rely = 0.7)
        self.mainWindow.mainloop()

    def goToMainWindow(self, name):
        rcv = threading.Thread(target=self.receive)
        rcv.start()
        print("Start window --> ")
        self.usernameWindow.destroy()
        self.name = name
        self.client.clientSetUsername(name)
        self.layout()

    def layout(self):
        self.mainWindow.deiconify()
        self.mainWindow.title("Room")
        self.mainWindow.configure(width = 500, height = 600)
        self.textCons = Text(self.mainWindow, width = 20, height = 2, padx = 5, pady = 5)
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.textCons.yview)
        self.textCons.config(state = DISABLED)
        self.labelBottom = Label(self.mainWindow, height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)
        self.entryMsg = Entry(self.labelBottom)
        self.entryMsg.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)
        self.entryMsg.focus()
        self.buttonMsg = Button(self.labelBottom, text = "Send", width = 20, command = lambda : self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)

    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target = self.sendMessage)
        snd.start()

    def receive(self):
        message = self.client.clientEventLoop()
        self.textCons.config(state = NORMAL)
        self.textCons.insert(END, message.decode('utf-8')+"\n\n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        message = (f"{self.name}: {self.msg}")
        self.client.clientSendMessage(message.encode('utf-8'))

        self.textCons.config(state = NORMAL)
        self.textCons.insert(END, message+"\n\n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)

g = UI()