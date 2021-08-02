import json
from resources import *
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import messagebox, Button, Entry, Label, StringVar, ttk, filedialog, messagebox, scrolledtext
from tkinter.constants import CENTER, END, INSERT
from tooltip import CreateToolTip
from PIL import Image, ImageTk
from AdditionalFunction import loadFile
from courseRunFunctions import curlPostRequest, getCourseRun, updateCourserun


#Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)


# Frame for Page 1 - update Course Run
class updateCourseRunPageSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Course Run JSON File", variable=self.var, value=1).place(x=158, y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2).place(x=158, y=130)
        self.var.set(2)

        label_0 = Label(self, text="Basic Mandate Form", width=20, font=("bold", 15))
        label_0.place(x=137, y=185)

        self.label_runId = Label(self, text="Course Run Id*", width=20, font=("bold", 10), anchor='w')
        self.label_runId.place(x=100, y=220)

        label_runId_ttp = CreateToolTip(self.label_runId, tooltipDescription["CourseRunId"])

        self.entry_runId = Entry(self)
        self.entry_runId.place(x=270, y=220)

        label_CRN = Label(self, text="Course Reference Number*", width=20, font=("bold", 10), anchor='w')
        label_CRN.place(x=100, y=290)

        label_CRN_ttp = CreateToolTip(label_CRN, tooltipDescription["ExternalCourseReferenceNumber"])

        entry_CRN = Entry(self)
        entry_CRN.place(x=270, y=290)

        label_runTitle = Label(self, text="Run", width=20, font=("bold", 15))
        label_runTitle.place(x=137, y=320)

        label_openRegDate = Label(self, text="Registration Dates (Open)*", width=20, font=("bold", 10), anchor='w')
        label_openRegDate.place(x=100, y=355)

        label_openRegDate_ttp = CreateToolTip(label_openRegDate, tooltipDescription["CourseRegistrationDateOpen"])

        entry_openRegDate = Entry(self)
        entry_openRegDate.place(x=270, y=355)

        label_closeRegDate = Label(self, text="Registration Dates (Close)*", width=20, font=("bold", 10), anchor='w')
        label_closeRegDate.place(x=100, y=380)

        label_closeRegDate_ttp = CreateToolTip(label_closeRegDate, tooltipDescription["CourseRegistrationDateClose"])

        entry_closeRegDate = Entry(self)
        entry_closeRegDate.place(x=270, y=380)

        label_CourseStartDate = Label(self, text="Course Start Date*", width=20, font=("bold", 10), anchor='w')
        label_CourseStartDate.place(x=100, y=405)

        label_CourseStartDate_ttp = CreateToolTip(label_CourseStartDate, tooltipDescription["CourseStartDate"])

        entry_CourseStartDate = Entry(self)
        entry_CourseStartDate.place(x=270, y=405)

        label_CourseEndDate = Label(self, text="Course End Date*", width=20, font=("bold", 10), anchor='w')
        label_CourseEndDate.place(x=100, y=430)

        label_CourseEndDate_ttp = CreateToolTip(label_CourseEndDate, tooltipDescription["CourseEndDate"])

        entry_CourseEndDate = Entry(self)
        entry_CourseEndDate.place(x=270, y=430)

        label_scheduleInfoType = Label(self, text="InfoType*", width=20, font=("bold", 10), anchor='w')
        label_scheduleInfoType.place(x=100, y=455)

        label_scheduleInfoTypee_ttp = CreateToolTip(label_scheduleInfoType, tooltipDescription["InfoTypeCode"])

        entry_scheduleInfoType = Entry(self)
        entry_scheduleInfoType.place(x=270, y=455)

        label_scheduleInfoTypeDescription = Label(self, text="InfoType Description", width=20, font=("bold", 10),
                                                  anchor='w')
        label_scheduleInfoTypeDescription.place(x=100, y=480)

        label_scheduleInfoTypeDescription_ttp = CreateToolTip(label_scheduleInfoTypeDescription,
                                                              tooltipDescription["InfoTypeDescription"])

        entry_scheduleInfoTypeDescription = Entry(self)
        entry_scheduleInfoTypeDescription.place(x=270, y=480)

        label_CourseModeOfTraining = Label(self, text="Mode Of Training", width=20, font=("bold", 10), anchor='w')
        label_CourseModeOfTraining.place(x=100, y=505)

        label_CourseModeOfTraining_ttp = CreateToolTip(label_CourseModeOfTraining, tooltipDescription["ModeOfTraining"])
        modeOfTraining = ttk.Combobox(self, width=25, state="readonly")
        modeOfTraining['values'] = ["Select An Option",
                                    "1. Classroom",
                                    "2. Asynchronous eLearning",
                                    "3. In-house",
                                    "4. On-the-Job",
                                    "5. Practical/Practicum",
                                    "6. Supervised Field",
                                    "7. Traineeship",
                                    "8. Assessment",
                                    "9. Synchronous eLearning"]
        modeOfTraining.current(0)
        modeOfTraining.place(x=270, y=505)

        label_adminEmail = Label(self, text="Course Admin Email", width=20, font=("bold", 10), anchor='w')
        label_adminEmail.place(x=100, y=530)

        label_adminEmail_ttp = CreateToolTip(label_adminEmail, tooltipDescription["CourseAdminEmail"])

        entry_adminEmail = Entry(self)
        entry_adminEmail.place(x=270, y=530)

        label_threshold = Label(self, text="Threshold", width=20, font=("bold", 10), anchor='w')
        label_threshold.place(x=100, y=555)

        label_threshold_ttp = CreateToolTip(label_threshold, tooltipDescription["Threshold"])

        entry_threshold = Entry(self)
        entry_threshold.place(x=270, y=555)

        label_intakeSize = Label(self, text="Intake Size", width=20, font=("bold", 10), anchor='w')
        label_intakeSize.place(x=100, y=580)

        label_intakeSize_ttp = CreateToolTip(label_intakeSize, tooltipDescription["IntakeSize"])

        entry_intakeSize = Entry(self)
        entry_intakeSize.place(x=270, y=580)

        label_RegUserCount = Label(self, text="Registered User Count", width=20, font=("bold", 10), anchor='w')
        label_RegUserCount.place(x=100, y=605)

        label_RegUserCount_ttp = CreateToolTip(label_RegUserCount, tooltipDescription["RegisteredUserCount"])

        entry_RegUserCount = Entry(self)
        entry_RegUserCount.place(x=270, y=605)

        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5,
                               command=lambda: previewCallBack() if self.var.get() == 2 else controller.show_frame(
                                   updateCourseRunPageFormFileUpload))
        nextButton.place(x=250, y=675, anchor=CENTER)
        retrieveButton = tk.Button(self, text="Retrieve required fields", bg="white", width=25, pady=5,
                                   command=lambda: retrieveCallBack())
        retrieveButton.place(x=250, y=265, anchor=CENTER)

        def retrieveCallBack():
            if (self.entry_runId.get() != ''):
                resp = getCourseRun(self.entry_runId.get())
                if (resp.status_code < 400):
                    respObject = resp.json()
                    entry_CRN.delete("0", "end")
                    entry_CRN.insert(tk.END, respObject['data']['course']['referenceNumber'])

                    entry_CourseStartDate.delete("0", "end")
                    entry_CourseStartDate.insert(tk.END, respObject['data']['course']['run']['courseStartDate'])

                    entry_CourseEndDate.delete("0", "end")
                    entry_CourseEndDate.insert(tk.END, respObject['data']['course']['run']['courseEndDate'])

                    entry_closeRegDate.delete("0", "end")
                    entry_closeRegDate.insert(tk.END, respObject['data']['course']['run']['registrationClosingDate'])

                    entry_openRegDate.delete("0", "end")
                    entry_openRegDate.insert(tk.END, respObject['data']['course']['run']['registrationOpeningDate'])

                    entry_scheduleInfoType.delete("0", "end")
                    entry_scheduleInfoType.insert(tk.END,
                                                  respObject['data']['course']['run']['scheduleInfoType']['code'])
                    modeOfTraining.current(respObject['data']['course']['run']['modeOfTraining'])

                    print(respObject['data']['course']['run']['courseVacancy']['code'])
                    if respObject['data']['course']['run']['courseVacancy']['code'] == 'L':
                        controller.frames[updateCourseRunPagePage2].courseVacCode.current(2)
                    elif respObject['data']['course']['run']['courseVacancy']['code'] == 'A':
                        controller.frames[updateCourseRunPagePage2].courseVacCode.current(1)
                    else:
                        controller.frames[updateCourseRunPagePage2].courseVacCode.current(3)

                    if (str(respObject['data']['course']['run']['modeOfTraining']) != '2' and str(
                            respObject['data']['course']['run']['modeOfTraining']) != '4'):

                        controller.frames[updateCourseRunPagePage2].entry_venueFloor.delete("0", "end")
                        controller.frames[updateCourseRunPagePage2].entry_venueFloor.insert(tk.END, respObject['data'][
                            'course']['run']['venue']['floor'])

                        controller.frames[updateCourseRunPagePage2].entry_venueRoom.delete("0", "end")
                        controller.frames[updateCourseRunPagePage2].entry_venueRoom.insert(tk.END,
                                                                                           respObject['data']['course'][
                                                                                               'run']['venue']['room'])

                        controller.frames[updateCourseRunPagePage2].entry_venueUnit.delete("0", "end")
                        controller.frames[updateCourseRunPagePage2].entry_venueUnit.insert(tk.END,
                                                                                           respObject['data']['course'][
                                                                                               'run']['venue']['unit'])

                        controller.frames[updateCourseRunPagePage2].entry_venuePostalCode.delete("0", "end")
                        controller.frames[updateCourseRunPagePage2].entry_venuePostalCode.insert(tk.END,
                                                                                                 respObject['data'][
                                                                                                     'course']['run'][
                                                                                                     'venue'][
                                                                                                     'postalCode'])
                    else:
                        controller.frames[updateCourseRunPagePage2].label_venueRoom['text'] = "Venue - Room"
                        controller.frames[updateCourseRunPagePage2].label_venueUnit['text'] = "Venue - Unit"
                        controller.frames[updateCourseRunPagePage2].label_venueFloor['text'] = "Venue - Floor"
                        controller.frames[updateCourseRunPagePage2].label_venuePostalCode[
                            'text'] = "Venue - Postal Code"
                        modeOfTraining.current(int(respObject['data']['course']['run']['modeOfTraining']))
                else:
                    messagebox.showerror(title="Error", message="Unable to retrieve Information - Invalid Run Id")
            else:
                messagebox.showerror(title="Error", message="Unable to retrieve Information - Run Id cannot be empty")

        # Initialies the empty payload first in order to prevent clearing of data
        updateCourseRunPagePreview.payload = '{}'

        def storeAndsave_all():
            # load config File
            uen_Info = loadFile(config_path)
            config_uenJson = json.loads(uen_Info)
            uen_number = config_uenJson["UEN"]
            # self.courseRunInfoPythonObject["course"]["trainingProvider"]["uen"] = uen_number
            self.payload = json.loads(updateCourseRunPagePreview.payload)
            print(updateCourseRunPagePreview.payload)
            # self.payload = updateCourseRunPagePreview.payload

            # Check if the Key-Value Pair exists, if not create a new object
            try:
                self.payload["course"]
            except:
                self.payload["course"] = {}
                self.payload["course"]["run"] = {}

            self.payload["course"]["trainingProvider"] = {}
            self.payload["course"]["trainingProvider"]["uen"] = uen_number

            if modeOfTraining.get() != 'Select An Option':
                self.payload["course"]["run"]["modeOfTraining"] = modeOfTraining.get()[0]
            if entry_adminEmail.get() != '':
                self.payload["course"]["run"]["courseAdminEmail"] = entry_adminEmail.get()
            if entry_threshold.get() != '':
                self.payload["course"]["run"]["threshold"] = entry_threshold.get()
            if entry_intakeSize.get() != '':
                self.payload["course"]["run"]["intakeSize"] = entry_intakeSize.get()
            if entry_RegUserCount.get() != '':
                self.payload["course"]["run"]["registeredUserCount"] = entry_RegUserCount.get()
            if entry_CRN.get() != '':
                self.payload["course"]["courseReferenceNumber"] = entry_CRN.get()

            if entry_scheduleInfoType.get() != '' or entry_scheduleInfoTypeDescription.get() != '':
                self.payload["course"]["run"]["scheduleInfoType"] = {}
                if entry_scheduleInfoType.get() != '':
                    self.payload["course"]["run"]["scheduleInfoType"]["code"] = entry_scheduleInfoType.get()
                if entry_scheduleInfoTypeDescription.get() != '':
                    self.payload["course"]["run"]["scheduleInfoType"][
                        "description"] = entry_scheduleInfoTypeDescription.get()

            if entry_openRegDate.get() != '' or entry_closeRegDate.get() != '':
                self.payload["course"]["run"]["registrationDates"] = {}
                if entry_openRegDate.get() != '':
                    self.payload["course"]["run"]["registrationDates"]["opening"] = entry_openRegDate.get()
                if entry_closeRegDate.get() != '':
                    self.payload["course"]["run"]["registrationDates"]["closing"] = entry_closeRegDate.get()

            if entry_CourseStartDate.get() != '' or entry_CourseEndDate.get() != '':
                self.payload["course"]["run"]["courseDates"] = {}
                if entry_CourseStartDate.get() != '':
                    self.payload["course"]["run"]["courseDates"]["start"] = entry_CourseStartDate.get()
                if entry_CourseEndDate.get() != '':
                    self.payload["course"]["run"]["courseDates"]["end"] = entry_CourseEndDate.get()

            updateCourseRunPagePreview.runIdEntered = self.entry_runId.get()

            return str(json.dumps(self.payload, indent=4))

        def previewCallBack():
            updateCourseRunPagePreview.payload = storeAndsave_all()
            controller.show_frame(updateCourseRunPagePage2)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Page 2 for Update Course Run
