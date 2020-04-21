import os
from tkinter import *
from glob import glob
from tkinter.messagebox import askyesno
from PIL.ImageTk import PhotoImage
from tkinter.filedialog import askdirectory
import random

Size = (450, 450)
imageTypes = [('Gif (*.gif)', '.gif'),
              ('Ppm (*.ppm)', '.ppm'),
              ('Pgm (*.pgm)', '.pgm'),
              ('JPEG (*.jpg;*.jpeg;*.jpe;*.jfif)', '.jpg;.jpeg;.jpe;.jfif'),
              ('PNG (*.png)', '.png'),
              ('All files', '*')]

ImageTypes = [('Gif files', '.gif'),
              ('Ppm files', '.ppm'),
              ('Pgm files', '.pgm'),
              ('JPEG files', '.jpg'),
              ('PNG files', '.png'),
              ('All files', '*')]


class SlideShow(Frame):
    def __init__(self, parent=None, picdir='.', msecs=3000, size=Size, **args):
        super().__init__(parent, **args)
        self.size = size
        self.makeWidgets()
        self.pack(expand=YES, fill=BOTH)
        self.opens = picdir
        files = []
        for _, ext in ImageTypes[:-1]:
            files = files + glob('%s/*%s' %(picdir, ext))
        #print(files)
        self.images = [(x, PhotoImage(file=x)) for x in files]
        self.msecs = msecs
        self.beep = True
        self.drawn = None

    def makeWidgets(self):
        height, width = self.size
        self.canvas = Canvas(self, bg='white', height=height, width=width)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.OnOff = Button(self, text='Start', command=self.onStart)
        self.OnOff.pack(fill=X)
        Button(self, text='Open', command=self.onOpen).pack(fill=X)
        Button(self, text='Beep', command=self.onBeep).pack(fill=X)
        Button(self, text='Quit', command=self.onQuit).pack(fill=X)

    def onStart(self):
        self.loop = True
        self.OnOff.config(text='Stop', command=self.onStop)
        self.canvas.config(height=self.size[0], width=self.size[1])
        self.onTimer()

    def onStop(self):
        self.loop = False
        self.OnOff.config(text='Start', command=self.onStart)

    def onOpen(self):
        self.onStop()
        name = askdirectory()
        if name:
            self.images = [(x, PhotoImage(file=name+'/'+x)) for x in os.listdir(name)]
            #print(self.images)
            if self.drawn:
                self.canvas.delete(self.drawn)
            img = PhotoImage(file=name+'/'+self.images[0][0])
            self.canvas.config(height=img.height(), width=img.width())
            self.drawn = self.canvas.create_image(2, 2, image=img, anchor=NW)
            self.canvas.update()
            #print(self.drawn)     
            
            self.image = name+'/'+self.images[0][0], img

    def onQuit(self):
        self.onStop()
        self.update()
        if askyesno('PyView', 'Really quit now?'):
            self.quit()

    def onBeep(self):
        self.beep = not self.beep

    def onTimer(self):
        if self.loop:
            self.drawNext()
            self.after(self.msecs, self.onTimer)

    def drawNext(self):
        if self.drawn:
            self.canvas.delete(self.drawn)
        name, img = random.choice(self.images)
        self.drawn = self.canvas.create_image(2, 2, image=img, anchor=NW)
        self.image = name, img
        if self.beep:
            self.bell()
        self.canvas.update()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        picdir = sys.argv[1]
    else:
        picdir = '../gifs'
    root = Tk()
    root.title('PyView')
    root.iconname('PyView')
    Label(root, text='Python Slide Show Viewer').pack()
    SlideShow(root, picdir=picdir, bd=3, relief=SUNKEN)
    root.mainloop()