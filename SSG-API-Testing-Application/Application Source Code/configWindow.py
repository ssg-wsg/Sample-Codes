import json
from os import makedirs
import os
from AdditionalFunction import loadFile, saveJsonFormat
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter
from resources import config_path

def displayFileLabel(window ,filePath, type):
    global pathName, certPemPath
    if (type == "cert"):
        entries[2].clear_text()
        entries[2].insert_text(filePath)
    else :
        entries[3].clear_text()
        entries[3].insert_text(filePath)


    

#This method is used to saved the local Certificate Pem file path in a local variable 
def getCertPemFile(window):
    filePath=filedialog.askopenfilename()
    displayFileLabel(window, filePath, "cert")


#This method is used to saved the local Key Pem file path in a local variable 
def getKeyPemFile(window):
    filePath=filedialog.askopenfilename()
    displayFileLabel(window, filePath,"key")


#This class open a new window  to allow User to input the required parameters for mandate API
class setConfigWindow(Toplevel):
    global entries
    entries = []
    def __init__(self, master = None):      
        
        super().__init__(master = master)
        self.title("Configuration Window")
        self.geometry("470x180+200+200")
        self.resizable(False,False)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0)
        for field in 'UEN', 'Encryption Key', 'Certificate Pem File', 'Key Pem File':
            if field == 'Certificate Pem File':
                button = tk.Button(self,text="Browse", command=lambda:getCertPemFile(self))
                entries.append(LabelEntry(frame, field, button))
            elif field =='Key Pem File':
                button = tk.Button(self,text="Browse", command=lambda:getKeyPemFile(self))
                entries.append(LabelEntry(frame, field, button))

            else:
                entries.append(LabelEntry(frame, field))
        saveButtonFrame(frame)
        def disable_event():
            global entries
            entries = []
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", disable_event)
        

class saveButtonFrame(tkinter.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.pack(fill=tk.X)
        okButton = Button(self, text="Save", command=lambda:storeAndsave_all(), width=60)
        okButton.pack(side=RIGHT,padx=5, pady=5)


class LabelEntry(tkinter.Frame):
    def __init__(self, parent, text, button=None):
        super().__init__(parent)
        self.pack(fill=tk.X)

        placeholder = loadFile(config_path)
        placeholder = json.loads(placeholder)
        UENPlaceholder = placeholder["UEN"]
        KeyPlaceholder = placeholder["key"]
        CertPlaceHolder = placeholder["certPath"]
        KeyPlaceHolder = placeholder["keyPath"]
        lbl = tk.Label(self, text=text, width=14, anchor='w')
        lbl.pack(side=tk.LEFT, padx=5, pady=5)
        if button:
            
            self.frame2 = tk.Frame(self)
            self.frame2.pack(side=tk.LEFT, expand=True)

            textPlaceholder = StringVar(self, value=CertPlaceHolder) if text == 'Certificate Pem File' else StringVar(self, value=KeyPlaceHolder)
            self.entry = tk.Entry(self.frame2, width=45,textvariable = textPlaceholder) 
            self.entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

            button.pack(in_=self.frame2, side=tk.LEFT, padx=5, pady=5)
        else:
            textPlaceholder = StringVar(self, value=UENPlaceholder) if text == 'UEN' else StringVar(self, value=KeyPlaceholder)
            self.entry = tk.Entry(self, width=30, textvariable = textPlaceholder) 
            self.entry.pack(side=tk.LEFT, fill=tk.X, padx=5)

    #This two methods are used for Cert and Key File Upload
    def clear_text(self):
        self.entry.delete(0, tkinter.END)

    def insert_text(self,text):
        self.entry.insert(1, text)

        
def storeAndsave_all():
    global entries
    #load config File
    configInfo = loadFile(config_path)
    configInfoJson = json.loads(configInfo)

    configInfoJson["UEN"] = entries[0].entry.get()
    configInfoJson["key"] = entries[1].entry.get()
    configInfoJson["certPath"] = entries[2].entry.get()
    configInfoJson["keyPath"] = entries[3].entry.get()
    #Save config File
    saveJsonFormat(configInfoJson, config_path)
    entries = entries
    tkinter.messagebox.showinfo(title="Success", message="Configuration Information Successfully Saved")
    
 

#This class open a new window  to show the current input value in the required for mandate API
class showConfigWindow(Toplevel):
    def __init__(self, master = None):       
        super().__init__(master = master)
        self.title("Configuration Window")
        self.geometry("600x200")
        self.resizable(False,False)
        self.displayConfigInfo()

    def displayConfigInfo(frame):

        #Load Config Infomation
        configData = loadFile(config_path)
        configData = json.loads(configData)
        

        #Display Config Information
        Fact = "UEN: " + configData["UEN"] + "\nKey: " + configData["key"] + "\nCert Path: " + configData["certPath"] + "\nKey Path: " + configData["keyPath"]
        T = Text(frame, height = 7, width = 70)
        l = Label(frame, text = "Configuration Information")
        l.config(font =("Courier", 12))
        l.pack(pady=10)  
        T.pack()
        T.insert(tk.END, Fact)
        T.config(state=DISABLED)