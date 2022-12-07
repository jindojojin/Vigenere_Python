from tkinter import *
from customtkinter import *
from ProcessGUI import *

set_appearance_mode('dark')
set_default_color_theme('dark-blue')

DECRYPT_ACTION = "decrypt_action"
ENCRYPT_ACTION = "encrypt_action"


class MainWindow(CTk):
    def __init__(self, onAction=None):
        super().__init__()
        self.onAction=onAction
        self.draw()

        
    def draw(self):
        print("Init main window")
        self.configure(bg="grey10")
        self.geometry("440x140")
        self.title("FileLocker by linh.tq")
        frame = CTkFrame(self)
        
        encrypt_btn = CTkButton(frame,command=self.encryptFolder, text="🔒\n Encrypt a Folder", width=150, height=100)
        encrypt_btn.pack(side=LEFT, padx=20, pady=20)

        decrypt_btn = CTkButton(frame,command=self.decryptFolder, text="🔓\n Decrypt a Folder", width=150, height=100)
        decrypt_btn.pack(side=RIGHT, padx=20, pady=20)

        frame.pack(padx=20, pady=20)
        self.mainloop()

    def getAllFileInFolder(self,dirPath,fileExt=None):
        total_files = []
        total_size= 0
        for fileName in os.listdir(dirPath):
            path = os.path.join(dirPath, fileName)
            if(os.path.isfile(path) and (not fileExt or fileName.endswith(fileExt))):
                total_files.append(path)
                total_size += os.path.getsize(path)
            if(os.path.isdir(path)):
                files, size = self.getAllFileInFolder(path)
                total_files.extend(files)
                total_size += size
        return total_files, total_size
    
    def encryptFolder(self):
        dirPath = filedialog.askdirectory()
        if not len(dirPath): return
        folder_info = self.getAllFileInFolder(dirPath)
        Process(self,folder_info,ENCRYPT_PROCESS_MODE)
        
    
    def decryptFolder(self):
        dirPath = filedialog.askdirectory()
        if not len(dirPath): return
        folder_info = self.getAllFileInFolder(dirPath, ".vig")
        Process(self,folder_info,DECRYPT_PROCESS_MODE)

        

if __name__ == "__main__":
    MainWindow()

