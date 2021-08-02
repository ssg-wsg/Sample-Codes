from resources import *
from tkinter.constants import CENTER, END, INSERT
from EncryptAndDecryptFunction import doEncryption
import tkinter as tk
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar, ttk, scrolledtext
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
from EnrolmentFunction import curlGetRequestViewEnrolment, getEnrolment, getDeleteEnrolmentPayLoad, cancelEnrolment,curlPostRequest
from courseRunFunctions import getDeleteCourseRunPayLoad
import json
from tooltip import CreateToolTip

#Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)
#Global method for this File - This method allow copy and paste but not editing textbox
def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

# ViewEnrolment Page
class viewEnrolmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Setting of Variable
        self.textPayload = ''

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="View Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_EnrolRefNum = Label(self, text="Enrolment Reference Number*", width=22, font=("bold", 10), anchor='w')
        label_EnrolRefNum.place(x=100, y=130)
        label_EnrolRefNum_ttp = CreateToolTip(label_EnrolRefNum, tooltipDescription["EnrolRefNum"])
        entry_1 = Entry(self)
        entry_1.place(x=280, y=132)

        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(event):
            value = curlGetRequestViewEnrolment(entry_1.get())
            curlText.delete("1.0", "end")
            curlText.insert(tk.END, value)

        entry_1.bind('<KeyRelease>', typing)

        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        responseFrame = ttk.Frame(tabControl)
        curlFrame = ttk.Frame(tabControl)

        tabControl.add(curlFrame, text='Request')
        tabControl.add(responseFrame, text='Reponse')

        tabControl.place(width=440, height=460, x=30, y=222)

        # Textbox for response Frame
        responseText = scrolledtext.ScrolledText(responseFrame, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", txtEvent)

        # Textbox for Curl Frame
        curlText = scrolledtext.ScrolledText(curlFrame, width=70, height=30)
        curlText.insert(tk.END, str(curlGetRequestViewEnrolment("")))
        curlText.place(height=405, width=440, y=20)
        curlText.bind("<Key>", txtEvent)

        self.varResp = IntVar()
        Radiobutton(responseFrame, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w', command = lambda:displayResp("decrypt")).place(x=0,y=-5)
        Radiobutton(responseFrame, text="Encrypt", variable=self.varResp, value=2,width=12, anchor='w',command = lambda:displayResp("encrypt")).place(x=130,y=-5)
        self.varResp.set(1)

        # adding of single line text box
        edit = Entry(self, background="light gray")

        # positioning of text box
        edit.place(x=285, height=21, y=244)

        # setting focus
        edit.focus_set()

        butt = Button(responseFrame, text='Find', command=lambda: find("resp"), highlightthickness=0, bd=0,
                      background="gray")
        butt.place(x=380, y=0, height=21, width=60)
        butt_curl = Button(curlFrame, text='Find', command=lambda: find("curl"), highlightthickness=0, bd=0,
                           background="gray")
        butt_curl.place(x=380, y=0, height=21, width=60)

        submitButton = tk.Button(self, text="Submit", bg="white", width=25, pady=5,
                                 command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton = tk.Button(self, text="Export Decrypted Response", bg="white", width=25, pady=5,
                                 command=lambda: downloadFile())
        exportButton.place(relx=0.5, rely=0.95, anchor=CENTER)


        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = viewEnrolmentPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(viewEnrolmentPage.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())

        # This call back method activates two other methods.
        # 1) this method calls the get method in enrolmentFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def submitCallBack():
            responseText.delete("1.0", "end")
            enrolmentRefNo = entry_1.get()
            resp = getEnrolment(enrolmentRefNo)
            viewEnrolmentPage.textPayload = StringVar(self, value=resp)
            responseText.insert(INSERT, viewEnrolmentPage.textPayload.get())
            tabControl.select(responseFrame)

        def downloadFile():
            files = [('JSON', '*.json'),
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
            filetext = str(responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = curlText
            # remove tag 'found' from index 1 to END
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

    def show_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)


# Delete Enrolment Page
class deleteEnrolmentPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #variable
        self.textPayload = ''
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        label_0 = Label(self, text="Delete Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        # Enrolment Ref Number
        label_ERN = Label(self, text="Enrolment Reference Number*", width=22, font=("bold", 10), anchor='w')
        label_ERN.place(x=100, y=110)

        entry_ERN = Entry(self)
        entry_ERN.place(x=280, y=110)

        label_ERN_ttp = CreateToolTip(label_ERN, tooltipDescription["EnrolRefNum"])

        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            value = curlPostRequest(entry_ERN.get(), getDeleteEnrolmentPayLoad())
            curlText.delete("1.0", "end")
            curlText.insert(tk.END, value)
            self.varPayload.set(1)
            

        entry_ERN.bind('<KeyRelease>', lambda a: typing())


        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Response')
        tabControl.place(width=440, height=460, x=30, y=222)

        curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        curlText.insert(tk.END, str(curlPostRequest("", getDeleteEnrolmentPayLoad())))
        curlText.place(height=405, width=440, y=20)
        curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        submitButton = tk.Button(self, text="Delete", bg="white", width=25, pady=5,
                                 command=lambda: deleteCallBack(entry_ERN.get()))
        submitButton.place(relx=0.5, rely=0.22, anchor=CENTER)
        exportButton1 = tk.Button(self, text="Export Decrypted Payload", bg="white", width=20, pady=3,
                                  command=lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.95, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Decrypted Response", bg="white", width=20, pady=3,
                                  command=lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.95, anchor=CENTER)

        #Radio button for Request
        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w', command = lambda:displayPayload("decrypt")).place(x=0,y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2,width=12, anchor='w',command = lambda:displayPayload("encrypt")).place(x=130,y=-5)
        self.varPayload.set(1)
        
        #Radio button for Response
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
                    display = deleteEnrolmentPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(deleteEnrolmentPage.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())
                
        def displayPayload(method):
            if method == 'decrypt':
                getDeleteEnrolmentPayLoad()
                curlText.delete("1.0","end")
                curlText.insert(tk.END,curlPostRequest("",getDeleteEnrolmentPayLoad()))
            else:
                curlText.delete("1.0","end")
                curlText.insert(tk.END, curlPostRequest("", str(doEncryption(getDeleteEnrolmentPayLoad().encode()).decode())))

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
            filetext = str(getDeleteCourseRunPayLoad(entry_ERN.get())) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method activates two other methods.
        # 1) this method calls the delete method in enrolmentFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def deleteCallBack(enrolRefNum):
            resp = cancelEnrolment(enrolRefNum)
            responseText.delete("1.0", "end")
            deleteEnrolmentPage.textPayload = StringVar(self, value=resp)
            responseText.insert(tk.END, deleteEnrolmentPage.textPayload.get())
            tabControl.select(tab3)
            self.varResp.set(1)