class updateCourseRunPagePage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_1 = Label(self, text="Run", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        label_courseVacCode = Label(self, text="Vacancy Code*", width=20, font=("bold", 10), anchor='w')
        label_courseVacCode.place(x=100, y=140)

        label_courseVacCode_ttp = CreateToolTip(label_courseVacCode, tooltipDescription["CourseVacCode"])

        # self.entry_courseVacCode = Entry(self)
        # self.entry_courseVacCode.place(x=270, y=140)
        self.courseVacCode = ttk.Combobox(self, width=17, state="readonly")
        self.courseVacCode['values'] = ["Select An Option",
                                        "A - Available",
                                        "L - Limited",
                                        "F - Full"]
        self.courseVacCode.current(0)
        self.courseVacCode.place(x=270, y=140)

        self.label_courseVacDescription = Label(self, text="Vacancy Description", width=20, font=("bold", 10),
                                                anchor='w')
        self.label_courseVacDescription.place(x=100, y=165)

        label_courseVacDescription_ttp = CreateToolTip(self.label_courseVacDescription,
                                                       tooltipDescription["CourseVacDescription"])

        self.entry_courseVacDescription = Entry(self)
        self.entry_courseVacDescription.place(x=270, y=165)

        self.label_scheduleInfo = Label(self, text="Schedule Info", width=20, font=("bold", 10), anchor='w')
        self.label_scheduleInfo.place(x=100, y=190)

        label_scheduleInfo_ttp = CreateToolTip(self.label_scheduleInfo, tooltipDescription["ScheduleInfo"])

        self.entry_scheduleInfo = Entry(self)
        self.entry_scheduleInfo.place(x=270, y=190)

        self.label_venueRoom = Label(self, text="Venue - Room*", width=20, font=("bold", 10), anchor='w')
        self.label_venueRoom.place(x=100, y=215)

        label_venueRoom_ttp = CreateToolTip(self.label_venueRoom, tooltipDescription["Room"])

        self.entry_venueRoom = Entry(self)
        self.entry_venueRoom.place(x=270, y=215)

        self.label_venueUnit = Label(self, text="Venue - Unit*", width=20, font=("bold", 10), anchor='w')
        self.label_venueUnit.place(x=100, y=240)

        label_venueUnit_ttp = CreateToolTip(self.label_venueUnit, tooltipDescription["Unit"])

        self.entry_venueUnit = Entry(self)
        self.entry_venueUnit.place(x=270, y=240)

        self.label_venueFloor = Label(self, text="Venue - Floor*", width=20, font=("bold", 10), anchor='w')
        self.label_venueFloor.place(x=100, y=265)

        label_venueFloor_ttp = CreateToolTip(self.label_venueFloor, tooltipDescription["Floor"])

        self.entry_venueFloor = Entry(self)
        self.entry_venueFloor.place(x=270, y=265)

        self.label_venueBlock = Label(self, text="Venue - Block", width=20, font=("bold", 10), anchor='w')
        self.label_venueBlock.place(x=100, y=290)

        label_venueBlock_ttp = CreateToolTip(self.label_venueBlock, tooltipDescription["Block"])

        self.entry_venueBlock = Entry(self)
        self.entry_venueBlock.place(x=270, y=290)

        self.label_venueStreet = Label(self, text="Venue - Street", width=20, font=("bold", 10), anchor='w')
        self.label_venueStreet.place(x=100, y=315)

        label_venueStreet_ttp = CreateToolTip(self.label_venueStreet, tooltipDescription["Street"])

        self.entry_venueStreet = Entry(self)
        self.entry_venueStreet.place(x=270, y=315)

        self.label_venueBuilding = Label(self, text="Venue - Building", width=20, font=("bold", 10), anchor='w')
        self.label_venueBuilding.place(x=100, y=340)

        label_venueBuilding_ttp = CreateToolTip(self.label_venueBuilding, tooltipDescription["Building"])

        self.entry_venueBuilding = Entry(self)
        self.entry_venueBuilding.place(x=270, y=340)

        self.label_venuePostalCode = Label(self, text="Venue - Postal Code*", width=20, font=("bold", 10), anchor='w')
        self.label_venuePostalCode.place(x=100, y=365)

        label_venuePostalCode_ttp = CreateToolTip(self.label_venuePostalCode, tooltipDescription["PostalCode"])

        self.entry_venuePostalCode = Entry(self)
        self.entry_venuePostalCode.place(x=270, y=365)

        self.label_venueWheelchair = Label(self, text="Venue - Wheelchair Access", width=20, font=("bold", 10),
                                           anchor='w')
        self.label_venueWheelchair.place(x=100, y=390)

        label_venueWheelchair_ttp = CreateToolTip(self.label_venueWheelchair, tooltipDescription["WheelChairAccess"])

        options_Wheelchair = ttk.Combobox(self, width=17, state="readonly")
        options_Wheelchair['values'] = ["Select An Option",
                                        "True",
                                        "False"]
        options_Wheelchair.current(0)
        options_Wheelchair.place(x=270, y=390)

        def storeAndsave_all():

            print(updateCourseRunPagePreview.payload)
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)

            if self.courseVacCode.get() != 'Select An Option' or self.entry_courseVacDescription.get() != '':
                payloadToEdit['course']['run']['courseVacancy'] = {}
                if self.courseVacCode.get() != 'Select An Option':
                    payloadToEdit['course']['run']['courseVacancy']['code'] = self.courseVacCode.get()[0]
                if self.entry_courseVacDescription.get() != '':
                    payloadToEdit['course']['run']['courseVacancy'][
                        'description'] = self.entry_courseVacDescription.get()

            payloadToEdit['course']['run']['scheduleInfo'] = {}
            if self.entry_scheduleInfo.get() != '':
                payloadToEdit['course']['run']['scheduleInfo'] = self.entry_scheduleInfo.get()
            else:
                del payloadToEdit['course']['run']['scheduleInfo']

            def venueLoop():
                if self.entry_venuePostalCode.get() != '':
                    payloadToEdit['course']['run']['venue']['postalCode'] = self.entry_venuePostalCode.get()
                if self.entry_venueFloor.get() != '':
                    payloadToEdit['course']['run']['venue']['floor'] = self.entry_venueFloor.get()
                if self.entry_venueUnit.get() != '':
                    payloadToEdit['course']['run']['venue']['unit'] = self.entry_venueUnit.get()
                if self.entry_venueRoom.get() != '':
                    payloadToEdit['course']['run']['venue']['room'] = self.entry_venueRoom.get()
                if self.entry_venueBuilding.get() != '':
                    payloadToEdit['course']['run']['venue']['building'] = self.entry_venueBuilding.get()
                if self.entry_venueBlock.get() != '':
                    payloadToEdit['course']['run']['venue']['block'] = self.entry_venueBlock.get()
                if self.entry_venueStreet.get() != '':
                    payloadToEdit['course']['run']['venue']['street'] = self.entry_venueStreet.get()
                if options_Wheelchair.get() != 'Select An Option':
                    payloadToEdit['course']['run']['venue'][
                        'wheelChairAccess'] = True if options_Wheelchair.get() == 'True' else False

            try:
                venueLoop()
            except:
                payloadToEdit['course']['run']['venue'] = {}
                venueLoop()
            # print(payloadToEdit)
            return str(json.dumps(payloadToEdit, indent=4))

        backButton = tk.Button(self, text="Back", bg="white", width=15, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPageSelect)
                               )
        backButton.place(relx=0.35, rely=0.86, anchor=CENTER)

        def callback():

            updateCourseRunPagePreview.payload = storeAndsave_all()
            # print(updateCourseRunPagePreview.payload)
            # updateCourseRunPageSelect.updateCourseRunInfo = storeAndsave_all()
            # updateCourseRunPagePreview.refresh(controller.frames[updateCourseRunPagePreview].curlText)
            controller.show_frame(updateCourseRunPagePage3)

        nextButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: callback())
        nextButton.place(relx=0.65, rely=0.86, anchor=CENTER)


