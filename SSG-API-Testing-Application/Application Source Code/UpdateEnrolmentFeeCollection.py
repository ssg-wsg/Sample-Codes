from resources import *
from EncryptAndDecryptFunction import doEncryption
import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from EnrolmentFunction import curlPostRequestUpdateEnrolmentFee, getUpdateEnrolmentFeePayLoad, updateEnrolmentFee
import json
from tooltip import CreateToolTip

# Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)

# Update Fee Collection Page
class updateEnrolFeePage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Variables
        self.textPayload = ''
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        label_0 = Label(self, text="Update Enrolment Payment Records", width=28, font=("bold", 20))
        label_0.place(x=30, y=53)

        # Enrolment Ref Number
        label_ERN = Label(self, text="Enrolment Reference Number*", width=22, font=("bold", 10), anchor='w')
        label_ERN.place(x=100, y=110)

        self.entry_ERN = Entry(self)
        self.entry_ERN.place(x=280, y=110)

        label_ERN_ttp = CreateToolTip(label_ERN, tooltipDescription["EnrolRefNum"])

        label_statusCollection = Label(self, text="Fee Status Collection*", width=22, font=("bold", 10), anchor='w')
        label_statusCollection.place(x=100, y=140)

        label_statusCollection_ttp = CreateToolTip(label_statusCollection, tooltipDescription["collectionStatus"])

        self.statusCollection = ttk.Combobox(self, width=27, state="readonly")
        self.statusCollection['values'] = ["Full Payment",
                                           "Pending Payment",
                                           "Partial Payment",
                                           "Cancelled"
                                           ]
        self.statusCollection.current(0)
        self.statusCollection.place(x=280, y=140)


        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            value = curlPostRequestUpdateEnrolmentFee(self.entry_ERN.get(), getUpdateEnrolmentFeePayLoad(self.statusCollection.get()))
            curlText.delete("1.0", "end")
            curlText.insert(tk.END, value)
            self.varPayload.set(1)

        self.entry_ERN.bind('<KeyRelease>', lambda a: typing())
        self.statusCollection.bind("<<ComboboxSelected>>",lambda a: typing())


        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        #Tab 2 refers to Request Tab
        #Tab 3 refers to Response Tab
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Response')
        tabControl.place(width=440, height=460, x=30, y=222)

        curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        curlText.insert(tk.END,
                        str(curlPostRequestUpdateEnrolmentFee("", getUpdateEnrolmentFeePayLoad(self.statusCollection.get()))))
        curlText.place(height=405, width=440, y=20)
        curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        submitButton = tk.Button(self, text="Update", bg="white", width=25, pady=5,
                                 command=lambda: updateFeeCallBack(self.entry_ERN.get()))
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)

        #Exportbutton1 refers to Export Payload
        #Exportbutton2 refers to Export Response
        exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5,
                                  command=lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,
                                  command=lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)
        
        #Radio button for Request
        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w', command = lambda:displayPayload("decrypt")).place(x=0,y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2,width=12, anchor='w',command = lambda:displayPayload("encrypt")).place(x=130,y=-5)
        self.varPayload.set(1)

        #Radio button for Reponse
        self.varResp = IntVar()
        Radiobutton(tab3, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w', command = lambda:displayResp("decrypt")).place(x=0,y=-5)
        Radiobutton(tab3, text="Encrypt", variable=self.varResp, value=2,width=12, anchor='w',command = lambda:displayResp("encrypt")).place(x=130,y=-5)
        self.varResp.set(1)
        # adding of single line text box
        edit = Entry(self, background="light gray")

        # positioning of text box
        edit.place(x=285, height=21, y=244)

        # setting focus
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda: find("curl"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        butt_resp = Button(tab3, text='Find', command=lambda: find("resp"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = updateEnrolFeePage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(updateEnrolFeePage.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())
                
        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = doEncryption(str(getUpdateEnrolmentFeePayLoad(self.statusCollection.get())).encode()).decode()
                curlText.delete("1.0","end")
                curlText.insert(tk.END, str(curlPostRequestUpdateEnrolmentFee(self.entry_ERN.get(),payloadToDisplay)))
            else:
                curlText.delete("1.0","end")
                curlText.insert(tk.END, curlPostRequestUpdateEnrolmentFee(self.entry_ERN.get(), getUpdateEnrolmentFeePayLoad(self.statusCollection.get())))        
        
        # This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = curlText
            textw.tag_remove('found', '1.0', END)

            # returns to widget currently in focus
            s = edit.get()
            if s:
                idx = '1.0'
                while 1:
                    # searches for desried string from index 1
                    idx = textw.search(s, idx, nocase=1,
                                       stopindex=END)
                    if not idx: break

                    # last index sum of current index and
                    # length of text
                    lastidx = '%s+%dc' % (idx, len(s))

                    # overwrite 'Found' at idx
                    textw.tag_add('found', idx, lastidx)
                    idx = lastidx
                    # textw.see(idx)  # Once found, the scrollbar automatically scrolls to the text

                # mark located string as red
                textw.tag_config('found', foreground='red')

            edit.focus_set()

        def downloadFile(method):
            files = [('JSON', '*.json'),
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
            filetext = str(getUpdateEnrolmentFeePayLoad(self.entry_ERN.get())) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method activates two other methods.
        # 1) this method calls the delete method in enrolmentFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def updateFeeCallBack(enrolRefNum):
            resp = updateEnrolmentFee(enrolRefNum)
            responseText.delete("1.0", "end")
            updateEnrolFeePage.textPayload = StringVar(self, value=resp)
            responseText.insert(tk.END, updateEnrolFeePage.textPayload.get())
            tabControl.select(tab3)
