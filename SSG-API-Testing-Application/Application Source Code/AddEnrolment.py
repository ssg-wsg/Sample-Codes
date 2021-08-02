from resources import *
from EncryptAndDecryptFunction import doDecryption, doEncryption
from EnrolmentFunction import addEnrolment, displayPostRequestEnrolment
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar,scrolledtext,filedialog, ttk, messagebox
import tkinter as tk
from tkinter.constants import CENTER, DISABLED, END, INSERT
from tooltip import CreateToolTip
from PIL import ImageTk, Image
import json

#Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)
#Preload file for UEN
with open(config_path) as file:
    config = json.load(file)

#Global method for this File - This method allow copy and paste but not editing textbox
def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
        return
    else:
        return "break"

#Page 1 for Create Enrolment
class AddEnrolmentMainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Variable
        #This list will be used to generate the payload layout for Trainee
        entry_list = []
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Create Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Enrolment JSON File", variable=self.var, value=1, width=25, anchor='w').place(x=158,y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2,width=25, anchor='w').place(x=158,y=130)
        self.var.set(2)

        label_0 = Label(self, text="Basic Mandate Form", width=20, font=("bold", 15))
        label_0.place(x=137, y=180)

        self.label_runId = Label(self, text="Course Run Id*", width=20, font=("bold", 10), anchor='w')
        self.label_runId.place(x=100, y=215)

        label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        self.entry_runId = Entry(self)
        self.entry_runId.place(x=270, y=215)
        

        self.label_CRN = Label(self, text="Course Reference Number*", width=20, font=("bold", 10), anchor='w')
        self.label_CRN.place(x=100, y=240)

        self.label_CRN_ttp = CreateToolTip(self.label_CRN, tooltipDescription["ExternalCourseReferenceNumber"])

        self.entry_CRN = Entry(self)
        self.entry_CRN.place(x=270, y=240)
        

        self.label_TpUEN = Label(self, text="Training Partner - UEN*", width=20, font=("bold", 10), anchor='w')
        self.label_TpUEN.place(x=100, y=265)

        self.label_UEN_ttp = CreateToolTip(self.label_TpUEN, tooltipDescription["UEN"])
        uenReadOnly = StringVar()
        uenReadOnly.set(config["UEN"])
        self.entry_TpUEN = Entry(self, state=DISABLED, textvariable=uenReadOnly)
        self.entry_TpUEN.place(x=270, y=265)

        self.label_TpCode = Label(self, text="Training Partner - Code*", width=20, font=("bold", 10), anchor='w')
        self.label_TpCode.place(x=100, y=290)
        

        self.label_TpCode_ttp = CreateToolTip(self.label_TpCode, tooltipDescription["TpCode"])

        self.entry_TpCode = Entry(self)
        self.entry_TpCode.place(x=270, y=290)


        self.label_TraineeTitle = Label(self, text="Trainee Details", width=20, font=("bold", 15))
        self.label_TraineeTitle.place(x=137, y=315)

        self.Label_TraineeEmpUen = Label(self, text="Trainee - Employer UEN", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmpUen.place(x=100, y=350)

        self.Label_TraineeEmpUen_ttp = CreateToolTip(self.Label_TraineeEmpUen, tooltipDescription["UEN"])
        self.entry_TraineeEmpUen = Entry(self)
        self.entry_TraineeEmpUen.place(x=270, y=350)
        entry_list.append(self.entry_TraineeEmpUen)

        self.Label_TraineeEmpPhone = Label(self, text="Trainee - Employer Contact Number*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmpPhone.place(x=100, y=375)

        self.Label_TraineePhone_ttp = CreateToolTip(self.Label_TraineeEmpPhone, tooltipDescription["Phone"])

        self.entry_TraineeEmpCountryCode = Entry(self, width=3)
        self.entry_TraineeEmpCountryCode.place(x=270, y=375)
        entry_list.append(self.entry_TraineeEmpCountryCode)

        self.entry_TraineeEmpAreaCode = Entry(self, width=3)
        self.entry_TraineeEmpAreaCode.place(x=300, y=375)
        entry_list.append(self.entry_TraineeEmpAreaCode)


        self.entry_TraineeEmpPhone = Entry(self, width=10)
        self.entry_TraineeEmpPhone.place(x=330, y=375)
        entry_list.append(self.entry_TraineeEmpPhone)

        self.Label_TraineeEmpName = Label(self, text="Trainee - Employer Name", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmpName.place(x=100, y=400)

        self.Label_TraineeEmpName_ttp = CreateToolTip(self.Label_TraineeEmpName, tooltipDescription["TrainerName"])
        self.entry_TraineeEmpName = Entry(self)
        self.entry_TraineeEmpName.place(x=270, y=400)
        entry_list.append(self.entry_TraineeEmpName)

        self.Label_TraineeEmpEmail = Label(self, text="Trainee - Employer Email", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmpEmail.place(x=100, y=425)

        self.Label_TraineeEmpEmail_ttp = CreateToolTip(self.Label_TraineeEmpEmail, tooltipDescription["CourseAdminEmail"])
        self.entry_TraineeEmpEmail = Entry(self)
        self.entry_TraineeEmpEmail.place(x=270, y=425)
        entry_list.append(self.entry_TraineeEmpEmail)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: NextCallBack() if self.var.get() == 2 else controller.show_frame(addEnrolmentPageFileUpload))
        nextButton.place(x=250, y=675, anchor=CENTER)
        def NextCallBack():
            AddEnrolmentPreviewPage.payload = StoreAndSave()
            controller.show_frame(AddEnrolmentPage2)
            
        def StoreAndSave():
            try:
                payload = json.loads(AddEnrolmentPreviewPage.payload)
            except:
                payload = {}
            
            payload['enrolment'] = {}

            if uenReadOnly.get() != '' or self.entry_TpCode.get() != '':
                payload['enrolment']['trainingPartner'] = {}
                if uenReadOnly != '':
                    payload['enrolment']['trainingPartner']['uen']=uenReadOnly.get()
                if self.entry_TpCode.get() != '':
                    payload['enrolment']['trainingPartner']['code'] = self.entry_TpCode.get()
            
            if self.entry_CRN.get() != '' or self.entry_runId.get() != '':
                payload['enrolment']['course'] = {}
                if self.entry_CRN.get() != '':
                    payload['enrolment']['course']['referenceNumber'] = self.entry_CRN.get()
                if self.entry_runId.get() != '':
                    payload['enrolment']['course']['run'] = {"id":self.entry_runId.get()}

            for entries in entry_list:
                if (entries.get() != '' or uenReadOnly.get()!= ''):
                    payload['enrolment']['trainee'] = {}
                    payload['enrolment']['trainee']['employer'] = {}
                    payload['enrolment']['trainee']['employer']['contact'] = {}
                    break
            if (self.entry_TraineeEmpAreaCode.get() != '' or self.entry_TraineeEmpCountryCode.get() != '' or self.entry_TraineeEmpPhone.get()):
                payload['enrolment']['trainee']['employer']['contact']['contactNumber'] = {}
                if self.entry_TraineeEmpAreaCode.get() != '':
                    payload['enrolment']['trainee']['employer']['contact']['contactNumber']['areaCode'] = self.entry_TraineeEmpAreaCode.get()
                if self.entry_TraineeEmpCountryCode.get() != '':
                    payload['enrolment']['trainee']['employer']['contact']['contactNumber']['countryCode'] = self.entry_TraineeEmpCountryCode.get()
                if self.entry_TraineeEmpPhone.get() != '':
                    payload['enrolment']['trainee']['employer']['contact']['contactNumber']['phoneNumber'] = self.entry_TraineeEmpPhone.get()
            if self.entry_TraineeEmpUen.get() != '':
                payload['enrolment']['trainee']['employer']['uen'] = self.entry_TraineeEmpUen.get()
            if self.entry_TraineeEmpEmail.get() != '':
                payload['enrolment']['trainee']['employer']['contact']['emailAddress'] = self.entry_TraineeEmpEmail.get()
            if self.entry_TraineeEmpName.get() != '':
                payload['enrolment']['trainee']['employer']['contact']['fullName'] = self.entry_TraineeEmpName.get()

            return str(json.dumps(payload, indent=4))
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Page 2 for Create Enrolment
class AddEnrolmentPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        # Variable
        # This list will be used to generate the payload layout for Trainee
        entry_list = []
        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)


        label_0 = Label(self, text="Trainee - Details", width=20, font=("bold", 15))
        label_0.place(x=137, y=73)

        self.label_TraineeIdType = Label(self, text="Trainee - Id Type*", width=20, font=("bold", 10), anchor='w')
        self.label_TraineeIdType.place(x=100, y=110)

        self.label_IdType_ttp = CreateToolTip(self.label_TraineeIdType, tooltipDescription["TraineeIdType"])

        self.TraineeIdType = ttk.Combobox(self, width = 17,state="readonly")
        self.TraineeIdType['values'] = ["Select An Option",
                     "NRIC",
                     "Fin",
                     "Others"]
        self.TraineeIdType.current(0)
        self.TraineeIdType.place(x=270, y=110)
        entry_list.append(self.TraineeIdType)

        self.Label_TraineeId = Label(self, text="Trainee - Id*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeId.place(x=100, y=135)

        self.Label_TraineeId_ttp = CreateToolTip(self.Label_TraineeId, tooltipDescription["TraineeId"])

        self.entry_TraineeId = Entry(self)
        self.entry_TraineeId.place(x=270, y=135)
        entry_list.append(self.entry_TraineeId)

        self.Label_TraineeName = Label(self, text="Trainee - Full Name", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeName.place(x=100, y=160)

        self.Label_TraineeName_ttp = CreateToolTip(self.Label_TraineeName, tooltipDescription["TrainerName"])

        self.entry_TraineeName = Entry(self)
        self.entry_TraineeName.place(x=270, y=160)
        entry_list.append(self.entry_TraineeName)

        self.Label_TraineeDOB = Label(self, text="Trainee - Date of Birth*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeDOB.place(x=100, y=185)

        self.Label_TraineeDOB_ttp = CreateToolTip(self.Label_TraineeDOB, tooltipDescription["DOB"])

        self.entry_TraineeDOB = Entry(self)
        self.entry_TraineeDOB.place(x=270, y=185)
        entry_list.append(self.entry_TraineeDOB)

        self.Label_TraineeEmail = Label(self, text="Trainee - Email*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEmail.place(x=100, y=210)

        self.Label_TraineeEmail_ttp = CreateToolTip(self.Label_TraineeEmail, tooltipDescription["TrainerEmail"])

        self.entry_TraineeEmail = Entry(self)
        self.entry_TraineeEmail.place(x=270, y=210)
        entry_list.append(self.entry_TraineeEmail)
        
        self.Label_TraineePhone = Label(self, text="Trainee - Contact Number*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineePhone.place(x=100, y=235)

        self.Label_TraineePhone_ttp = CreateToolTip(self.Label_TraineePhone, tooltipDescription["Phone"])

        self.entry_TraineeCountryCode = Entry(self, width=3)
        self.entry_TraineeCountryCode.place(x=270, y=235)
        entry_list.append(self.entry_TraineeCountryCode)

        self.entry_TraineeAreaCode = Entry(self, width=3)
        self.entry_TraineeAreaCode.place(x=300, y=235)
        entry_list.append(self.entry_TraineeAreaCode)

        self.entry_TraineePhone = Entry(self, width=10)
        self.entry_TraineePhone.place(x=330, y=235)
        entry_list.append(self.entry_TraineePhone)

        self.Label_TraineeSponsorship = Label(self, text="Trainee - Sponsorship Type*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeSponsorship.place(x=100, y=260)

        self.Label_TraineeSponsorship_ttp = CreateToolTip(self.Label_TraineeSponsorship, tooltipDescription["SponsorshipType"])

        self.sponsorshipType = ttk.Combobox(self, width = 17,state="readonly")
        self.sponsorshipType['values'] = ["Select An Option",
                     "EMPLOYER",
                     "INDIVIDUAL"]
        self.sponsorshipType.current(0)
        self.sponsorshipType.place(x=270, y=260)
        entry_list.append(self.sponsorshipType)

        self.Label_TraineeEntrolmentDate = Label(self, text="Trainee - Enrolment Date*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeEntrolmentDate.place(x=100, y=285)

        self.Label_TraineeEntrolmentDate_ttp = CreateToolTip(self.Label_TraineeEntrolmentDate, tooltipDescription["DOB"])
        
        self.entry_TraineeEntrolmentDate  = Entry(self)
        self.entry_TraineeEntrolmentDate.place(x=270, y=285)
        entry_list.append(self.entry_TraineeEntrolmentDate)

        self.Label_TraineeCollectionStatus = Label(self, text="Trainee - Collection Status*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeCollectionStatus.place(x=100, y=310)

        self.Label_TraineeCollectionStatus_ttp = CreateToolTip(self.Label_TraineeCollectionStatus, tooltipDescription["collectionStatus"])
        
        self.collectionStatus = ttk.Combobox(self, width = 17,state="readonly")
        self.collectionStatus['values'] = ["Select An Option",
                     "Full Payment",
                     "Partial Payment ",
                     "Pending Payment"
                     ]
        self.collectionStatus.current(0)
        self.collectionStatus.place(x=270, y=310)
        entry_list.append(self.collectionStatus)


        self.Label_TraineeDiscountAmt = Label(self, text="Trainee - Discount Amount", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeDiscountAmt.place(x=100, y=335)

        self.Label_TraineeDiscountAmt_ttp = CreateToolTip(self.Label_TraineeDiscountAmt, tooltipDescription["discountAmount"])
        
        self.entry_TraineeDiscountAmt  = Entry(self)
        self.entry_TraineeDiscountAmt.place(x=270, y=335)
        entry_list.append(self.entry_TraineeDiscountAmt)
  

        nextButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: NextCallBack())
        nextButton.place(relx=0.65, rely=0.86, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=15, pady=5,
                               command=lambda: controller.show_frame(AddEnrolmentMainPage)
                               )
        backButton.place(relx=0.35, rely=0.86, anchor=CENTER)

        def NextCallBack():
            AddEnrolmentPreviewPage.payload = StoreAndSave()
            AddEnrolmentPreviewPage.refresh(controller.frames[AddEnrolmentPreviewPage].curlText)
            controller.show_frame(AddEnrolmentPreviewPage)

        def StoreAndSave():
            try:
                payload = json.loads(AddEnrolmentPreviewPage.payload)
                payload['enrolment']['trainee'] 
            except:
                payload = json.loads(AddEnrolmentPreviewPage.payload)
                payload['enrolment']['trainee'] = {}
            
            if self.entry_TraineeId.get() != '':
                payload['enrolment']['trainee']['id'] = self.entry_TraineeId.get()
            if self.entry_TraineeName.get() != '':
                payload['enrolment']['trainee']['fullName'] = self.entry_TraineeName.get()
            if self.entry_TraineeDOB.get() != '':
                payload['enrolment']['trainee']['dateOfBirth'] = self.entry_TraineeDOB.get()
            if self.entry_TraineeEmail.get() != '':
                payload['enrolment']['trainee']['emailAddress'] = self.entry_TraineeEmail.get()
            if self.entry_TraineeEntrolmentDate.get() != '':
                payload['enrolment']['trainee']['enrolmentDate'] = self.entry_TraineeEntrolmentDate.get()
            if self.sponsorshipType.get() != 'Select An Option':
                payload['enrolment']['trainee']['sponsorshipType'] = self.sponsorshipType.get()
            if self.TraineeIdType.get() != 'Select An Option':
                payload['enrolment']['trainee']['idType'] = {}
                payload['enrolment']['trainee']['idType']['type'] = self.TraineeIdType.get()
            if self.entry_TraineeDiscountAmt.get() != '' or self.collectionStatus.get() != 'Select An Option':
                payload['enrolment']['trainee']['fees'] = {}
                if self.entry_TraineeDiscountAmt.get() != '':
                    payload['enrolment']['trainee']['fees']['discountAmount'] = self.entry_TraineeDiscountAmt.get()
                if self.collectionStatus.get() != 'Select An Option':
                    payload['enrolment']['trainee']['fees']['collectionStatus'] = self.collectionStatus.get()
            if self.entry_TraineeAreaCode.get() != '' or self.entry_TraineeCountryCode.get() != '' or self.entry_TraineePhone.get() != '':
                payload['enrolment']['trainee']['contactNumber'] = {}
                if self.entry_TraineeAreaCode.get() != '':
                    payload['enrolment']['trainee']['contactNumber']['areaCode'] = self.entry_TraineeAreaCode.get()
                if self.entry_TraineeCountryCode.get() != '':
                    payload['enrolment']['trainee']['contactNumber']['countryCode'] = self.entry_TraineeCountryCode.get()
                if self.entry_TraineePhone.get() != '':
                    payload['enrolment']['trainee']['contactNumber']['phoneNumber'] = self.entry_TraineePhone.get()
            
            return str(json.dumps(payload, indent=4))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Preview Page for Create Enrolment
class AddEnrolmentPreviewPage(tk.Frame):
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(displayPostRequestEnrolment("",AddEnrolmentPreviewPage.payload)))

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
        self.runIdEntered = 0

        # Title
        label_0 = Label(self, text="Add Enrolment", width=20, font=("bold", 20))
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
            
        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=5, command=lambda: createCallBack())
        submitButton.place(relx=0.5, rely=0.15, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(AddEnrolmentPage2),
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

        #Radio button for Response
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
        
        #displayPayload and displayResp method is used to display the encrypted and decrypted payload/response in the Preview/Fileupload Page
        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = doEncryption(str(AddEnrolmentPreviewPage.payload).encode()).decode()
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",payloadToDisplay)))
            else:
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",AddEnrolmentPreviewPage.payload)))

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = AddEnrolmentPreviewPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(AddEnrolmentPreviewPage.textPayload.get()).encode())
                except:
                    display = b''
                
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())

        def createCallBack():
            responseText.delete("1.0","end")
            resp = addEnrolment(AddEnrolmentPreviewPage.payload)
            print(resp)
            resp = doDecryption(resp)
            resp = json.loads(resp.decode())
            AddEnrolmentPreviewPage.textPayload = StringVar(self, value = str(json.dumps(resp,indent=4))) 
            responseText.insert(INSERT,AddEnrolmentPreviewPage.textPayload.get())
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
            filetext = str(AddEnrolmentPreviewPage.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")
            
class addEnrolmentPageFileUpload(tk.Frame):
    global fileUploadEntry

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Variable
        self.textPayload = ''
        self.contentInfo = ''

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Create Enrolment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)
        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=90, y=110)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X )


         #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        
        #Adding of tabs
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
                               command=lambda: controller.show_frame(AddEnrolmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.26, anchor=CENTER)

        exportRespButton = tk.Button(self, text="Export Decrypted Response", bg="white", width=25, pady=5, command = lambda: downloadFile())
        exportRespButton.place(relx=0.5, rely=0.95, anchor=CENTER)
        
        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w', command = lambda:displayPayload("decrypt")).place(x=0,y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2,width=12, anchor='w',command = lambda:displayPayload("encrypt")).place(x=130,y=-5)
        self.varPayload.set(1)

        self.varResp = IntVar()
        Radiobutton(tab3, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w', command = lambda:displayResp("decrypt")).place(x=0,y=-5)
        Radiobutton(tab3, text="Encrypt", variable=self.varResp, value=2,width=12, anchor='w',command = lambda:displayResp("encrypt")).place(x=130,y=-5)
        self.varResp.set(1)
    
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

        #displayPayload and displayResp method is used to display the encrypted and decrypted payload/response in the Preview/Fileupload Page
        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = ''
                try:
                    if self.contentInfo != '':
                        payloadToDisplay = doEncryption(str(self.contentInfo).encode()).decode()
                except:
                    payloadToDisplay = ''
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",payloadToDisplay)))
            else:
                try:
                    self.contentInfo != ''
                except:
                    self.contentInfo = ''
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayPostRequestEnrolment("",self.contentInfo)))
        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = addEnrolmentPageFileUpload.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(addEnrolmentPageFileUpload.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())
        
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

            self.curlText.insert(tk.END, displayPostRequestEnrolment("",self.contentInfo))
                

        def submitCallBack():
            responseText.delete("1.0","end")
            payload = self.contentInfo
            if (payload != ''):
                responseText.delete("1.0","end")
                resp = addEnrolment(payload)
                resp = doDecryption(resp)
                resp = json.loads(resp.decode())
                addEnrolmentPageFileUpload.textPayload = StringVar(self, value = str(json.dumps(resp,indent=4))) 
                responseText.insert(INSERT,addEnrolmentPageFileUpload.textPayload.get())
                self.varResp.set(1)
                tabControl.select(tab3)
            else:
                print("empty payload")


        def downloadFile():
            try:
                filetext = str(addEnrolmentPageFileUpload.textPayload.get())
                files = [('JSON', '*.json'),
                        ('Text Document', '*.txt')]
                file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
                file.write(filetext)
                file.close()
                messagebox.showinfo("Successful", "File has been downloaded")
            except:
                messagebox.showerror("Error", "Unable to download File - Empty Response")