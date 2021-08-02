
from resources import *
from AssessmentFunction import displayUpdateAssessment, updateAssessment
from re import S
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
        
#Page 1 for Create Enrolment
class UpdateAssessmentMainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)
        #Variable
        #This list will be used to generate the payload layout for Trainee

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="Update/Void Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=53)

        self.var = IntVar()
        Radiobutton(self, text="Upload a Assessment JSON File", variable=self.var, value=1, width=25, anchor='w').place(x=158,y=100)
        Radiobutton(self, text="Fill in the basic mandate form", variable=self.var, value=2,width=25, anchor='w').place(x=158,y=130)
        self.var.set(2)

        label_0 = Label(self, text="Assessment Details", width=20, font=("bold", 15))
        label_0.place(x=137, y=195)

        self.label_EnrolRefNum = Label(self, text="Reference Number*", width=20, font=("bold", 10), anchor='w')
        self.label_EnrolRefNum.place(x=100, y=230)

        label_EnrolRefNum_ttp = CreateToolTip(self.label_EnrolRefNum, tooltipDescription["EnrolRefNum"])

        self.entry_EnrolRefNum = Entry(self)
        self.entry_EnrolRefNum.place(x=270, y=230)

        self.Label_Action = Label(self, text="Action*", width=20, font=("bold", 10), anchor='w')
        self.Label_Action.place(x=100, y=255)
        self.Label_Actionl_ttp = CreateToolTip(self.Label_Action, tooltipDescription["Action"])
        self.Action = ttk.Combobox(self, width = 17,state="readonly")
        self.Action['values'] = ["Select An Option",
                     "Update",
                     "Void"
                     ]
        self.Action.current(0)
        self.Action.place(x=270, y=255)
        def changeLabel():
            if self.Action.get() == 'Void' or self.Action.get() == 'Select An Option':
                self.Grade.place_forget()
                self.Result.place_forget()
                self.entry_AssessmentDate.place_forget()
                self.entry_Name.place_forget()
                self.entry_SkillCode.place_forget()
                self.Label_SkillCode.place_forget()
                self.Label_AssessmentDate.place_forget()
                self.Label_Name.place_forget()
                self.Label_Grade.place_forget()
                self.Label_Result.place_forget()
                self.Label_Score.place_forget()
                self.entry_Score.place_forget()
            else:
                self.Label_Grade.place(x=100, y=280)
                self.Grade.place(x=270, y=280)
                self.Label_Result.place(x=100, y=305)
                self.Result.place(x=270, y=305)
                self.Label_Score.place(x=100, y=330)
                self.entry_Score.place(x=270, y=330)
                self.Label_Name.place(x=100, y=355)
                self.entry_Name.place(x=270, y=355)
                self.Label_SkillCode.place(x=100, y=380)
                self.entry_SkillCode.place(x=270, y=380)
                self.Label_AssessmentDate.place(x=100, y=405)
                self.entry_AssessmentDate.place(x=270, y=405)

        self.Action.bind('<<ComboboxSelected>>', lambda x: changeLabel())

        self.Label_Grade = Label(self, text="Grade", width=20, font=("bold", 10), anchor='w')
        self.Label_Grade.place(x=100, y=280)

        self.Label_Grade_ttp = CreateToolTip(self.Label_Grade, tooltipDescription["Grade"])
        
        self.Grade = ttk.Combobox(self, width = 17,state="readonly")
        self.Grade['values'] = ["Select An Option",
                     "A",
                     "B",
                     "C",
                     "D",
                     "E",
                     "F"
                     ]
        self.Grade.current(0)
        self.Grade.place(x=270, y=280)
        
        self.Label_Result = Label(self, text="Results", width=20, font=("bold", 10), anchor='w')
        self.Label_Result.place(x=100, y=305)

        self.Label_Result_ttp = CreateToolTip(self.Label_Result, tooltipDescription["Result"])
        
        self.Result = ttk.Combobox(self, width = 17,state="readonly")
        self.Result['values'] = ["Select An Option",
                     "Pass",
                     "Fail",
                     "Exempt "
                     ]
        self.Result.current(0)
        self.Result.place(x=270, y=305)
        
        self.Label_Score = Label(self, text="Score", width=20, font=("bold", 10), anchor='w')
        self.Label_Score.place(x=100, y=330)
        self.Label_Score_ttp = CreateToolTip(self.Label_Score, tooltipDescription["Score"])
        self.entry_Score = Entry(self)
        self.entry_Score.place(x=270, y=330)

        self.Label_Name = Label(self, text="Trainee Full Name", width=20, font=("bold", 10), anchor='w')
        self.Label_Name.place(x=100, y=355)
        self.Label_Name_ttp = CreateToolTip(self.Label_Name, tooltipDescription["TrainerName"])
        self.entry_Name  = Entry(self)
        self.entry_Name.place(x=270, y=355)

        self.Label_SkillCode = Label(self, text="Skill Code", width=20, font=("bold", 10), anchor='w')
        self.Label_SkillCode.place(x=100, y=380)
        self.Label_SkillCode_ttp = CreateToolTip(self.Label_SkillCode, tooltipDescription["skillCode"])
        self.entry_SkillCode  = Entry(self)
        self.entry_SkillCode.place(x=270, y=380)

        self.Label_AssessmentDate = Label(self, text="Assessment Date", width=20, font=("bold", 10), anchor='w')
        self.Label_AssessmentDate.place(x=100, y=405)
        self.Label_AssessmentDate_ttp = CreateToolTip(self.Label_AssessmentDate, tooltipDescription["assessmentDate"])
        self.entry_AssessmentDate  = Entry(self)
        self.entry_AssessmentDate.place(x=270, y=405)


        nextButton = tk.Button(self, text="Next", bg="white", width=25, pady=5, command=lambda: NextCallBack() if self.var.get() == 2 else controller.show_frame(UpdateAssessmentPageFileUploadPage))
        nextButton.place(x=250, y=675, anchor=CENTER)

        #This function is used during the initialization to hide certain label
        changeLabel()

        def NextCallBack():
            UpdateAssessmentPreviewPage.payload = StoreAndSave()
            UpdateAssessmentPreviewPage.refresh(controller.frames[UpdateAssessmentPreviewPage].curlText)
            controller.show_frame(UpdateAssessmentPreviewPage)
            
        def StoreAndSave():
            payload = {}
            payload['assessment'] = {}
            payload['assessment']['action'] = self.Action.get() if self.Action.get() != 'Select An Option' else {}
            if self.Action.get() != 'Void':
                if self.entry_Name.get() != '':
                    payload['assessment']['trainee'] = {'fullName':self.Action.get()}
                if self.entry_AssessmentDate.get() != '':
                    payload['assessment']['assessmentDate'] = self.entry_AssessmentDate.get()
                if self.entry_SkillCode.get() != '':
                    payload['assessment']['skillCode'] = self.entry_SkillCode.get()            
                if self.Grade.get() != 'Select An Option':
                    payload['assessment']['grade'] = self.Grade.get()
                if self.entry_Score.get() != '':
                    payload['assessment']['score'] = self.entry_Score.get()
                if self.Result.get() != 'Select An Option':
                    payload['assessment']['result'] = self.Result.get()
            UpdateAssessmentPreviewPage.refNumber = self.entry_EnrolRefNum.get()       
            return str(json.dumps(payload, indent=4))
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class UpdateAssessmentPreviewPage(tk.Frame):
    def refresh(controllerCurlText):
        controllerCurlText.delete("1.0","end")
        controllerCurlText.insert(tk.END, str(displayUpdateAssessment(UpdateAssessmentPreviewPage.refNumber,UpdateAssessmentPreviewPage.payload)))

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
        label_0 = Label(self, text="Update Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=43)

        # Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        # Configuration for Notebook layout
        tabControl = ttk.Notebook(self)

        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)

        # Adding of tabs
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
                               command=lambda: controller.show_frame(UpdateAssessmentMainPage),
                               )
        backButton.place(relx=0.5, rely=0.2, anchor=CENTER)
        exportButton1 = tk.Button(self, text="Export Decrypted Payload", bg="white", width=20, pady=3, command = lambda: downloadFile("payload"))
        exportButton1.place(relx=0.3, rely=0.90, anchor=CENTER)
        exportButton2 = tk.Button(self, text="Export Decrypted Response", bg="white", width=20, pady=3,command = lambda: downloadFile("response"))
        exportButton2.place(relx=0.7, rely=0.90, anchor=CENTER)
        
        
        self.varPayload = IntVar()
        Radiobutton(tab2, text="Decrypt", variable=self.varPayload, value=1, width=12, anchor='w', command = lambda:displayPayload("decrypt")).place(x=0,y=-5)
        Radiobutton(tab2, text="Encrypt", variable=self.varPayload, value=2,width=12, anchor='w',command = lambda:displayPayload("encrypt")).place(x=130,y=-5)
        self.varPayload.set(1)

        self.varResp = IntVar()
        Radiobutton(tab3, text="Decrypt", variable=self.varResp, value=1, width=12, anchor='w', command = lambda:displayResp("decrypt")).place(x=0,y=-5)
        Radiobutton(tab3, text="Encrypt", variable=self.varResp, value=2,width=12, anchor='w',command = lambda:displayResp("encrypt")).place(x=130,y=-5)
        self.varResp.set(1)
        # adding of single line text box
        edit = Entry(self, background="light gray")
        edit.place(x=285, height=21, y=204)
        edit.focus_set()

        butt_resp = Button(tab2, text='Find', command=lambda: find("curl"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        butt_resp = Button(tab3, text='Find', command=lambda: find("resp"), highlightthickness=0, bd=0,
                           background="gray")
        butt_resp.place(x=380, y=0, height=21, width=60)
        
        def displayPayload(method):
            if method != 'decrypt':
                payloadToDisplay = doEncryption(str(UpdateAssessmentPreviewPage.payload).encode()).decode()
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayUpdateAssessment(UpdateAssessmentPreviewPage.refNumber,payloadToDisplay)))
            else:
                self.curlText.delete("1.0","end")
                self.curlText.insert(tk.END, str(displayUpdateAssessment(UpdateAssessmentPreviewPage.refNumber,UpdateAssessmentPreviewPage.payload)))

        def displayResp(method):
            if method != 'encrypt':
                try:
                    display = UpdateAssessmentPreviewPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(UpdateAssessmentPreviewPage.textPayload.get()).encode())
                except:
                    display = b''
                
                responseText.delete("1.0","end")
                responseText.insert(tk.END, display.decode())

        def updateCallBack():
            responseText.delete("1.0","end")
            resp = updateEnrolment(UpdateAssessmentPreviewPage.refNumber,UpdateAssessmentPreviewPage.payload)
            try:
                    resp = doDecryption(resp)
                    resp = json.loads(resp.decode())
                    resp = str(json.dumps(resp,indent=4))
            except:
                pass
                
            UpdateAssessmentPreviewPage.textPayload = StringVar(self, value = resp) 
            responseText.insert(INSERT,UpdateAssessmentPreviewPage.textPayload.get())
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
            filetext = str(UpdateAssessmentPreviewPage.payload) if method == "payload" else str(
                responseText.get("1.0", END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

#File Upload Page for UpdateEnrolment
class UpdateAssessmentPageFileUploadPage(tk.Frame):
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

        label_0 = Label(self, text="Update Assessment", width=20, font=("bold", 20))
        label_0.place(x=90, y=33)

        #Course Run Id
        label_EnrolRefNum = Label(self, text="Reference Number*", width=20, font=("bold", 10), anchor='w')
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
                               command=lambda: controller.show_frame(UpdateAssessmentMainPage),
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
                    display = UpdateAssessmentPageFileUploadPage.textPayload.get()
                except:
                    display = ''
                responseText.delete("1.0","end")
                responseText.insert(INSERT,display)
            else:
                try:
                    display = doEncryption(str(UpdateAssessmentPageFileUploadPage.textPayload.get()).encode())
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
                resp = updateAssessment(self.entry_EnrolRefNum.get(),payload)
                try:
                    resp = doDecryption(resp)
                    resp = json.loads(resp.decode())
                    resp = str(json.dumps(resp,indent=4))
                except:
                    pass
                
                UpdateAssessmentPageFileUploadPage.textPayload = StringVar(self, value = resp)
                responseText.insert(INSERT,UpdateAssessmentPageFileUploadPage.textPayload.get())
                self.varResp.set(1)
                tabControl.select(tab3)


        def downloadFile():
            try:
                filetext = str(UpdateAssessmentPageFileUploadPage.textPayload.get())
                files = [('JSON', '*.json'),
                        ('Text Document', '*.txt')]
                file = filedialog.asksaveasfile(filetypes=files, defaultextension='.json')
                file.write(filetext)
                file.close()
                messagebox.showinfo("Successful", "File has been downloaded")
            except:
                messagebox.showerror("Error", "Unable to download File - Empty Response")