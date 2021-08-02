from resources import *
from AssessmentFunction import displayPostRequestAssessment, addAssessmentFn
from EncryptAndDecryptFunction import doEncryption
from tkinter import Button, Entry, IntVar, Label, Radiobutton, StringVar, scrolledtext, filedialog, ttk, messagebox
import tkinter as tk
from tkinter.constants import CENTER, DISABLED, END, INSERT
from tooltip import CreateToolTip
from PIL import ImageTk, Image
import json

# Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)

with open(config_path) as file:
    config = json.load(file)


# Global method for this File - This method allow copy and paste but not editing textbox
def txtEvent(event):
    if (event.state == 12 and event.keysym == 'c'):
        return
    else:
        return "break"


# Page 1 for Create Assessment
class AddAssessmentMainPage(tk.Frame):
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

        label_0 = Label(self, text="Create Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload an Assessment JSON File", variable=self.var, value=1, width=25, anchor='w').place(
            x=158, y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2, width=25,
                    anchor='w').place(x=158, y=130)
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

        label_0 = Label(self, text="Trainee - Details", width=20, font=("bold", 15))
        label_0.place(x=137, y=315)

        self.label_TraineeIdType = Label(self, text="Trainee - Id Type*", width=20, font=("bold", 10), anchor='w')
        self.label_TraineeIdType.place(x=100, y=350)

        self.label_IdType_ttp = CreateToolTip(self.label_TraineeIdType, tooltipDescription["TraineeIdType"])

        self.TraineeIdType = ttk.Combobox(self, width=17, state="readonly")
        self.TraineeIdType['values'] = ["Select An Option",
                                        "NRIC",
                                        "Fin",
                                        "Others"]
        self.TraineeIdType.current(0)
        self.TraineeIdType.place(x=270, y=350)
        entry_list.append(self.TraineeIdType)

        self.Label_TraineeId = Label(self, text="Trainee - Id*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeId.place(x=100, y=375)

        self.Label_TraineeId_ttp = CreateToolTip(self.Label_TraineeId, tooltipDescription["TraineeId"])

        self.entry_TraineeId = Entry(self)
        self.entry_TraineeId.place(x=270, y=375)
        entry_list.append(self.entry_TraineeId)

        self.Label_TraineeName = Label(self, text="Trainee - Full Name*", width=20, font=("bold", 10), anchor='w')
        self.Label_TraineeName.place(x=100, y=400)

        self.Label_TraineeName_ttp = CreateToolTip(self.Label_TraineeName, tooltipDescription["TrainerName"])

        self.entry_TraineeName = Entry(self)
        self.entry_TraineeName.place(x=270, y=400)
        entry_list.append(self.entry_TraineeName)

        self.label_results = Label(self, text="Results*", width=20, font=("bold", 10), anchor='w')
        self.label_results.place(x=100, y=425)

        self.label_IdType_ttp = CreateToolTip(self.label_TraineeIdType, tooltipDescription["TraineeIdType"])

        self.results = ttk.Combobox(self, width=17, state="readonly")
        self.results['values'] = ["Select An Option",
                                  "Pass",
                                  "Fail",
                                  "Exempt"]
        self.results.current(0)
        self.results.place(x=270, y=425)

        self.Label_score = Label(self, text="Score", width=20, font=("bold", 10), anchor='w')
        self.Label_score.place(x=100, y=450)

        self.Label_score_ttp = CreateToolTip(self.Label_score, tooltipDescription["Result"])

        self.entry_score = Entry(self)
        self.entry_score.place(x=270, y=450)

        self.label_grade = Label(self, text="Grades", width=20, font=("bold", 10), anchor='w')
        self.label_grade.place(x=100, y=475)

        self.label_grade_ttp = CreateToolTip(self.label_grade, tooltipDescription["Grade"])

        self.grade = ttk.Combobox(self, width=17, state="readonly")
        self.grade['values'] = ["Select An Option",
                                "A",
                                "B",
                                "C",
                                "D",
                                "E",
                                "F"]
        self.grade.current(0)
        self.grade.place(x=270, y=475)

        self.Label_assessmentDate = Label(self, text="Assessment Date*", width=20, font=("bold", 10), anchor='w')
        self.Label_assessmentDate.place(x=100, y=500)

        self.Label_assessmentDatettp = CreateToolTip(self.Label_assessmentDate, tooltipDescription["assessmentDate"])

        self.entry_assessmentDate = Entry(self)
        self.entry_assessmentDate.place(x=270, y=500)


        self.Label_skillCode = Label(self, text="Skill Code", width=20, font=("bold", 10), anchor='w')
        self.Label_skillCode.place(x=100, y=525)

        self.Label_skillCode_ttp = CreateToolTip(self.Label_skillCode, tooltipDescription["skillCode"])

        self.entry_skillCode = Entry(self)
        self.entry_skillCode.place(x=270, y=525)


        self.Label_branchCode = Label(self, text="UEN/Branch Code (Results)", width=20, font=("bold", 10), anchor='w')
        self.Label_branchCode.place(x=100, y=550)

        self.Label_branchCode_ttp = CreateToolTip(self.Label_branchCode, tooltipDescription["conferringInstitute"])

        self.entry_branchCode = Entry(self)
        self.entry_branchCode.place(x=270, y=550)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command=lambda: NextCallBack() if self.var.get() == 2 else controller.show_frame(
                                   addAssessmentPageFileUpload))
        nextButton.place(x=250, y=675, anchor=CENTER)

        def NextCallBack():
            AddAssessmentPreviewPage.payload = StoreAndSave()
            AddAssessmentPreviewPage.refresh(controller.frames[AddAssessmentPreviewPage].curlText)
            controller.show_frame(AddAssessmentPreviewPage)

        def StoreAndSave():
            try:
                payload = json.loads(AddAssessmentPreviewPage.payload)
            except:
                payload = {}

            payload['assessment'] = {}

            if uenReadOnly.get() != '' or self.entry_TpCode.get() != '':
                payload['assessment']['trainingPartner'] = {}
                if uenReadOnly != '':
                    payload['assessment']['trainingPartner']['uen'] = uenReadOnly.get()
                if self.entry_TpCode.get() != '':
                    payload['assessment']['trainingPartner']['code'] = self.entry_TpCode.get()

            if self.entry_CRN.get() != '' or self.entry_runId.get() != '':
                payload['assessment']['course'] = {}
                if self.entry_CRN.get() != '':
                    payload['assessment']['course']['referenceNumber'] = self.entry_CRN.get()
                if self.entry_runId.get() != '':
                    payload['assessment']['course']['run'] = {"id": self.entry_runId.get()}

            if self.entry_TraineeId.get() != '' or self.entry_TraineeName.get() != '' or self.TraineeIdType.get() != 'Select An Option':
                payload['assessment']['trainee'] = {}
                payload['assessment']['trainee']['id'] = self.entry_TraineeId.get()
                payload['assessment']['trainee']['fullName'] = self.entry_TraineeName.get()
                payload['assessment']['trainee']['idType'] = self.TraineeIdType.get()

            if self.results.get() != 'Select An Option':
                payload['assessment']['result'] = self.results.get()
            if self.entry_score.get() != '':
                payload['assessment']['score'] = self.entry_score.get()
            if self.grade.get() != 'Select An Option':
                payload['assessment']['grade'] = self.grade.get()
            if self.entry_assessmentDate.get() != '':
                payload['assessment']['assessmentDate'] = self.entry_assessmentDate.get()
            if self.entry_skillCode.get() != '':
                payload['assessment']['skillCode'] = self.entry_skillCode.get()
            if self.entry_branchCode.get() != '':
                payload['assessment']['conferringInstitute'] = {}
                payload['assessment']['conferringInstitute']['code'] = self.entry_branchCode.get()

            return str(json.dumps(payload, indent=4))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Preview Page for Create Assessment
