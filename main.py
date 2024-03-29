from tkinter import messagebox,ttk
from PIL import Image,ImageTk
from tkinter import *
from pygame import *
from threading import Thread
import PIL.Image
import os.path
import easygui
import urllib.request
import bs4
import cv2

class MainWindow:
    
    def __init__(self):
        #HEAD_____________________________________________________________________________________
        self.version=0.1
        self.root=Tk()
        self.root.geometry('680x480')
        self.root.title(f'SMBX 1/2 Graphic Editor ({self.version})')
        self.root.iconphoto(True,PhotoImage(file='icon.png'))
        self.title_label=Label(text='SMBX Graphic Editor by Rhubarb06150').place(x=2,y=2)

        #DEFAULT WIDGETS _________________________________________________________________________

        self.level_path=None
        self.custom_graphic_choosen=None
        self.level_path_button=Button(text='Choose level folder',command= lambda: self.ChooselevelPath(),height=1)
        self.level_path_button.place(x=540,y=0)
        self.gte=Label(self.root,text='Graphic you want to edit:').place(x=25,y=50)
        self.graphic_type=ttk.Combobox(self.root,values=['block-','effect-','npc-'],width=7)
        self.graphic_type.set('block-')
        self.graphic_type.place(x=50,y=75)
        self.graphic_num=Entry(self.root,width=7)
        self.graphic_num.place(x=120,y=75)
        self.graphic_select_button=Button(text='Select custom graphic',command= lambda: self.SelectCustomGraphic())
        self.graphic_select_button.place(x=170,y=70)

        #IMAGES __________________________________________________________________________________
        
        self.arrow=Label(self.root,image=ImageTk.PhotoImage(file='arrow.png'),borderwidth=0)
        self.arrow.place(x=82,y=100)
        self.arrow.im=ImageTk.PhotoImage(file='no-img.png')

        self.custom_graphic=Label(self.root,image=ImageTk.PhotoImage(file='arrow.png'),borderwidth=0)
        self.custom_graphic.place(x=82,y=100)

        self.img=Label(self.root,borderwidth=0)
        self.img.place(x=50,y=100)

        self.root.bind('<Return>', lambda event:self.ShowCurrentGraphic())
        self.root.bind('<Control-S>', lambda event:self.SaveGraphic())
        self.root.bind('<Control-s>', lambda event:self.SaveGraphic())

        #ANIMATION _______________________________________________________________________________

        self.framerate=Entry(self.root,width=5)
        self.framerate.place(x=490,y=70)
        self.framerate_label=Label(self.root,text='Framespeed (t/s):')
        self.framerate_label.place(x=390,y=70)

        self.anim_width=Entry(self.root,width=5)
        self.anim_width.place(x=460,y=90)
        self.anim_width_label=Label(self.root,text='Width (px):')
        self.anim_width_label.place(x=390,y=90)

        self.anim_height=Entry(self.root,width=5)
        self.anim_height.place(x=460,y=110)
        self.anim_height_label=Label(self.root,text='Height (px):')
        self.anim_height_label.place(x=390,y=110)

        self.frames_nb=Entry(self.root,width=5)
        self.frames_nb.place(x=440,y=130)
        self.frames_nb_label=Label(self.root,text='Frames:')
        self.frames_nb_label.place(x=390,y=130)

        self.animated=BooleanVar()
        self.animated_checkbox=Checkbutton(self.root,text='Animated?',var=self.animated,command=self.ShowAnimationMenu)
        self.animated_checkbox.place(x=300,y=68)
    
        self.root.mainloop()

    def ShowAnimationMenu(self):

        if self.animated.get():
            self.framerate.place(x=490,y=70)
            self.framerate_label.place(x=390,y=70)
            self.anim_width.place(x=460,y=90)
            self.anim_width_label.place(x=390,y=90)
            self.anim_height.place(x=460,y=110)
            self.anim_height_label.place(x=390,y=110)
            self.frames_nb.place(x=440,y=130)
            self.frames_nb_label.place(x=390,y=130)

        else:
            self.framerate_label.place_forget()
            self.framerate.place_forget()
            self.anim_width.place_forget()
            self.anim_width_label.place_forget()
            self.anim_height.place_forget()
            self.anim_height_label.place_forget()
            self.frames_nb.place_forget()
            self.frames_nb_label.place_forget()



    def SelectCustomGraphic(self):
        path=easygui.fileopenbox(title='Choose your custom graphic',filetypes=[['*.png','*.jpg','*.jpeg','Images only']])
        if path!=None:
            self.custom_graphic_choosen=path
        self.ShowCurrentGraphic()

    def SaveGraphic(self):
        if self.level_path==None:
            msg=messagebox.showerror(title='Error',message='Please choose an level folder first')
        else:
            PIL.Image.open(self.custom_graphic_choosen).save(f'{self.level_path}\\{self.graphic_type.get()}{self.graphic_num.get()}.png')

    def ShowCurrentGraphic(self):

        path=f'smbxdata\\{self.graphic_type.get().replace('-','')}\\{self.graphic_type.get()}{self.graphic_num.get()}.png'

        try:
            img=ImageTk.PhotoImage(file=path)
            h,w,c=cv2.imread(path).shape
        except:
            img=ImageTk.PhotoImage(file='no-img.png')
            h,w=32,32

        self.img.configure(image=img)
        self.img.im=img

        arrow_im=ImageTk.PhotoImage(file='arrow.png')
        self.arrow.configure(image=arrow_im)
        self.arrow.im=arrow_im

        self.arrow.place_forget()

        if self.custom_graphic_choosen!=None:
            img=ImageTk.PhotoImage(file=self.custom_graphic_choosen)
            self.custom_graphic.configure(image=img)
            self.custom_graphic.im=img
            self.custom_graphic.place(x=82+w,y=100)
            self.arrow.place(x=50+w,y=100)



    def ChooselevelPath(self):
        path=easygui.diropenbox(title='Choose your level folder')
        if path!=None:
            self.root.title(f'SMBX 1/2 Graphic Editor ({self.version}) => level: {os.path.basename(path)}')
            self.level_path=path

    def GetLastVersion(self):
        content=urllib.request.urlopen('https://mcrhubarb.net/softwares/index.html')
        content=bs4.BeautifulSoup(content, 'html.parser')
        verspan = content.find(id='smbxgever')
        self.last_ver=verspan=float(verspan.text)

    def AnimateGraphic(self):
        pass

Main=MainWindow()