from resources import *
from EncryptAndDecryptFunction import doEncryption
from AttendanceFunction import curlRequestUploadAttendance, uploadAttendanceFn
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar, scrolledtext, filedialog, ttk, messagebox
import tkinter as tk
from tkinter.constants import CENTER, DISABLED, END
from tooltip import CreateToolTip
from PIL import ImageTk, Image
import json

# Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)

with open(config_path) as file:
    config = json.load(file)


# Frame for Page 1 - Add Attendance
class addAttendancePage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Upload Attendance", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_filterTitle = Label(self, text="Request Form:", width=20, font=("bold", 15))
        label_filterTitle.place(x=137, y=100)

        label_TpUEN = Label(self, text="Training Partner - UEN", width=20, font=("bold", 10), anchor='w')
        label_TpUEN.place(x=80, y=135)

        label_UEN_ttp = CreateToolTip(label_TpUEN, tooltipDescription["UEN"])
        uenReadOnly = StringVar()
        uenReadOnly.set(config["UEN"])
        entry_TpUEN = Entry(self, state=DISABLED, textvariable=uenReadOnly)
        entry_TpUEN.place(x=250, y=135)

        label_sessionID = Label(self, text="Session ID", width=20, font=("bold", 10), anchor='w')
        label_sessionID.place(x=80, y=160)

        label_sessionID_ttp = CreateToolTip(label_sessionID, tooltipDescription["SessionId"])

        entry_sessionID = Entry(self)
        entry_sessionID.place(x=250, y=160)

        label_attendanceStatusCode = Label(self, text="Attendance Status Code*", width=20, font=("bold", 10), anchor='w')
        label_attendanceStatusCode.place(x=80, y=185)

        label_attendanceStatusCode_ttp = CreateToolTip(label_attendanceStatusCode, tooltipDescription["StatusCode"])

        attendanceStatusCode = ttk.Combobox(self, width=17, state="readonly")
        attendanceStatusCode['values'] = ["Select an Option",
                                          "1 - Confirmed",
                                          "2 - Unconfirmed",
                                          "3 - Rejected",
                                          "4 - TP Voided"]
        attendanceStatusCode.current(0)
        attendanceStatusCode.place(x=250, y=185)

        label_traineeID = Label(self, text="Trainee ID*", width=20, font=("bold", 10), anchor='w')
        label_traineeID.place(x=80, y=210)

        label_traineeID_ttp = CreateToolTip(label_traineeID, tooltipDescription["TraineeId"])

        entry_traineeID = Entry(self)
        entry_traineeID.place(x=250, y=210)

        label_traineeName = Label(self, text="Trainee Name*", width=20, font=("bold", 10), anchor='w')
        label_traineeName.place(x=80, y=235)

        label_traineeNamee_ttp = CreateToolTip(label_traineeName, tooltipDescription["TraineeName"])

        entry_traineeName = Entry(self)
        entry_traineeName.place(x=250, y=235)

        label_traineeEmail = Label(self, text="Trainee Email", width=20, font=("bold", 10), anchor='w')
        label_traineeEmail.place(x=80, y=260)

        label_traineeEmail_ttp = CreateToolTip(label_traineeEmail, tooltipDescription["TrainerEmail"])

        entry_traineeEmail = Entry(self)
        entry_traineeEmail.place(x=250, y=260)

        label_traineeIdType = Label(self, text="Trainee ID Type*", width=20, font=("bold", 10), anchor='w')
        label_traineeIdType.place(x=80, y=285)

        label_traineeIdType_ttp = CreateToolTip(label_traineeIdType, tooltipDescription["TraineeIdType"])

        traineeIdType = ttk.Combobox(self, width=17, state="readonly")
        traineeIdType['values'] = ["Select an Option",
                                   "SB - SG Blue Identification Card",
                                   "SP - SG Pink Identification Card",
                                   "SO -  Fin/Work Permit/SAF 11B",
                                   "OT - Others"]
        traineeIdType.current(0)
        traineeIdType.place(x=250, y=285)

        label_TraineePhone = Label(self, text="Trainee Contact Number*", width=20, font=("bold", 10), anchor='w')
        label_TraineePhone.place(x=80, y=310)

        Label_TraineePhone_ttp = CreateToolTip(label_TraineePhone, tooltipDescription["Phone"])

        entry_TraineeCountryCode = Entry(self, width=3)
        entry_TraineeCountryCode.place(x=250, y=310)

        entry_TraineeAreaCode = Entry(self, width=3)
        entry_TraineeAreaCode.place(x=280, y=310)

        entry_TraineePhoneNo = Entry(self, width=10)
        entry_TraineePhoneNo.place(x=310, y=310)

        label_traineeHours = Label(self, text="Number of Hours", width=20, font=("bold", 10), anchor='w')
        label_traineeHours.place(x=80, y=335)

        label_traineeHours = CreateToolTip(label_traineeHours, tooltipDescription["NumberOfHours"])

        entry_traineeHours = Entry(self)
        entry_traineeHours.place(x=250, y=335)

        label_surveyLanguage = Label(self, text="Survey Language*", width=20, font=("bold", 10), anchor='w')
        label_surveyLanguage.place(x=80, y=360)
        label_surveyLanguage_ttp = CreateToolTip(label_surveyLanguage, tooltipDescription["SurveyLanguage"])  

        surveyLanguage = ttk.Combobox(self, width=17, state="readonly")
        surveyLanguage['values'] = ["Select an Option",
                                    "EL - English",
                                    "MN - Mandarin",
                                    "MY - Malay",
                                    "TM - Tamil"]
        surveyLanguage.current(0)
        surveyLanguage.place(x=250, y=360)

        label_referenceNumber = Label(self, text="Reference Number", width=20, font=("bold", 10), anchor='w')
        label_referenceNumber.place(x=80, y=385)

        label_referenceNumber_ttp = CreateToolTip(label_referenceNumber, tooltipDescription["CourseReferenceNumber"])

        entry_referenceNumber = Entry(self)
        entry_referenceNumber.place(x=250, y=385)

        label_corppassID = Label(self, text="Corpass ID*", width=20, font=("bold", 10), anchor='w')
        label_corppassID.place(x=80, y=410)

        label_corppassID_ttp = CreateToolTip(label_corppassID, tooltipDescription["CorpPassId"])

        entry_corppassID = Entry(self)
        entry_corppassID.place(x=250, y=410)

        previewButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                                  command=lambda: NextCallBack())
        previewButton.place(x=250, y=470, anchor=CENTER)

        def NextCallBack():
            addAttendancePage2.payload = StoreAndSave()
            addAttendancePage2.refresh(controller.frames[addAttendancePage2].curlText)
            controller.show_frame(addAttendancePage2)

        def StoreAndSave():
            payload = {}
            payload['course'] = {}
            payload['course']['attendance'] = {}
            if entry_TpUEN.get() != '':
                payload['uen'] = entry_TpUEN.get()

            if entry_sessionID.get() != '':
                payload['course']['sessionID'] = entry_sessionID.get()

            if attendanceStatusCode.get() != 'Select an Option':
                payload['course']['attendance']['status'] = {}
                payload['course']['attendance']['status']['code'] = attendanceStatusCode.get()[0]

            if entry_traineeID.get() != '' or entry_traineeName.get() != '' or entry_traineeEmail.get() != ''  or entry_TraineePhoneNo.get() != '' or entry_TraineeCountryCode.get() != '' or entry_TraineeAreaCode.get() != '' or entry_traineeHours.get() != '' :
                payload['course']['attendance']['trainee'] = {}
                payload['course']['attendance']['trainee']['id'] = entry_traineeID.get()
                payload['course']['attendance']['trainee']['name'] = entry_traineeName.get()
                payload['course']['attendance']['trainee']['email'] = entry_traineeEmail.get()
                if traineeIdType.get() != 'Select an Option':
                    payload['course']['attendance']['trainee']['idType'] = {}
                    payload['course']['attendance']['trainee']['idType']['code'] = traineeIdType.get()[0:2]
                payload['course']['attendance']['trainee']['contactNumber'] = {}
                payload['course']['attendance']['trainee']['contactNumber']['mobile'] = entry_TraineePhoneNo.get()
                payload['course']['attendance']['trainee']['contactNumber']['areaCode'] = entry_TraineeAreaCode.get()
                payload['course']['attendance']['trainee']['contactNumber'][
                    'countryCode'] = entry_TraineeCountryCode.get()
                payload['course']['attendance']['trainee']['numberOfHours'] = entry_traineeHours.get()
                if surveyLanguage.get() != 'Select an Option':
                    payload['course']['attendance']['trainee']['surveyLanguage'] = {}
                    payload['course']['attendance']['trainee']['surveyLanguage']['code'] = surveyLanguage.get()[0:2]

            if entry_referenceNumber.get() != '':
                payload['course']['referenceNumber'] = entry_referenceNumber.get()

            if entry_corppassID.get() != '':
                payload['corppassId'] = entry_corppassID.get()

            print(json.dumps(payload, indent=4))
            return str(json.dumps(payload, indent=4))