class AddAssessmentPreviewPage(tk.Frame):
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0", "end")
        controllerCurlText.insert(tk.END, str(displayPostRequestAssessment(AddAssessmentPreviewPage.payload)))

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
        self.runIdEntered = 0

        # Title
        label_0 = Label(self, text="Create Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=43)

        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        #Tab 2 refers to Request Tab
        #Tab 3 refers to Response Tab
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Response')
        tabControl.place(width=440, height=460, x=30, y=182)

        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END, str(displayPostRequestAssessment("")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: txtEvent(e))

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: txtEvent(e))

        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=5, command=lambda: createCallBack())
        submitButton.place(relx=0.5, rely=0.15, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(AddAssessmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.2, anchor=CENTER)

        #exportButton1 refers to "Export Decrytped Payload" button
        #exportButton2 refers tp "Export Decrypted Response" button
        exportButton1 = tk.Button(self, text="Export Decrypted Payload", bg="white", width=20, pady=3,
                                  command=lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.90, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Decrypted Response", bg="white", width=20, pady=3,
                                  command=lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.90, anchor=CENTER)

        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w',
                    command=lambda: displayPayload("decrypt")).place(x=0, y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2, width=12, anchor='w',
                    command=lambda: displayPayload("encrypt")).place(x=130, y=-5)
        self.varPayload.set(1)

        self.varResp = IntVar()
        Radiobutton(tab3, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w',
                    command=lambda: displayResp("decrypt")).place(x=0, y=-5)
        Radiobutton(tab3, text="Encrypt", variable=self.varResp, value=2, width=12, anchor='w',
                    command=lambda: displayResp("encrypt")).place(x=130, y=-5)
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
                payloadToDisplay = doEncryption(str(AddAssessmentPreviewPage.payload).encode()).decode()
                self.curlText.delete("1.0", "end")
                self.curlText.insert(tk.END, str(displayPostRequestAssessment(payloadToDisplay)))
            else:
                self.curlText.delete("1.0", "end")
                self.curlText.insert(tk.END, str(displayPostRequestAssessment(AddAssessmentPreviewPage.payload)))

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = AddAssessmentPreviewPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0", "end")
                responseText.insert(INSERT, display)
            else:
                try:
                    display = doEncryption(str(AddAssessmentPreviewPage.textPayload.get()).encode())
                except:
                    display = b''

                responseText.delete("1.0", "end")
                responseText.insert(tk.END, display.decode())

        def createCallBack():
            print("Create Assessment:" + AddAssessmentPreviewPage.payload)
            responseText.delete("1.0", "end")
            resp = addAssessmentFn(AddAssessmentPreviewPage.payload)
            responseText.insert(INSERT, resp)
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
            filetext = str(AddAssessmentPreviewPage.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")


class addAssessmentPageFileUpload(tk.Frame):
    global fileUploadEntry

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        # Variable
        self.textPayload = ''
        self.contentInfo = ''

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Create Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)
        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=90, y=110)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X)

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
        tabControl.add(tab2, text='Request')
        tabControl.add(tab3, text='Response')
        tabControl.place(width=440, height=460, x=30, y=222)

        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END, str(displayPostRequestAssessment("")))
        self.curlText.place(height=405, width=440, y=20)

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)

        self.curlText.bind("<Key>", lambda e: txtEvent(e))
        responseText.bind("<Key>", lambda e: txtEvent(e))

        browseButton = tk.Button(self, text="Browse", command=lambda: getFile(self))
        browseButton.pack(in_=fileuploadframe, side=tk.LEFT)
        submitButton = tk.Button(self, text="Create", bg="white", width=25, pady=4, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.21, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=4,
                               command=lambda: controller.show_frame(AddAssessmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.26, anchor=CENTER)

        exportRespButton = tk.Button(self, text="Export Decrypted Response", bg="white", width=25, pady=5,
                                     command=lambda: downloadFile())
        exportRespButton.place(relx=0.5, rely=0.95, anchor=CENTER)
        
        #Radio button for Request
        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w',
                    command=lambda: displayPayload("decrypt")).place(x=0, y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2, width=12, anchor='w',
                    command=lambda: displayPayload("encrypt")).place(x=130, y=-5)
        self.varPayload.set(1)
        #Radio button for Response
        self.varResp = IntVar()
        Radiobutton(tab3, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w',
                    command=lambda: displayResp("decrypt")).place(x=0, y=-5)
        Radiobutton(tab3, text="Encrypt", variable=self.varResp, value=2, width=12, anchor='w',
                    command=lambda: displayResp("encrypt")).place(x=130, y=-5)
        self.varResp.set(1)

        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = ''
                try:
                    if self.contentInfo != '':
                        payloadToDisplay = doEncryption(str(self.contentInfo).encode()).decode()
                except:
                    payloadToDisplay = ''
                self.curlText.delete("1.0", "end")
                self.curlText.insert(tk.END, str(displayPostRequestAssessment(payloadToDisplay)))
            else:
                try:
                    self.contentInfo != ''
                except:
                    self.contentInfo = ''
                self.curlText.delete("1.0", "end")
                self.curlText.insert(tk.END, str(displayPostRequestAssessment(self.contentInfo)))

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = addAssessmentPageFileUpload.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0", "end")
                responseText.insert(INSERT, display)
            else:
                try:
                    display = doEncryption(str(addAssessmentPageFileUpload.textPayload.get()).encode())
                except:
                    display = b''
                responseText.delete("1.0", "end")
                responseText.insert(tk.END, display.decode())

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

        def getFile(window):
            self.curlText.delete("1.0", "end")
            filePath = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
            fileUploadEntry.delete(0, 'end')
            fileUploadEntry.insert(1, filePath)
            with open(filePath, 'r') as content:
                self.contentInfo = content.read()

            self.curlText.insert(tk.END, displayPostRequestAssessment(self.contentInfo))

        def submitCallBack():
            responseText.delete("1.0", "end")
            payload = self.contentInfo
            if (payload != ''):
                responseText.delete("1.0", "end")
                resp = addAssessmentFn(payload)
                responseText.insert(INSERT, resp)
                self.varResp.set(1)
                tabControl.select(tab3)
            else:
                print("empty payload")

        def downloadFile():
            try:
                filetext = str(addAssessmentPageFileUpload.textPayload.get())
                files = [('JSON', '*.json'),
                         ('Text Document', '*.txt')]
                file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
                file.write(filetext)
                file.close()
                messagebox.showinfo("Successful", "File has been downloaded")
            except:
                messagebox.showerror("Error", "Unable to download File - Empty Response")
