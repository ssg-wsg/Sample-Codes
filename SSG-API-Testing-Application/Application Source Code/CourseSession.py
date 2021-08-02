import json
from resources import *
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, ttk, scrolledtext, filedialog
from tkinter import messagebox
from tkinter.constants import CENTER, END, INSERT
from PIL import ImageTk, Image
from courseRunFunctions import curlGetCourseSession, getCourseSession
from tooltip import CreateToolTip

#Load Tooltip Json object as ttDescription
with open(tooltip_path) as f:
    tooltipDescription = json.load(f)


# ViewCourseSession Page
class getCourseSessionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        file_path = resource_path("SKFBGPage.JPG")
        load = Image.open(file_path)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img2 = Label(self, image=render)
        img2.image = render
        img2.place(x=0, y=0, relwidth=1, relheight=1)

        label_0 = Label(self, text="View Course Sessions", width=20, font=("bold", 20))
        label_0.place(x=90, y=23)

        label_runId = Label(self, text="Course Run ID*", width=21, font=("bold", 10), anchor='w')
        label_runId.place(x=105, y=90)
        label_runId_ttp = CreateToolTip(label_runId, tooltipDescription["CourseRunId"])
        entry_runId = Entry(self)
        entry_runId.place(x=275, y=90)

        label_CRN = Label(self, text="Course References Number*", width=21, font=("bold", 10), anchor='w')
        label_CRN.place(x=105, y=120)
        label_CRN_ttp = CreateToolTip(label_CRN, tooltipDescription["CourseReferenceNumber"])
        entry_CRN = Entry(self)
        entry_CRN.place(x=275, y=120)

        label_sessionMonth = Label(self, text="Session Month (Optional)", width=21, font=("bold", 10), anchor='w')
        label_sessionMonth.place(x=105, y=150)
        label_sessionMonth_ttp = CreateToolTip(label_sessionMonth, tooltipDescription["SessionMonth"])
        entry_sessionMonth = Entry(self)
        entry_sessionMonth.place(x=275, y=150)

        #This method is used to update the display information dynamically in "Payload" Tab whenever user key in a value
        def typing(event):
            value = curlGetCourseSession(entry_runId.get(), entry_CRN.get(), entry_sessionMonth.get())
            curlText.delete("1.0","end")
            curlText.insert(tk.END, value)

        entry_runId.bind('<KeyRelease>',typing)
        entry_CRN.bind('<KeyRelease>',typing)
        entry_sessionMonth.bind('<KeyRelease>',typing)

        #Expand label to fit window size
        style = ttk.Style(self)
        style.configure('TNotebook.Tab', width=self.winfo_screenwidth())

        #Configuration for Notebook layout
        tabControl = ttk.Notebook(self)
  
        responseFrame = ttk.Frame(tabControl)
        curlFrame = ttk.Frame(tabControl)

        tabControl.add(curlFrame, text ='Request')
        tabControl.add(responseFrame, text ='Reponse')

        tabControl.place(width= 440, height= 460, x = 30, y = 222)

        #Textbox for response Frame
        responseText = scrolledtext.ScrolledText(responseFrame,width=70,height=30)
        responseText.place(height = 405, width = 440,y=20)
        responseText.bind("<Key>", lambda e: "break")

        #Textbox for Curl Frame
        curlText = scrolledtext.ScrolledText(curlFrame,width=70,height=30)
        curlText.insert(tk.END, str(curlGetCourseSession("","","")))
        curlText.place(height = 405, width = 440, y=20)
        curlText.bind("<Key>", lambda e: "break")

        #adding of single line text box
        edit = Entry(self, background="light gray") 

        #positioning of text box
        edit.place(x = 285, height= 21, y=244) 

        #setting focus
        edit.focus_set()

        butt = Button(responseFrame, text='Find', command=lambda:find("resp"), highlightthickness = 0, bd = 0, background="gray")  
        butt.place(x = 380, y=0, height=21, width=60) 
        butt_curl = Button(curlFrame, text='Find', command=lambda:find("curl"), highlightthickness = 0, bd = 0, background="gray")  
        butt_curl.place(x = 380, y=0, height=21, width=60) 
        


        submitButton = tk.Button(self, text="Submit", bg="white", width=25, pady=5,
                            command=lambda: submitCallBack())
        submitButton.place(relx=0.5, rely=0.27, anchor=CENTER)
        exportButton = tk.Button(self, text="Export Response", bg="white", width=25, pady=5, command = lambda: downloadFile())
        exportButton.place(relx=0.5, rely=0.95, anchor=CENTER)

        
        # This method activates two other methods.
        # 1) this method calls the get method in courseRunFunction and return the response
        # 2) Based on the response, if a status 200 is received, it will display the response    
        def submitCallBack():
            responseText.delete("1.0","end") 
            resp = getCourseSession(entry_runId.get(), entry_CRN.get(), entry_sessionMonth.get())
            print(resp.status_code)
            textPayload = StringVar(self, value = resp.text) 
            responseText.insert(INSERT, textPayload.get())
        def downloadFile():
            files = [('JSON', '*.json'), 
                     ('Text Document', '*.txt')]
            file = filedialog.asksaveasfile(filetypes = files, defaultextension='.json')
            filetext = str(responseText.get("1.0",END))
            file.write(filetext)
            file.close()
            messagebox.showinfo("Successful", "File has been downloaded")

        #This method is used to search the response text and highlight the searched word in red
        def find(method):
            if method == "resp":
                textw = responseText
            else:
                textw = curlText
            #remove tag 'found' from index 1 to END
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

    def show_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = new_frame_class(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)