# Page 3 for Update Course Run - Sessions
class updateCourseRunPagePage3(tk.Frame):
    sessionSeqNumber = 0

    def deleteFrameInit(self, deleteFrame):

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(deleteFrame, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_sessionId = Label(deleteFrame, text="Session Id*", width=20, font=("bold", 10), anchor='w')
        self.label_sessionId.place(x=0, y=0)
        label_sessionId_ttp = CreateToolTip(self.label_sessionId, tooltipDescription["SessionId"])
        self.entry_sessionId = Entry(deleteFrame)
        self.entry_sessionId.place(x=170, y=0)

    def updateFrame(self, updateFrame):
        # self.addFrame(updateFrame)
        self.label_sessionId = Label(updateFrame, text="Session Id*", width=20, font=("bold", 10), anchor='w')
        self.label_sessionId.place(x=0, y=0)
        label_sessionId_ttp = CreateToolTip(self.label_sessionId, tooltipDescription["SessionId"])
        self.entry_sessionIdUpdate = Entry(updateFrame)
        self.entry_sessionIdUpdate.place(x=170, y=0)

    def addFrame(self, AddFrame):

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(AddFrame, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_ModeOfTraining = Label(AddFrame, text="Mode of Training*", width=20, font=("bold", 10), anchor='w')
        label_ModeOfTraining.place(x=0, y=0)
        label_ModeOfTraining_ttp = CreateToolTip(label_ModeOfTraining, tooltipDescription["ModeOfTraining"])

        self.modeOfTraining = ttk.Combobox(AddFrame, width=25, state="readonly")
        self.modeOfTraining['values'] = ["Select An Option",
                                         "1. Classroom",
                                         "2. Asynchronous eLearning",
                                         "3. In-house",
                                         "4. On-the-Job",
                                         "5. Practical/Practicum",
                                         "6. Supervised Field",
                                         "7. Traineeship",
                                         "8. Assessment",
                                         "9. Synchronous eLearning"]
        self.modeOfTraining.current(0)
        self.modeOfTraining.place(x=170, y=0)

        self.label_SessionStartDate = Label(AddFrame, text="Session Start Date*", width=20, font=("bold", 10),
                                            anchor='w')
        self.label_SessionStartDate.place(x=0, y=25)
        label_SessionStartDate_ttp = CreateToolTip(self.label_SessionStartDate, tooltipDescription["SessionStartDate"])
        self.entry_SessionStartDate = Entry(AddFrame)
        self.entry_SessionStartDate.place(x=170, y=25)

        self.label_SessionEndDate = Label(AddFrame, text="Session End Date*", width=20, font=("bold", 10), anchor='w')
        self.label_SessionEndDate.place(x=0, y=50)
        label_SessionEndDate_ttp = CreateToolTip(self.label_SessionEndDate, tooltipDescription["SessionEndDate"])
        self.entry_SessionEndDate = Entry(AddFrame)
        self.entry_SessionEndDate.place(x=170, y=50)

        self.label_SessionStartTime = Label(AddFrame, text="Session Start Time*", width=20, font=("bold", 10),
                                            anchor='w')
        self.label_SessionStartTime.place(x=0, y=75)
        label_SessionStartTime_ttp = CreateToolTip(self.label_SessionStartTime, tooltipDescription["SessionStartTime"])
        self.entry_SessionStartTime = Entry(AddFrame)
        self.entry_SessionStartTime.place(x=170, y=75)

        self.label_SessionEndTime = Label(AddFrame, text="Session End Time*", width=20, font=("bold", 10), anchor='w')
        self.label_SessionEndTime.place(x=0, y=100)
        label_SessionEndTime_ttp = CreateToolTip(self.label_SessionEndTime, tooltipDescription["SessionEndTime"])
        self.entry_SessionEndTime = Entry(AddFrame)
        self.entry_SessionEndTime.place(x=170, y=100)

        self.label_SessionVenueRoom = Label(AddFrame, text="Venue Room*", width=20, font=("bold", 10), anchor='w')
        self.label_SessionVenueRoom.place(x=0, y=125)
        label_SessionVenueRoom_ttp = CreateToolTip(self.label_SessionVenueRoom, tooltipDescription["Room"])
        self.entry_SessionVenueRoom = Entry(AddFrame)
        self.entry_SessionVenueRoom.place(x=170, y=125)

        self.label_SessionVenueUnit = Label(AddFrame, text="Venue Unit*", width=20, font=("bold", 10), anchor='w')
        self.label_SessionVenueUnit.place(x=0, y=150)
        label_SessionVenueUnitttp = CreateToolTip(self.label_SessionVenueUnit, tooltipDescription["Unit"])
        self.entry_SessionVenueUnit = Entry(AddFrame)
        self.entry_SessionVenueUnit.place(x=170, y=150)

        self.label_SessionVenueFloor = Label(AddFrame, text="Venue Floor*", width=20, font=("bold", 10), anchor='w')
        self.label_SessionVenueFloor.place(x=0, y=175)
        label_SessionVenueFloor_ttp = CreateToolTip(self.label_SessionVenueFloor, tooltipDescription["Floor"])
        self.entry_SessionVenueFloor = Entry(AddFrame)
        self.entry_SessionVenueFloor.place(x=170, y=175)

        self.label_SessionVenueBuilding = Label(AddFrame, text="Venue Building", width=20, font=("bold", 10),
                                                anchor='w')
        self.label_SessionVenueBuilding.place(x=0, y=200)
        label_SessionVenueBuilding_ttp = CreateToolTip(self.label_SessionVenueBuilding, tooltipDescription["Building"])
        self.entry_SessionVenueBuilding = Entry(AddFrame)
        self.entry_SessionVenueBuilding.place(x=170, y=200)

        self.label_SessionVenueBlock = Label(AddFrame, text="Venue Block", width=20, font=("bold", 10), anchor='w')
        self.label_SessionVenueBlock.place(x=0, y=225)
        label_SessionVenueBlock_ttp = CreateToolTip(self.label_SessionVenueBlock, tooltipDescription["Block"])
        self.entry_SessionVenueBlock = Entry(AddFrame)
        self.entry_SessionVenueBlock.place(x=170, y=225)

        self.label_SessionVenueStreet = Label(AddFrame, text="Venue Street", width=20, font=("bold", 10), anchor='w')
        self.label_SessionVenueStreet.place(x=0, y=250)
        label_SessionVenueStreet_ttp = CreateToolTip(self.label_SessionVenueStreet, tooltipDescription["Street"])
        self.entry_SessionVenueStreet = Entry(AddFrame)
        self.entry_SessionVenueStreet.place(x=170, y=250)

        self.label_SessionVenuePostalCode = Label(AddFrame, text="Venue Postal Code*", width=20, font=("bold", 10),
                                                  anchor='w')
        self.label_SessionVenuePostalCode.place(x=0, y=275)
        label_SessionVenuePostalCode_ttp = CreateToolTip(self.label_SessionVenuePostalCode,
                                                         tooltipDescription["PostalCode"])
        self.entry_SessionVenuePostalCode = Entry(AddFrame)
        self.entry_SessionVenuePostalCode.place(x=170, y=275)

        self.label_SessionVenuePrimary = Label(AddFrame, text="Venue Primary Venue", width=20, font=("bold", 10),
                                               anchor='w')
        self.label_SessionVenuePrimary.place(x=0, y=300)
        label_SessionVenuePrimary_ttp = CreateToolTip(self.label_SessionVenuePrimary,
                                                      tooltipDescription["PrimaryVenue"])
        self.options_PrimaryVenue = ttk.Combobox(AddFrame, width=17, state="readonly")
        self.options_PrimaryVenue['values'] = ["Select An Option",
                                               "True",
                                               "False"]
        self.options_PrimaryVenue.current(0)
        self.options_PrimaryVenue.place(x=170, y=300)

        self.label_SessionVenueWheelchair = Label(AddFrame, text="Venue Wheelchair Access", width=20, font=("bold", 10),
                                                  anchor='w')
        self.label_SessionVenueWheelchair.place(x=0, y=325)
        label_SessionVenueWheelchair_ttp = CreateToolTip(self.label_SessionVenueWheelchair,
                                                         tooltipDescription["WheelChairAccess"])
        self.options_Wheelchair = ttk.Combobox(AddFrame, width=17, state="readonly")
        self.options_Wheelchair['values'] = ["Select An Option",
                                             "True",
                                             "False"]
        self.options_Wheelchair.current(0)
        self.options_Wheelchair.place(x=170, y=325)

        # Change the label for venue to reflect the accuracy when selecting mode 2 and 4
        def changeLabel():
            if str(self.modeOfTraining.get()[0]) == '2' or str(self.modeOfTraining.get()[0]) == '4':
                self.label_SessionVenueRoom.configure(text="Venue Room")
                self.label_SessionVenueUnit.configure(text="Venue Unit")
                self.label_SessionVenueFloor.configure(text="Venue Floor")
                self.label_SessionVenuePostalCode.configure(text="Venue Postal code")
            else:
                self.label_SessionVenueRoom.configure(text="Venue Room*")
                self.label_SessionVenueUnit.configure(text="Venue Unit*")
                self.label_SessionVenueFloor.configure(text="Venue Floor*")
                self.label_SessionVenuePostalCode.configure(text="Venue Postal code*")

        self.modeOfTraining.bind('<<ComboboxSelected>>', lambda x: changeLabel())

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Setting of frame based on Choice for "action"
        def hide(choice):
            if choice == 'Delete':
                print('delete')
                deleteFrame.place(width=300, height=300, x=100, y=200)
                addFrame.place_forget()
                updateFrame.place_forget()
            elif choice == 'Add':
                print('Add')
                deleteFrame.place_forget()
                addFrame.place(width=350, height=400, x=100, y=200)
                updateFrame.place_forget()
            elif choice == 'Update':
                deleteFrame.place_forget()
                addFrame.place(width=350, height=350, x=100, y=200)
                updateFrame.place(width=295, height=20, x=100, y=550)
            else:
                updateFrame.place_forget()
                deleteFrame.place_forget()
                addFrame.place_forget()

        addFrame = tk.Frame(self)
        deleteFrame = tk.Frame(self)
        updateFrame = tk.Frame(self)
        self.options_Session_Action = ttk.Combobox(self, width=17, state="readonly")
        self.options_Session_Action['values'] = ["Select An option",
                                                 "Add",
                                                 "Update",
                                                 "Delete"]
        self.options_Session_Action.place(x=270, y=140)
        self.options_Session_Action.current(0)
        self.options_Session_Action.bind("<<ComboboxSelected>>", lambda x: hide(self.options_Session_Action.get()))

        self.addFrame(addFrame)
        self.updateFrame(updateFrame)
        self.deleteFrameInit(deleteFrame)

        label_1 = Label(self, text="Sessions", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        label_courseVacCode = Label(self, text="Action", width=20, font=("bold", 10))
        label_courseVacCode.place(x=100, y=140)

        backButton = tk.Button(self, text="Back", bg="white", width=15, pady=5,
                               command=lambda: backcallback()
                               )
        backButton.place(relx=0.35, rely=0.86, anchor=CENTER)
        addButton = tk.Button(self, text="Add", bg="white", width=15, pady=5, command=lambda: addCallback())
        addButton.place(relx=0.65, rely=0.8, anchor=CENTER)
        previewButton = tk.Button(self, text="Next", bg="white", width=15, pady=5, command=lambda: callback())
        previewButton.place(relx=0.65, rely=0.86, anchor=CENTER)
        resetButton = tk.Button(self, text="Clear Sessions", bg="white", width=15, pady=5,
                                command=lambda: resetSessions())
        resetButton.place(relx=0.35, rely=0.8, anchor=CENTER)

        def callback():
            hide('All')
            controller.show_frame(updateCourseRunPagePage4)

        def resetSessions():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)
            del (payloadToEdit["course"]["run"]["sessions"])
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent=4)
            tkinter.messagebox.showinfo(title="Success", message="All sessions successfully cleared")

        def addCallback():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)

            priVenue = self.options_PrimaryVenue.get() if self.options_PrimaryVenue.get() != 'Select An Option' else ''
            wheelChair = self.options_Wheelchair.get() if self.options_Wheelchair.get() != 'Select An Option' else ''
            try:
                sessionList = payloadToEdit["course"]["run"]["sessions"]
            except:
                sessionList = []

            if self.options_Session_Action.get() == 'Delete':
                sessionObjectTemplate = {
                    "action": self.options_Session_Action.get(),
                    "sessionId": self.entry_sessionId.get()
                }
            else:
                sessionObjectTemplate = {
                    "action": self.options_Session_Action.get(),
                }
                if self.entry_SessionStartDate.get() != '':
                    sessionObjectTemplate["startDate"] = self.entry_SessionStartDate.get()
                if self.entry_SessionEndTime.get() != '':
                    sessionObjectTemplate["endTime"] = self.entry_SessionEndTime.get()
                if self.entry_SessionEndDate.get() != '':
                    sessionObjectTemplate["endDate"] = self.entry_SessionEndDate.get()
                if self.entry_SessionStartTime.get() != '':
                    sessionObjectTemplate["startTime"] = self.entry_SessionStartTime.get()
                if self.modeOfTraining.get() != '':
                    sessionObjectTemplate["modeOfTraining"] = self.modeOfTraining.get()[0]

                def sessionVenueLoop():
                    if self.entry_SessionVenueRoom.get() != '':
                        sessionObjectTemplate["venue"]["room"] = self.entry_SessionVenueRoom.get()
                    if self.entry_SessionVenueFloor.get() != '':
                        sessionObjectTemplate["venue"]["floor"] = self.entry_SessionVenueFloor.get()
                    if self.entry_SessionVenueUnit.get() != '':
                        sessionObjectTemplate["venue"]["unit"] = self.entry_SessionVenueUnit.get()
                    if self.entry_SessionVenuePostalCode.get() != '':
                        sessionObjectTemplate["venue"]["postalCode"] = self.entry_SessionVenuePostalCode.get()
                    if self.entry_SessionVenueBlock.get() != '':
                        sessionObjectTemplate["venue"]["block"] = self.entry_SessionVenueBlock.get()
                    if self.entry_SessionVenueStreet.get() != '':
                        sessionObjectTemplate["venue"]["street"] = self.entry_SessionVenueStreet.get()
                    if self.entry_SessionVenueBuilding.get() != '':
                        sessionObjectTemplate["venue"]["building"] = self.entry_SessionVenueBuilding.get()
                    if priVenue != '':
                        sessionObjectTemplate["venue"]["primaryVenue"] = True if priVenue == 'True' else False
                    if wheelChair != '':
                        sessionObjectTemplate["venue"]["wheelChairAccess"] = True if wheelChair == 'True' else False

                try:
                    sessionVenueLoop()
                except:
                    sessionObjectTemplate['venue'] = {}
                    sessionVenueLoop()

            sessionList.append(sessionObjectTemplate)
            payloadToEdit['course']['run']['sessions'] = sessionList
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent=4)
            tkinter.messagebox.showinfo(title="Success", message="Session successfully added")
            clearSessionEntryBox()

        def clearSessionEntryBox():
            self.entry_SessionEndDate.delete(0, 'end')
            self.entry_SessionEndTime.delete(0, 'end')
            self.entry_sessionId.delete(0, 'end')
            self.entry_sessionIdUpdate.delete(0, 'end')
            self.entry_SessionStartDate.delete(0, 'end')
            self.entry_SessionStartTime.delete(0, 'end')
            self.entry_SessionVenueBlock.delete(0, 'end')
            self.entry_SessionVenueBuilding.delete(0, 'end')
            self.entry_SessionVenueFloor.delete(0, 'end')
            self.entry_SessionVenuePostalCode.delete(0, 'end')
            self.entry_SessionVenueRoom.delete(0, 'end')
            self.entry_SessionVenueStreet.delete(0, 'end')
            self.entry_SessionVenueUnit.delete(0, 'end')
            self.modeOfTraining.current(0)
            self.options_Wheelchair.current(0)
            self.options_PrimaryVenue.current(0)

        def backcallback():
            hide('All')
            controller.show_frame(updateCourseRunPagePage2)


