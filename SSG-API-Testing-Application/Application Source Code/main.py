# CONTRIBUTIONS:
# Authors: Lam Zi Wen, Chua Mint Sheen Grace, Chong Zhe Ming

from resources import resource_path
from tkinter import Label, Menu
import tkinter as tk
from PIL import Image, ImageTk
from ViewDeleteCourseRun import viewCourseRunPage, deleteCourseRunPage
from AddCourseRun import addCourseRunPageForm, addCourseRunPageFormFileUpload, addCourseRunPage1, addCourseRunPage2, \
    addCourseRunPage3, addCourseRunPage4
from UpdateCourseRun import updateCourseRunPageFormFileUpload, updateCourseRunPagePage2, updateCourseRunPagePage3, \
    updateCourseRunPagePage4, updateCourseRunPagePreview, updateCourseRunPageSelect
from CourseSession import getCourseSessionPage
from AddEnrolment import AddEnrolmentMainPage, AddEnrolmentPage2, AddEnrolmentPreviewPage, addEnrolmentPageFileUpload
from ViewEnrolment import viewEnrolmentPage, deleteEnrolmentPage
from UpdateEnrolment import UpdateEnrolmentMainPage, UpdateEnrolmentPageFileUploadPage, UpdateEnrolmentPreviewPage
from SearchEnrolment import searchEnrolmentPage1, searchEnrolmentPage2
from UpdateEnrolmentFeeCollection import updateEnrolFeePage
from UpdateAssessment import UpdateAssessmentMainPage, UpdateAssessmentPageFileUploadPage, UpdateAssessmentPreviewPage
from addAssessment import AddAssessmentMainPage, AddAssessmentPreviewPage, addAssessmentPageFileUpload
from SearchAssessment import searchAssessmentPage1, searchAssessmentPage2
from ViewAssessment import ViewAssessmentPage
from ViewCourseSessionAttendance import ViewSessionAttendance
from AddAttendance import addAttendancePage1, addAttendancePage2
from tkinter.constants import CENTER
from configWindow import setConfigWindow, showConfigWindow


# Quit Program
def quit_program():
    quit()



