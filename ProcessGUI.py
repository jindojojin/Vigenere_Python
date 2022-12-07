from threading import Thread
import time
from typing import Tuple
from customtkinter import *
from tkinter import Tk
import humanize

from Vigenere import Vigenenere
from hurry.filesize import size as size2Str

ENCRYPT_PROCESS_MODE = "Encrypt Folder"
DECRYPT_PROCESS_MODE = "Decrypt Folder"


class Process(CTkToplevel):
    def __init__(self, mainWindow: Tk, folderInfor:Tuple[str,int], mode=ENCRYPT_PROCESS_MODE):
        super().__init__(mainWindow)
        self.files, self.total_size = folderInfor
        self.total_file= len(self.files)
        self.mode = mode
        self.options = {
            "password":{
                "label":"Password",
                "type":"input",
                "placeholder":"Please enter your password"
            },
            "delete_origin_file":{
                "label":f"After {self.mode.lower()} success",
                "type":"options",
                "values":["Delete the original file","Keep the original file"]
            }
        }
        self.draw()

    def startTimer(self):
        self.startTime = time.time()
    def getElapsedTime(self):
        return humanize.precisedelta(time.time() - self.startTime, format="%d")

    def draw(self):
        self.WIDTH= 600
        self.HEIGHT=500
        # self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title(f"{self.mode}")
        self.drawJobInfo()
        self.drawOptionsTable()
        self.start_btn = CTkButton(self,text=f"Start {self.mode.lower()}", command=self.run)
        self.start_btn.grid(row=1, columnspan=2, padx=10, pady=10)

    def drawJobInfo(self):
        frame = CTkFrame(self, corner_radius=10)
        CTkLabel(frame, text=f"Num of files: {self.total_file}", padx=2, pady=2, corner_radius=5).grid(row=0,column=0)
        CTkLabel(frame, text=f"Total size: {size2Str(self.total_size)}", padx=2, pady=2, corner_radius=5).grid(row=1,column=0)
        frame.grid(row=0, column=0,padx=10, pady=5, sticky='w')

    def drawOptionsTable(self):
        frame = CTkFrame(self)  
        for i,key in enumerate(self.options):
            option = self.options[key]
            option['value']=StringVar()
            CTkLabel(frame,width=150,text=option['label'], anchor="w").grid(row=i, column=0, padx=2, pady=2, sticky='w')
            match(option['type']):
                case 'input':
                    option['gui'] = CTkEntry(frame,width=250,textvariable=option['value'],show="*")
                    option['gui'].grid(row=i, column=1, padx=2,pady=2)

                case 'options':
                    option['gui'] = CTkOptionMenu(frame,width=250, values=option['values'])
                    option['gui'].grid(row=i,column=1,padx=2, pady=2) 

        frame.grid(row=0,column=1, sticky='e', padx=10)

    def drawProgress(self):
        frame = CTkFrame(self)
        self.totalProgressStatus = StringVar()
        self.currentProgressStatus = StringVar()

        self.timerLabel = CTkLabel(frame)
        self.timerLabel.pack(side=TOP, padx=10)

        self.currentProgressLabel = CTkLabel(frame,textvariable=self.currentProgressStatus, anchor='w')
        self.currentProgressLabel.pack(side=TOP, anchor="w", padx=10)
        self.currentProgress = CTkProgressBar(frame,width=self.WIDTH*0.9,height=10,progress_color="green")
        self.currentProgress.set(0)
        self.currentProgress.pack(side=TOP, padx=10, pady=5)
        CTkLabel(frame,textvariable=self.totalProgressStatus, anchor='w').pack(side=TOP, ancho="w", padx=10)
        self.totalProgress = CTkProgressBar(frame,width=self.WIDTH*0.9, height=10, progress_color="green")
        self.totalProgress.set(0)
        self.totalProgress.pack(side=TOP, padx=10, pady=5)

        frame.grid(row=3,columnspan=2, padx=10, pady=10)

    def updateProgress(self, fileIndex, encrypted, fileSize):
        MAX_LENGHT = 50
        if fileIndex == self.total_file: # finish all
            self.currentProgress.pack_forget()
            self.currentProgressLabel.pack_forget()
        else:
            filename = self.files[fileIndex]
            self.currentProgress.set(0 if fileSize == 0 else encrypted/fileSize)
            self.currentProgressStatus.set(f"Current file: {filename if len(filename) < MAX_LENGHT else ' .....'+ filename[len(filename)-MAX_LENGHT:]} ({size2Str(encrypted)}/{size2Str(fileSize)})")

        self.timerLabel.configure(text=f"Elapsed time: {self.getElapsedTime()}")
        self.totalProgress.set(0 if self.total_file == 0 else fileIndex/self.total_file)
        self.totalProgressStatus.set(f"Total progress: {fileIndex}/{self.total_file} file(s)")

    def run(self):
        print("Do "+ self.mode)
        self.start_btn.configure(state=DISABLED)
        password = self.options['password']['gui'].get()
        delete_after_done =self.options['delete_origin_file']['gui'].get() == self.options['delete_origin_file']['values'][0]
        print(self.options['delete_origin_file']['gui'].get())
        vg = Vigenenere(password)
        def do_the_thing():
            self.startTimer()
            global currentFileSize
            mself = self
            def update_finished_byte(value,fileIndex):
                mself.updateProgress(fileIndex,value,currentFileSize)
            if(self.mode == ENCRYPT_PROCESS_MODE):
                for i,file in enumerate(self.files):
                    currentFileSize = os.path.getsize(file)
                    vg.encrypt(file,onProgressUpdate=lambda x : update_finished_byte(x,i), delete_after_done=delete_after_done)
            else:
                for i,file in enumerate(self.files):
                    currentFileSize = os.path.getsize(file)
                    vg.decrypt(file,onProgressUpdate=lambda x : update_finished_byte(x,i), delete_after_done=delete_after_done)
            mself.updateProgress(self.total_file, currentFileSize,currentFileSize)
            print("Done")
            time.sleep(1)
            mself.destroy()
        self.drawProgress()
        Thread(target=do_the_thing,daemon=True).start()                
        
if __name__== "__main__":
    win = Tk()
    pro = Process(win,(["hiihi.exe" for i in range(100)],100), DECRYPT_PROCESS_MODE)
    # pro.drawProgress()
    def update():
        print("do update")
        # pro.totalProgress.set(0.3)
        for i in range(100):
            print("update progress", i)
            pro.updateProgress(i,i,100)
            time.sleep(1)
    Thread(target=update).start()
    win.mainloop()