# Page 4 for Update Course Run - Trainer
class updateCourseRunPagePage4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_1 = Label(self, text="Trainers", width=20, font=("bold", 15))
        label_1.place(x=137, y=100)

        self.label_trainerTypeCode = Label(self, text="Trainer Type Code*", width=20, font=("bold", 10), anchor='w')
        self.label_trainerTypeCode.place(x=100, y=140)

        self.index = 0
        self.ssecList = []

        label_trainerTypeCode_ttp = CreateToolTip(self.label_trainerTypeCode, tooltipDescription["TrainerCode"])
        self.entry_trainerTypeCode = ttk.Combobox(self, width=17, state="readonly")
        self.entry_trainerTypeCode['values'] = ["Select An option",
                                                "1. Existing",
                                                "2. New"]
        self.entry_trainerTypeCode.place(x=270, y=140)
        self.entry_trainerTypeCode.current(0)


        self.label_trainerTypeDescription = Label(self, text="Trainer Type Description*", width=20, font=("bold", 10),
                                                  anchor='w')
        self.label_trainerTypeDescription.place(x=100, y=165)
        label_trainerTypeDescription_ttp = CreateToolTip(self.label_trainerTypeDescription,
                                                         tooltipDescription["TrainerDescription"])
        self.entry_trainerTypeDescription = Entry(self)
        self.entry_trainerTypeDescription.place(x=270, y=165)

        self.label_trainerId = Label(self, text="Trainer Id", width=20, font=("bold", 10), anchor='w')
        self.label_trainerId.place(x=100, y=190)
        label_trainerId_ttp = CreateToolTip(self.label_trainerId, tooltipDescription["TrainerID"])
        self.entry_trainerId = Entry(self)
        self.entry_trainerId.place(x=270, y=190)

        self.label_trainerName = Label(self, text="Trainer Name*", width=20, font=("bold", 10), anchor='w')
        self.label_trainerName.place(x=100, y=215)
        label_trainerName_ttp = CreateToolTip(self.label_trainerName, tooltipDescription["TrainerName"])
        self.entry_trainerName = Entry(self)
        self.entry_trainerName.place(x=270, y=215)

        self.label_trainerEmail = Label(self, text="Trainer Email*", width=20, font=("bold", 10), anchor='w')
        self.label_trainerEmail.place(x=100, y=240)
        label_trainerEmail_ttp = CreateToolTip(self.label_trainerEmail, tooltipDescription["TrainerEmail"])
        self.entry_trainerEmail = Entry(self)
        self.entry_trainerEmail.place(x=270, y=240)

        self.label_trainerExperience = Label(self, text="Trainer Experience", width=20, font=("bold", 10), anchor='w')
        self.label_trainerExperience.place(x=100, y=265)
        label_trainerExperience_ttp = CreateToolTip(self.label_trainerExperience,
                                                    tooltipDescription["TrainerExperience"])
        self.entry_trainerExperience = Entry(self)
        self.entry_trainerExperience.place(x=270, y=265)

        self.label_trainerlinkedInUrl = Label(self, text="Trainer linkedInUrl", width=20, font=("bold", 10), anchor='w')
        self.label_trainerlinkedInUrl.place(x=100, y=290)
        label_trainerlinkedInUrl_ttp = CreateToolTip(self.label_trainerlinkedInUrl,
                                                     tooltipDescription["TrainerLinkedlnURL"])
        self.entry_trainerlinkedInUrl = Entry(self)
        self.entry_trainerlinkedInUrl.place(x=270, y=290)

        self.label_trainersalutationId = Label(self, text="Trainer salutationId", width=20, font=("bold", 10),
                                               anchor='w')
        self.label_trainersalutationId.place(x=100, y=315)
        label_trainersalutationId_ttp = CreateToolTip(self.label_trainersalutationId,
                                                      tooltipDescription["TrainerSalutationID"])
        self.trainersalutationId = ttk.Combobox(self, width=17, state="readonly")
        self.trainersalutationId['values'] = ["Select An Option",
                                              "1 - Mr",
                                              "2 - Ms",
                                              "3 - Mdm",
                                              "4 - Mrs",
                                              "5 - Dr",
                                              "6 - Prof"
                                              ]
        self.trainersalutationId.current(0)
        self.trainersalutationId.place(x=270, y=315)


        self.label_trainerdomainAreaOfPractice = Label(self, text="Trainer AreaOfPractice*", width=20,
                                                       font=("bold", 10), anchor='w')
        self.label_trainerdomainAreaOfPractice.place(x=100, y=340)
        label_trainerdomainAreaOfPractice_ttp = CreateToolTip(self.label_trainerdomainAreaOfPractice,
                                                              tooltipDescription["TrainerAreaOfPractice"])
        self.entry_trainerdomainAreaOfPractice = Entry(self)
        self.entry_trainerdomainAreaOfPractice.place(x=270, y=340)

        self.label_trainerinTrainingProviderProfile = Label(self, text="inTrainingProviderProfile", width=20,
                                                            font=("bold", 10), anchor='w')
        self.label_trainerinTrainingProviderProfile.place(x=100, y=365)
        label_trainerinTrainingProviderProfile_ttp = CreateToolTip(self.label_trainerinTrainingProviderProfile,
                                                                   tooltipDescription["inTrainingProviderProfile"])
        self.options_inTrainingProviderProfile = ttk.Combobox(self, width=17, state="readonly")
        self.options_inTrainingProviderProfile['values'] = ["Select An Option",
                                                            "True",
                                                            "False"]
        self.options_inTrainingProviderProfile.current(0)
        self.options_inTrainingProviderProfile.place(x=270, y=365)

        label_title = Label(self, text="Trainers - ssecEQAs", width=20, font=("bold", 15))
        label_title.place(x=137, y=410)

        self.label_trainerssecEQA = Label(self, text="Trainer ssecEQA", width=20, font=("bold", 10), anchor='w')
        self.label_trainerssecEQA.place(x=100, y=450)
        label_trainerssecEQA_ttp = CreateToolTip(self.label_trainerssecEQA, tooltipDescription["TrainerssecEQA"])
        self.entry_trainerssecEQA = Entry(self)
        self.entry_trainerssecEQA.place(x=270, y=450)

        self.label_trainerssecEQAdescription = Label(self, text="Trainer description", width=20, font=("bold", 10),
                                                     anchor='w')
        self.label_trainerssecEQAdescription.place(x=100, y=475)
        label_trainerssecEQAdescription_ttp = CreateToolTip(self.label_trainerssecEQAdescription,
                                                            tooltipDescription["TrainerssecDescription"])
        self.entry_trainerssecEQAdescription = Entry(self)
        self.entry_trainerssecEQAdescription.place(x=270, y=475)

        def addssecCallback():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)
            ssecEQAtemplate = {
                "code": self.entry_trainerssecEQA.get(),
                "description": self.entry_trainerssecEQAdescription.get()
            }

            self.ssecList.append(ssecEQAtemplate)
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent=4)
            self.entry_trainerssecEQA.delete(0, 'end')
            self.entry_trainerssecEQAdescription.delete(0, 'end')
            print(self.ssecList)

        def resetTrainers():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)
            del (payloadToEdit["course"]["run"]["linkCourseRunTrainer"])
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent=4)
            tkinter.messagebox.showinfo(title="Success", message="All trainers successfully cleared")

        def callback():

            updateCourseRunPagePreview.refresh(controller.frames[updateCourseRunPagePreview].curlText)
            controller.show_frame(updateCourseRunPagePreview)

        def addCallback():
            payloadToEdit = updateCourseRunPagePreview.payload
            payloadToEdit = json.loads(payloadToEdit)

            if self.options_inTrainingProviderProfile.get() == 'Select An Option':
                result = ''
            else:
                result = self.options_inTrainingProviderProfile.get()

            if self.entry_trainerTypeCode.get() == 'Select An Option':
                trainerCode = ''
            else:
                trainerCode = self.entry_trainerTypeCode.get()[0]

            try:
                trainerList = payloadToEdit["course"]['run']["linkCourseRunTrainer"]
            except:
                trainerList = []

            trainerObjectTemplate = {
                "trainer": {
                    "indexNumber": self.index,
                }
            }
            if (self.entry_trainerName.get() != ''):
                trainerObjectTemplate["trainer"]["name"] = self.entry_trainerName.get()
            if (self.entry_trainerEmail.get() != ''):
                trainerObjectTemplate["trainer"]["email"] = self.entry_trainerEmail.get()
            if (self.entry_trainerId.get() != ''):
                trainerObjectTemplate["trainer"]["id"] = self.entry_trainerId.get()
            if (self.entry_trainerExperience.get() != ''):
                trainerObjectTemplate["trainer"]["experience"] = self.entry_trainerExperience.get()
            if (self.entry_trainerlinkedInUrl.get() != ''):
                trainerObjectTemplate["trainer"]["linkedInURL"] = self.entry_trainerlinkedInUrl.get()
            if (self.entry_trainerdomainAreaOfPractice.get() != ''):
                trainerObjectTemplate["trainer"]["domainAreaOfPractice"] = self.entry_trainerdomainAreaOfPractice.get()
            if (self.trainersalutationId.get() != 'Select An Option'):
                trainerObjectTemplate["trainer"]["salutationId"] = int(self.trainersalutationId.get()[0])
            if (result != ''):
                trainerObjectTemplate["trainer"]["inTrainingProviderProfile"] = True if result == 'True' else False
            if (self.ssecList != []):
                trainerObjectTemplate["trainer"]["linkedSsecEQAs"] = self.ssecList
            if trainerCode != 'Select An Option' or self.entry_trainerTypeDescription.get() != '':
                trainerObjectTemplate["trainer"]["trainerType"] = {}
                if trainerCode != 'Select An Option':
                    trainerObjectTemplate["trainer"]["trainerType"]["code"] = trainerCode
                if self.entry_trainerTypeDescription.get() != '':
                    trainerObjectTemplate["trainer"]["trainerType"][
                        "description"] = self.entry_trainerTypeDescription.get()

            trainerList.append(trainerObjectTemplate)
            payloadToEdit['course']['run']['linkCourseRunTrainer'] = trainerList
            updateCourseRunPagePreview.payload = json.dumps(payloadToEdit, indent=4)
            tkinter.messagebox.showinfo(title="Success", message="Trainer successfully added")
            self.ssecList = []
            self.index = self.index + 1

            def clearEntryBox():
                self.entry_trainerName.delete(0, 'end')
                self.entry_trainerEmail.delete(0, 'end')
                self.entry_trainerId.delete(0, 'end')
                self.entry_trainerExperience.delete(0, 'end')
                self.entry_trainerlinkedInUrl.delete(0, 'end')
                self.entry_trainerdomainAreaOfPractice.delete(0, 'end')
                self.trainersalutationId.current(0)
                self.entry_trainerTypeDescription.delete(0, 'end')
                self.options_inTrainingProviderProfile.current(0)
                self.entry_trainerTypeCode.current(0)

            clearEntryBox()

        addssecEqasButton = tk.Button(self, text="add ssecEQA", bg="white", width=15, pady=5,
                                      command=lambda: addssecCallback())
        addssecEqasButton.place(relx=0.5, rely=0.70, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=15, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPagePage3))
        backButton.place(relx=0.35, rely=0.86, anchor=CENTER)
        addButton = tk.Button(self, text="Add Trainer", bg="white", width=15, pady=5, command=lambda: addCallback())
        addButton.place(relx=0.65, rely=0.80, anchor=CENTER)
        previewButton = tk.Button(self, text="Preview", bg="white", width=15, pady=5, command=lambda: callback())
        previewButton.place(relx=0.65, rely=0.86, anchor=CENTER)
        resetButton = tk.Button(self, text="Clear Trainer", bg="white", width=15, pady=5,
                                command=lambda: resetTrainers())
        resetButton.place(relx=0.35, rely=0.8, anchor=CENTER)


