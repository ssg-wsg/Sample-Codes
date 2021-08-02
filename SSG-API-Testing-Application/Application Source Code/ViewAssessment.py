from resources import *
from AssessmentFunction import displayViewAssessment, getAssessment
from PIL import Image, ImageTk
from tooltip import CreateToolTip
from EncryptAndDecryptFunction import doEncryption
import json
import tkinter as tk
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar, filedialog, messagebox, scrolledtext, ttk
from tkinter.constants import CENTER, DISABLED, END, INSERT

with open(config_path) as file:
    config = json.load(file)
#Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)
#Global method for this File - This method allow copy and paste but not editing textbox
def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

class ViewAssessmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Setting of Variable
        self.textResponse = ''

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="View Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=65)

        self.label_crn = Label(self, text="Reference Number*", width=20, font=("bold", 10), anchor = 'w')
        self.label_crn.place(x=100, y=130)

        label_crn_ttp = CreateToolTip(self.label_crn, tooltipDescription["ExternalCourseReferenceNumber"])

        self.entry_crn = Entry(self)
        self.entry_crn.place(x=250, y=130)

        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(event):
            value = displayViewAssessment(self.entry_crn.get())
            curlText.delete("1.0", "end")
            curlText.insert(tk.END, value)

        self.entry_crn.bind('<KeyRelease>', typing)

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
        responseText.bind("<Key>", lambda e: txtEvent)

        # Textbox for Curl Frame
        curlText = scrolledtext.ScrolledText(curlFrame, width=70, height=30)
        curlText.insert(tk.END, str(displayViewAssessment("")))
        curlText.place(height=405, width=440, y=20)
        curlText.bind("<Key>", lambda e: txtEvent)

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

        submitButton = tk.Button(self, text="View", bg="white", width=15, pady=5,
                                 command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.25, anchor=CENTER)
        exportButton = tk.Button(self, text="Export Decrypted Response", bg="white", width=25, pady=5,
                                 command=lambda: downloadFile())
        exportButton.place(relx=0.5, rely=0.95, anchor=CENTER)


        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = ViewAssessmentPage.textResponse.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(ViewAssessmentPage.textResponse.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())

        # This call back method activates two other methods.
        # 1) this method calls the get method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def submitCallBack():
            responseText.delete("1.0", "end")
            resp = getAssessment(self.entry_crn.get())
            ViewAssessmentPage.textResponse = StringVar(self, value=resp)
            responseText.insert(INSERT, ViewAssessmentPage.textResponse.get())
            tabControl.select(responseFrame)
            self.varResp.set(1)

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