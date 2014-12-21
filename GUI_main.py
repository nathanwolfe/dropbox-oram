from tkinter import *
from tkinter.ttk import *

class DropboxORAM(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)       
        self.parent = parent
        self.initUI()

    def Sync(self):
        print("Hello")
        
    def initUI(self):
        self.parent.title("Dropbox-ORAM")
        self.pack(fill=BOTH, expand=1)

        Sync = Button(self, text = "Sync", command = self.Sync)
        Sync.pack()
        Quit = Button(self, text = "Quit", command=self.quit)
        Quit.pack()
        
def main():
    root = Tk()
    root.geometry("100x100")
    root.wm_iconbitmap("DB_O.ico")
    app = DropboxORAM(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
