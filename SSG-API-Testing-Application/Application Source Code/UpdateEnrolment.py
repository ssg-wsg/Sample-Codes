from resources import *
from EncryptAndDecryptFunction import doDecryption, doEncryption
from EnrolmentFunction import displayPostRequestEnrolment, updateEnrolment
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar,scrolledtext,filedialog, ttk, messagebox
import tkinter as tk
from tkinter.constants import CENTER, DISABLED, END, INSERT
from tooltip import CreateToolTip
from PIL import ImageTk, Image
import json

with open(tooltip_path) as f:
    tooltipDescription = json.load(f)
#Global method for this File - This method allow copy and paste but not editing textbox
def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"
        
#Page 1 for Update Enrolment
class UpdateEnrolmentMainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Variable
        #This list will be used to generate the payload layout for Trainee
        entry_listEmp = []
        entry_listTrainee = []
        entry_fee = []
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Enrolment JSON File", variable=self.var, value=1, width=25, anchor='w').place(x=158,y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2,width=25, anchor='w').place(x=158,y=130)
        self.var.set(2)

        label_0 = Label(self, text="Course Details", width=20, font=("bold", 15))
        label_0.place(x=137, y=195)

        self.label_EnrolRefNum = Label(self, text="Enrol Reference Number*", width=20, font=("bold", 10), anchor='w')
        self.label_EnrolRefNum.place(x=100, y=230)

        label_EnrolRefNum_ttp = CreateToolTip(self.label_EnrolRefNum, tooltipDescription["EnrolRefNum"])

        self.entry_EnrolRefNum = Entry(self)
        self.entry_EnrolRefNum.place(x=270, y=230)

        self.label_runId = Label(self, text="Course Run Id", width=20, font=("bold", 10), anchor='w')
        self.label_runId.place(x=100, y=255)

        label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        self.entry_runId = Entry(self)
        self.entry_runId.place(x=270, y=255)
        
        
        self.label_TraineeTitle = Label(self, text="Trainee Details", width=20, font=("bold", 15))
        self.label_TraineeTitle.place(x=137, y=285)


        self.Label_TraineePhone = Label(self, text="Contact Number", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineePhone.place(x=100, y=320)

        self.Label_TraineePhone_ttp = CreateToolTip(self.Label_TraineePhone, tooltipDescription["Phone"])

        self.entry_TraineeCountryCode = Entry(self, width=3)
        self.entry_TraineeCountryCode.place(x=270, y=320)
        entry_listTrainee.append(self.entry_TraineeCountryCode)

        self.entry_TraineeAreaCode = Entry(self, width=3)
        self.entry_TraineeAreaCode.place(x=300, y=320)
        entry_listTrainee.append(self.entry_TraineeAreaCode)


        self.entry_TraineePhone = Entry(self, width=10)
        self.entry_TraineePhone.place(x=330, y=320)
        entry_listTrainee.append(self.entry_TraineePhone)

        self.Label_TraineeEmail = Label(self, text="Email", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmail.place(x=100, y=345)

        self.Label_TraineeEmail_ttp = CreateToolTip(self.Label_TraineeEmail, tooltipDescription["CourseAdminEmail"])
        self.entry_TraineeEmail = Entry(self)
        self.entry_TraineeEmail.place(x=270, y=345)
        entry_listTrainee.append(self.entry_TraineeEmail)

        self.label_TraineeTitle = Label(self, text="Employee Details", width=20, font=("bold", 15))
        self.label_TraineeTitle.place(x=137, y=375)

        self.Label_EmpName = Label(self, text="Name", width=20, font=("bold", 10), anchor='w')
        self.Label_EmpName.place(x=100, y=410)

        self.Label_EmpName_ttp = CreateToolTip(self.Label_EmpName, tooltipDescription["TrainerName"])
        self.entry_EmpName = Entry(self)
        self.entry_EmpName.place(x=270, y=410)
        entry_listEmp.append(self.entry_EmpName)

        self.Label_EmpEmail = Label(self, text="Email", width=20, font=("bold", 10), anchor='w')
        self.Label_EmpEmail.place(x=100, y=435)

        self.Label_EmpEmail_ttp = CreateToolTip(self.Label_EmpEmail, tooltipDescription["CourseAdminEmail"])
        self.entry_EmpEmail = Entry(self)
        self.entry_EmpEmail.place(x=270, y=435)
        entry_listEmp.append(self.entry_EmpEmail)

        self.Label_EmpPhone = Label(self, text="Contact Number", width=20, font=("bold", 10), anchor='w')
        self.Label_EmpPhone.place(x=100, y=460)

        self.Label_EmpPhone_ttp = CreateToolTip(self.Label_EmpPhone, tooltipDescription["Phone"])

        self.entry_EmpCountryCode = Entry(self, width=3)
        self.entry_EmpCountryCode.place(x=270, y=460)
        entry_listEmp.append(self.entry_EmpCountryCode)

        self.entry_EmpAreaCode = Entry(self, width=3)
        self.entry_EmpAreaCode.place(x=300, y=460)
        entry_listEmp.append(self.entry_EmpAreaCode)


        self.entry_EmpPhone = Entry(self, width=10)
        self.entry_EmpPhone.place(x=330, y=460)
        entry_listEmp.append(self.entry_EmpPhone)
        
        self.label_TraineeTitle = Label(self, text="Fees Details", width=20, font=("bold", 15))
        self.label_TraineeTitle.place(x=137, y=490)

        self.Label_CollectionStatus = Label(self, text="Collection Status", width=20, font=("bold", 10), anchor='w')
        self.Label_CollectionStatus.place(x=100, y=525)

        self.Label_CollectionStatus_ttp = CreateToolTip(self.Label_CollectionStatus, tooltipDescription["collectionStatus"])
        
        self.collectionStatus = ttk.Combobox(self, width = 17,state="readonly")
        self.collectionStatus['values'] = ["Select An Option",
                     "Full Payment",
                     "Partial Payment ",
                     "Pending Payment",
                     "Cancelled"
                     ]
        self.collectionStatus.current(0)
        self.collectionStatus.place(x=270, y=525)
        entry_fee.append(self.collectionStatus)


        self.Label_DiscountAmt = Label(self, text="Discount Amount", width=20, font=("bold", 10), anchor='w')
        self.Label_DiscountAmt.place(x=100, y=550)

        self.DiscountAmt_ttp = CreateToolTip(self.Label_DiscountAmt, tooltipDescription["discountAmount"])
        
        self.entry_DiscountAmt  = Entry(self)
        self.entry_DiscountAmt.place(x=270, y=550)
        entry_fee.append(self.entry_DiscountAmt)

        self.Label_Action = Label(self, text="Action*", width=20, font=("bold", 10), anchor='w')
        self.Label_Action.place(x=100, y=575)
        self.Label_Actionl_ttp = CreateToolTip(self.Label_Action, tooltipDescription["Action"])
        self.entry_Action  = Entry(self,state=DISABLED, textvariable=StringVar(value="Update"))
        self.entry_Action.place(x=270, y=575)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: NextCallBack() if self.var.get() == 2 else controller.show_frame(UpdateEnrolmentPageFileUploadPage))
        nextButton.place(x=250, y=675, anchor=CENTER)

        def NextCallBack():
            UpdateEnrolmentPreviewPage.payload = StoreAndSave()
            UpdateEnrolmentPreviewPage.refresh(controller.frames[UpdateEnrolmentPreviewPage].curlText)
            controller.show_frame(UpdateEnrolmentPreviewPage)
            
        def StoreAndSave():
            payload = {}
            payload['enrolment'] = {}

            for entry1 in entry_listEmp:
                if (entry1.get() != ''):
                    payload['enrolment']['employer'] = {}
                    payload['enrolment']['employer']['contact'] = {}
                    break
            for entry2 in entry_listTrainee:
                if (entry2.get() != ''):
                    payload['enrolment']['trainee'] = {}
                    break
            for entry3 in entry_fee:
                if (entry3.get() != '' and entry3.get() != 'Select An Option'):
                    payload['enrolment']['fees'] = {}
                    break
            
            payload['enrolment']['action'] = "Update"

            if self.entry_runId.get() != '':
                payload['enrolment']['course'] = {'run':{'id': self.entry_runId.get()}}

            if (self.entry_TraineePhone.get() != '' or self.entry_TraineeCountryCode.get() != '' or self.entry_TraineeAreaCode.get() != ''):
                payload['enrolment']['trainee']['contactNumber'] = {}
                if (self.entry_TraineePhone.get() != ''):
                    payload['enrolment']['trainee']['contactNumber']['phoneNumber'] = self.entry_TraineePhone.get()
                if (self.entry_TraineeCountryCode.get() != ''):
                    payload['enrolment']['trainee']['contactNumber']['countryCode'] = self.entry_TraineeCountryCode.get()
                if (self.entry_TraineeAreaCode.get() != ''):
                    payload['enrolment']['trainee']['contactNumber']['areaCode'] = self.entry_TraineeAreaCode.get()     

            if self.entry_TraineeEmail.get() != '':
                payload['enrolment']['trainee']['email'] = self.entry_TraineeEmail.get()
           
            if (self.entry_EmpEmail.get() != ''):
                payload['enrolment']['employer']['contact']['email'] = self.entry_EmpEmail.get()

            if (self.entry_EmpName.get() != ''):
                payload['enrolment']['employer']['contact']['fullName'] = self.entry_EmpName.get()

            if (self.entry_EmpAreaCode.get() != '' or self.entry_EmpCountryCode.get() != '' or self.entry_EmpPhone.get() != ''):
                payload['enrolment']['employer']['contact']['contactNumber'] = {}
                if (self.entry_EmpPhone.get() != ''):
                    payload['enrolment']['employer']['contact']['contactNumber']['phoneNumber'] = self.entry_EmpPhone.get()
                if (self.entry_EmpCountryCode.get() != ''):
                    payload['enrolment']['employer']['contact']['contactNumber']['countryCode'] = self.entry_EmpCountryCode.get()
                if (self.entry_EmpAreaCode.get() != ''):
                    payload['enrolment']['employer']['contact']['contactNumber']['areaCode'] = self.entry_EmpAreaCode.get()
            
            if self.entry_DiscountAmt.get() != '':
                payload['enrolment']['fees']['discountAmount'] = self.entry_DiscountAmt.get()
            if self.collectionStatus.get() != 'Select An Option':
                payload['enrolment']['fees']['feeCollectionStatus'] = self.collectionStatus.get()

            UpdateEnrolmentPreviewPage.refNumber = self.entry_EnrolRefNum.get()       
            return str(json.dumps(payload, indent=4))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Preview Page for Update Enrolment
class UpdateEnrolmentPreviewPage(tk.Frame):
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(displayPostRequestEnrolment(UpdateEnrolmentPreviewPage.refNumber,UpdateEnrolmentPreviewPage.payload)))

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        #Variable
        self.payload = '{}'
        self.textPayload = ''
        self.contentInfo = ''
        self.refNumber = 0

        # Title
        label_0 = Label(self, text="Update Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=43)

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
        tabControl.add(tab3, text='Reponse')
        tabControl.place(width=440, height=460, x=30, y=182)
        
        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END, str(displayPostRequestEnrolment("","")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: txtEvent(e))

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: txtEvent(e))
            
        submitButton = tk.Button(self, text="Update", bg="white", width=25, pady=5, command=lambda: updateCallBack())
        submitButton.place(relx=0.5, rely=0.15, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(UpdateEnrolmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.2, anchor=CENTER)
        #Exportbutton1 refers to Export Payload
        #Exportbutton2 refers to Export Response        
        exportButton1 = tk.Button(self, text="Export Decrypted Payload", bg="white", width=20, pady=3, command = lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.90, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Decrypted Response", bg="white", width=20, pady=3,command = lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.90, anchor=CENTER)
        
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
        edit.place(x=285, height=21, y=204)

        # setting focus
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda: find("curl"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        butt_resp = Button(tab3, text='Find', command=lambda: find("resp"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        
        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = doEncryption(str(UpdateEnrolmentPreviewPage.payload).encode()).decode()
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",payloadToDisplay)))
            else:
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",UpdateEnrolmentPreviewPage.payload)))

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = UpdateEnrolmentPreviewPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(UpdateEnrolmentPreviewPage.textPayload.get()).encode())
                except:
                    display = b''
                
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())

        def updateCallBack():
            responseText.delete("1.0","end")
            resp = updateEnrolment(UpdateEnrolmentPreviewPage.refNumber,UpdateEnrolmentPreviewPage.payload)
            try:
                    resp = doDecryption(resp)
                    resp = json.loads(resp.decode())
                    resp = str(json.dumps(resp,indent=4))
            except:
                pass
                
            UpdateEnrolmentPreviewPage.textPayload = StringVar(self, value = resp) 
            responseText.insert(INSERT,UpdateEnrolmentPreviewPage.textPayload.get())
            self.varResp.set(1)
            tabControl.select(tab3)


        # This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = self.curlText
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
            filetext = str(UpdateEnrolmentPreviewPage.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

#File Upload Page for UpdateEnrolment
class UpdateEnrolmentPageFileUploadPage(tk.Frame):
    global fileUploadEntry

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        #Setting of variables
        self.textPayload = ''
        self.contentInfo = ''

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=33)

        #Course Run Id
        label_EnrolRefNum = Label(self, text="Reference Number: ", width=20, font=("bold", 10), anchor='w')
        label_EnrolRefNum.place(x=100, y=80)

        self.entry_EnrolRefNum = Entry(self)
        self.entry_EnrolRefNum.place(x=270, y=80)
        label_1_ttp = CreateToolTip(label_EnrolRefNum, tooltipDescription["EnrolRefNum"])

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            value = displayPostRequestEnrolment(self.entry_EnrolRefNum.get(),self.contentInfo)
            self.curlText.delete("1.0","end")
            self.curlText.insert(tk.END, value)
            self.varPayload.set(1)

        self.entry_EnrolRefNum.bind('<KeyRelease>', lambda b:typing())

        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=90, y=108)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X )


         #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        
        # Adding of tabs
        #Tab 2 refers to Request Tab
        #Tab 3 refers to Response Tab
        tabControl.add(tab2, text ='Request')
        tabControl.add(tab3, text ='Reponse')
        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        self.curlText = scrolledtext.ScrolledText(tab2,width=70,height=30)
        self.curlText.insert(tk.END, str(displayPostRequestEnrolment("","")))
        self.curlText.place(height = 405, width = 440, y=20)
        
        responseText = scrolledtext.ScrolledText(tab3,width=70,height=30)
        responseText.place(height = 405, width = 440, y=20)
        
        self.curlText.bind("<Key>", lambda e: txtEvent(e))
        responseText.bind("<Key>", lambda e: txtEvent(e))


        browseButton = tk.Button(self,text="Browse", command=lambda:getFile(self))       
        browseButton.pack(in_=fileuploadframe, side=tk.LEFT)
        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=4, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.21, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=4,
                               command=lambda: controller.show_frame(UpdateEnrolmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.26, anchor=CENTER)

        exportRespButton = tk.Button(self, text="Export Decrypted Response", bg="white", width=25, pady=5, command = lambda: downloadFile())
        exportRespButton.place(relx=0.5, rely=0.95, anchor=CENTER)
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


        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = ''
                try:
                    if self.contentInfo != '':
                        payloadToDisplay = doEncryption(str(self.contentInfo).encode()).decode()
                except:
                    payloadToDisplay = ''
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment(self.entry_EnrolRefNum.get(),payloadToDisplay)))
            else:
                try:
                    self.contentInfo != ''
                except:
                    self.contentInfo = ''
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment(self.entry_EnrolRefNum.get(),self.contentInfo)))
        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = UpdateEnrolmentPageFileUploadPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(UpdateEnrolmentPageFileUploadPage.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())
    
        #adding of single line text box
        edit = Entry(self, background="light gray") 

        #positioning of text box
        edit.place(x = 285, height= 21, y=244) 

        #setting focus
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda:find("curl"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 
        butt_resp = Button(tab3, text='Find', command=lambda:find("resp"), highlightthickness = 0, bd = 0, background="gray")  
        butt_resp.place(x = 380, y=0, height=21, width=60) 

        #This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = self.curlText
            textw.tag_remove('found', '1.0', END) 
            
            #returns to widget currently in focus
            s = edit.get() 
            if s:
                idx = '1.0'
                while 1:
                    #searches for desried string from index 1
                    idx = textw.search(s, idx, nocase=1, 
                                    stopindex=END) 
                    if not idx: break
                    
                    #last index sum of current index and
                    #length of text
                    lastidx = '%s+%dc' % (idx, len(s)) 
                    
                    #overwrite 'Found' at idx
                    textw.tag_add('found', idx, lastidx) 
                    idx = lastidx
                    # textw.see(idx)  # Once found, the scrollbar automatically scrolls to the text
                
                #mark located string as red
                textw.tag_config('found', foreground='red') 
               
            edit.focus_set()

        def getFile(window):
            self.curlText.delete("1.0","end")
            filePath=filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
            fileUploadEntry.delete(0, 'end')
            fileUploadEntry.insert(1, filePath)
            with open(filePath, 'r') as content:
                self.contentInfo = content.read()

            self.curlText.insert(tk.END, displayPostRequestEnrolment(self.entry_EnrolRefNum.get(),self.contentInfo))
                

        def submitCallBack():
            payload = self.contentInfo
            if (payload != ''):
                responseText.delete("1.0","end")
                resp = updateEnrolment(self.entry_EnrolRefNum.get(),payload)
                try:
                    resp = doDecryption(resp)
                    resp = json.loads(resp.decode())
                    resp = str(json.dumps(resp,indent=4))
                except:
                    pass
                
                UpdateEnrolmentPageFileUploadPage.textPayload = StringVar(self, value = resp)
                responseText.insert(INSERT,UpdateEnrolmentPageFileUploadPage.textPayload.get())
                self.varResp.set(1)
                tabControl.select(tab3)


        def downloadFile():
            try:
                filetext = str(UpdateEnrolmentPageFileUploadPage.textPayload.get())
                files = [('JSON', '*.json'),
                        ('Text Document', '*.txt')]
                file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
                file.write(filetext)
                file.close()
                messagebox.showinfo("Successful", "File has been downloaded")
            except:
                messagebox.showerror("Error", "Unable to download File - Empty Response")