# upload Attendance Page
class addAttendancePage2(tk.Frame):

    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0", "end")
        controllerCurlText.insert(tk.END, str(curlRequestUploadAttendance("", addAttendancePage2.payload)))

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Variable
        self.payload = '{}'
        self.textPayload = ''
        self.contentInfo = ''

        # Title
        label_0 = Label(self, text="Upload Attendance", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        label_1 = Label(self, text="Course Run ID", width=20, font=("bold", 10), anchor='w')
        label_1.place(x=105, y=100)
        # label_1_ttp = CreateToolTip(label_1, tkDescription["CourseRunId"])
        self.entry_runId = Entry(self)
        self.entry_runId.place(x=275, y=100)

        # This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():
            value = curlRequestUploadAttendance(self.entry_runId.get(), addAttendancePage2.payload)
            self.curlText.delete("1.0", "end")
            self.curlText.insert(tk.END, value)

        self.entry_runId.bind('<KeyRelease>', lambda a: typing())

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

        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END,
                             str(curlRequestUploadAttendance("", "")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")

        submitButton = tk.Button(self, text="Create", bg="white", width=15, pady=5,
                                 command=lambda: uploadAttendanceCallBack(self.entry_runId.get(),
                                                                          addAttendancePage2.payload))
        submitButton.place(relx=0.5, rely=0.20, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=15, pady=5,
                               command=lambda: controller.show_frame(addAttendancePage1))
        backButton.place(relx=0.5, rely=0.25, anchor=CENTER)

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

        def displayPayload(method):
            if method == 'decrypt':
                
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END,curlRequestUploadAttendance(self.entry_runId.get(), addAttendancePage2.payload))
            else:
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, curlRequestUploadAttendance(self.entry_runId.get(), str(doEncryption(addAttendancePage2.payload.encode()).decode())))
                
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
            filetext = str(addAttendancePage2.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        # This method activates two other methods.
        # 1) this method calls the delete method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response
        def uploadAttendanceCallBack(runId, attendancePayload):
            resp = uploadAttendanceFn(runId, attendancePayload)
            responseText.delete("1.0", "end")
            responseText.insert(tk.END, resp)
            tabControl.select(tab3)