#Preview Page
class updateCourseRunPagePreview(tk.Frame):
    global contentInfo
    contentInfo = ''
    
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(curlPostRequest(updateCourseRunPagePreview.runIdEntered,updateCourseRunPagePreview.payload)))

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
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

        self.payload = '{}'
        self.runIdEntered = 0
        self.curlText = scrolledtext.ScrolledText(tab2, width=70, height=30)
        self.curlText.insert(tk.END,  str(curlPostRequest("","")))
        self.curlText.place(height=405, width=440, y=20)
        self.curlText.bind("<Key>", lambda e: "break")

        responseText = scrolledtext.ScrolledText(tab3, width=70, height=30)
        responseText.place(height=405, width=440, y=20)
        responseText.bind("<Key>", lambda e: "break")
            
        submitButton = tk.Button(self, text="Update", bg="white", width=25, pady=5, command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.15, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=5,
                               command=lambda: controller.show_frame(updateCourseRunPagePage4),
                               )
        backButton.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        #Exportbutton1 refers to Export Payload
        #Exportbutton2 refers to Export Response
        exportButton1 = tk.Button(self, text="Export Payload", bg="white", width=15, pady=5, command = lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.90, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Response", bg="white", width=15, pady=5,command = lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.90, anchor=CENTER)

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

        def submitCallBack():
            responseText.delete("1.0","end")
            resp = updateCourserun(updateCourseRunPagePreview.runIdEntered,updateCourseRunPagePreview.payload)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT,textPayload.get())
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
            filetext = str(updateCourseRunPagePreview.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")
            

class updateCourseRunPageFormFileUpload(tk.Frame):
    global fileUploadEntry
    global contentInfo
    contentInfo = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update Course Run", width=20, font=("bold", 20))
        label_0.place(x=90, y=33)

        
        #Course Run Id
        label_runId = Label(self, text="Course Run ID: ", width=20, font=("bold", 10), anchor='w')
        label_runId.place(x=100, y=90)

        entry_runId = Entry(self)
        entry_runId.place(x=270, y=90)
        label_1_ttp = CreateToolTip(label_runId, tooltipDescription["CourseRunId"])

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing():

            value = curlPostRequest(entry_runId.get(),contentInfo)
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)

        entry_runId.bind('<KeyRelease>', lambda b:typing())

        fileuploadframe = tk.Frame(self)
        fileuploadframe.place(x=100, y=123)

        fileUploadEntry = tk.Entry(fileuploadframe, width=45)
        fileUploadEntry.pack(side=tk.LEFT, fill=tk.X )
        fileUploadButton = tk.Button(self,text="Browse", command=lambda:getFile(self))       
        fileUploadButton.pack(in_=fileuploadframe, side=tk.LEFT)

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

        curlText = scrolledtext.ScrolledText(tab2,width=70,height=30)
        curlText.insert(tk.END, str(curlPostRequest("","")))
        curlText.place(height = 405, width = 440, y=20)
        curlText.bind("<Key>", lambda e: "break")
        
        responseText = scrolledtext.ScrolledText(tab3,width=70,height=30)
        responseText.place(height = 405, width = 440, y=20)
        # responseText.bind("<Key>", lambda e: "break")

        updateButton = tk.Button(self, text="Update", bg="white", width=25, pady=4, command=lambda: updateCallBack(entry_runId.get()))
        updateButton.place(relx=0.5, rely=0.223, anchor=CENTER)
        backButton = tk.Button(self, text="Back", bg="white", width=10, pady=4,
                               command=lambda: controller.show_frame(updateCourseRunPageSelect),
                               )
        backButton.place(relx=0.5, rely=0.27, anchor=CENTER)
        
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
                textw = curlText
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
            curlText.delete("1.0","end")
            filePath=filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
            fileUploadEntry.delete(0, 'end')
            fileUploadEntry.insert(1, filePath)
            global contentInfo
            with open(filePath, 'r') as content:
                contentInfo = content.read()

            curlText.insert(tk.END, curlPostRequest(entry_runId.get(),contentInfo))
                

        def updateCallBack(runId):
            responseText.delete("1.0","end")
            payload = contentInfo
            # payload = json.loads(payload)
            # print(payload)
            resp = updateCourserun(runId,payload)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT,textPayload.get())
            tabControl.select(tab3)

            