class APIProject(tk.Tk):

    def __init__(self, *args, **kwargs):

            
        tk.Tk.__init__(self, *args, *kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
                UpdateAssessmentPreviewPage, UpdateAssessmentPageFileUploadPage, UpdateAssessmentMainPage,
                updateEnrolFeePage,
                ViewSessionAttendance, ViewAssessmentPage,
                UpdateEnrolmentMainPage, UpdateEnrolmentPageFileUploadPage, UpdateEnrolmentPreviewPage,
                AddEnrolmentPage2, AddEnrolmentPreviewPage, addEnrolmentPageFileUpload, AddEnrolmentMainPage,
                deleteEnrolmentPage, viewEnrolmentPage, getCourseSessionPage, updateCourseRunPagePreview,
                updateCourseRunPagePage2, updateCourseRunPagePage3,
                updateCourseRunPagePage4, updateCourseRunPageFormFileUpload, updateCourseRunPageSelect,
                addCourseRunPageFormFileUpload, addCourseRunPageForm, addCourseRunPage4,
                addCourseRunPage3, addCourseRunPage2, addCourseRunPage1, viewCourseRunPage, deleteCourseRunPage,
                searchEnrolmentPage1, searchEnrolmentPage2,
                addAttendancePage1, addAttendancePage2,
                searchAssessmentPage1, searchAssessmentPage2,
                AddAssessmentMainPage, AddAssessmentPreviewPage, addAssessmentPageFileUpload, StartPage):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        #Menubar
        menubar = Menu(self, background='#ff8000', foreground='black', activebackground='white',
                       activeforeground='black')

        config = Menu(menubar, tearoff=0)
        config.add_command(label="Set Configuration", command=lambda: setConfigCallback())
        config.add_command(label="Show Configuration", command=lambda: showConfigWindow(self))
        menubar.add_cascade(label="Setting", menu=config)

        courseMenu = Menu(menubar, tearoff=0)
        courseMenu.add_command(label="View Course Run", command=lambda: self.show_frame(viewCourseRunPage))
        courseMenu.add_command(label="Add Course Run", command=lambda: self.show_frame(addCourseRunPage1))
        courseMenu.add_command(label="Delete Course Run", command=lambda: self.show_frame(deleteCourseRunPage))
        courseMenu.add_command(label="Update Course Run", command=lambda: self.show_frame(updateCourseRunPageSelect))
        courseMenu.add_command(label="Course Session", command=lambda: self.show_frame(getCourseSessionPage))
        menubar.add_cascade(label="Course", menu=courseMenu)

        enrolmentMenu = Menu(menubar, tearoff=0)
        enrolmentMenu.add_command(label="Create Enrolment", command=lambda: self.show_frame(AddEnrolmentMainPage))
        enrolmentMenu.add_command(label="Update Enrolment", command=lambda: self.show_frame(UpdateEnrolmentMainPage))
        enrolmentMenu.add_command(label="Delete Enrolment", command=lambda: self.show_frame(deleteEnrolmentPage))
        enrolmentMenu.add_command(label="Search Enrolment", command=lambda: self.show_frame(searchEnrolmentPage1))
        enrolmentMenu.add_command(label="View Enrolment", command=lambda: self.show_frame(viewEnrolmentPage))
        enrolmentMenu.add_command(label="Update Enrolment Fee Collection",
                                  command=lambda: self.show_frame(updateEnrolFeePage))
        menubar.add_cascade(label="Enrolment", menu=enrolmentMenu)

        attendanceMenu = Menu(menubar, tearoff=0)
        attendanceMenu.add_command(label="Course Session Attendance",
                                   command=lambda: self.show_frame(ViewSessionAttendance))
        attendanceMenu.add_command(label="Upload Course Session Attendance",
                                   command=lambda: self.show_frame(addAttendancePage1))
        menubar.add_cascade(label="Attendance", menu=attendanceMenu)

        assessmentMenu = Menu(menubar, tearoff=0)
        assessmentMenu.add_command(label="Create Assessment", command=lambda: self.show_frame(AddAssessmentMainPage))
        assessmentMenu.add_command(label="Update/Void Assessment",
                                   command=lambda: self.show_frame(UpdateAssessmentMainPage))
        assessmentMenu.add_command(label="Search Assessment", command=lambda: self.show_frame(searchAssessmentPage1))
        assessmentMenu.add_command(label="View Assessment", command=lambda: self.show_frame(ViewAssessmentPage))
        menubar.add_cascade(label="Assessment", menu=assessmentMenu)

        self.config(menu=menubar)

        # This method "blank" out the menubar to prevent duplicate opening of window for Setting
        def setConfigCallback():
            top2 = setConfigWindow(self)
            top2.transient(self)
            top2.grab_set()
            self.wait_window(top2)

        def recreateFrame(classObject):
            frame = classObject(self.container, self)
            self.frames[classObject] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        def reInitialiseFrame(FrameName):
            recreateFrame(FrameName)
            self.show_frame(FrameName)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # Starting Page (Welcome Page)


# 2 options for the user to choose from
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFMenuPage.JPG")
        load = Image.open(file_path)

        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        # button1 = tk.Button(self, text="Press to start the Navigation", bg="white", width=25, pady=5,
        #                     command=lambda: controller.show_frame(PageOne))  # go to Page One
        # button1.place(relx=0.5, rely=0.65, anchor=CENTER)
        button2 = tk.Button(self, text="Exit", bg="white", width=25, pady=5,
                            command=quit_program)  # quit program
        button2.place(relx=0.5, rely=0.7, anchor=CENTER)

    def show_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)


app = APIProject()
app.geometry("500x747")
app.winfo_toplevel().title("SSG API Testing Application")
app.resizable(0, 0)
app.mainloop()
