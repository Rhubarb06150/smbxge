from tkinter import messagebox,ttk
from PIL import Image,ImageTk
from tkinter import *
from threading import Thread
import PIL.Image
import platform
import os.path
import easygui
import urllib.request
import bs4
import cv2
import time as tm

class MainWindow:
    
    def __init__(self):
        #HEAD_____________________________________________________________________________________
        self.version=0.1
        self.root=Tk()
        self.root.geometry('680x480')
        self.root.title(f'SMBX 1/2 Graphic Editor ({self.version})')
        self.root.iconphoto(True,PhotoImage(file='assets/icon.png'))
        self.title_label=Label(text='SMBX Graphic Editor by Rhubarb06150').place(x=2,y=2)

        #DEFAULT WIDGETS _________________________________________________________________________

        self.level_path=None
        self.custom_graphic_choosen=None
        self.level_path_button=Button(text='Choose level folder',command= lambda: self.ChooselevelPath(),height=1)
        self.level_path_button.place(x=570,y=0)
        self.open_level_path=Button(text='Open level folder',command= lambda: self.OpenLevelPath(),height=1)
        self.open_level_path.place(x=570,y=26)
        self.gte=Label(self.root,text='Graphic you want to edit:').place(x=25,y=50)
        self.graphic_type=ttk.Combobox(self.root,values=['block-','effect-','npc-','background-','background2-'],width=13)
        self.graphic_type.set('block-')
        self.graphic_type.place(x=18,y=74)
        self.graphic_num=Entry(self.root,width=7)
        self.graphic_num.place(x=120,y=75)
        self.graphic_num.insert(0,"1")
        self.graphic_select_button=Button(text='Select custom graphic',command= lambda: self.SelectCustomGraphic())
        self.graphic_select_button.place(x=170,y=70)

        self.graphics_frame=Frame(self.root,height=264,width=200,borderwidth=1,relief='sunken')
        self.graphics_frame.place(x=480,y=216)
        self.scroll_index=0
        self.scroll_up_button=Button(text='  ^  ',command= lambda :self.Scroll('up'),state='disabled')
        self.scroll_down_button=Button(text='  v  ',command= lambda :self.Scroll('down'),state='disabled')
        self.scroll_up_button.place(x=480,y=194)
        self.scroll_down_button.place(x=510,y=194)
        self.animation_button=Button(self.root,text="Start animation",command=self.AnimationToggle,state='disabled')
        self.animation_button.place(x=300,y=40)
        self.animation_running=False

        #IMAGES __________________________________________________________________________________
        
        self.arrow=Label(self.root,image=ImageTk.PhotoImage(file='assets/arrow.png'),borderwidth=0)
        self.arrow.place(x=82,y=100)
        self.arrow.im=ImageTk.PhotoImage(file='assets/no-img.png')

        self.custom_graphic=Label(self.root,image=ImageTk.PhotoImage(file='assets/arrow.png'),borderwidth=0)
        self.custom_graphic.place(x=82,y=100)

        self.img=Label(self.root,borderwidth=0)
        self.img.place(x=50,y=100)

        #BINDS ___________________________________________________________________________________

        self.root.bind('<Configure>', lambda event:self.PlaceAll())
        self.root.bind('<Return>', lambda event:self.ShowCurrentGraphic())
        self.root.bind('<space>', lambda event:self.Animate())
        self.root.bind('<E>', lambda event:self.LoadCustomGraphics())
        self.root.bind('<Control-S>', lambda event:self.SaveGraphic())
        self.root.bind('<Control-s>', lambda event:self.SaveGraphic())
        self.root.bind('<Up>', lambda event:self.Scroll('up'))
        self.root.bind('<Down>', lambda event:self.Scroll('down'))
        if platform.system()=='Windows':
            self.graphics_frame.bind('<MouseWheel>',self.MouseWheel)

        #LIST IMAGES _____________________________________________________________________________
        
        self.lisframe0=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe1=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe2=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe3=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe4=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe5=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe6=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe7=Frame(self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisimg0=Label(self.lisframe0,borderwidth=0)
        self.lisimg1=Label(self.lisframe1,borderwidth=0)
        self.lisimg2=Label(self.lisframe2,borderwidth=0)
        self.lisimg3=Label(self.lisframe3,borderwidth=0)
        self.lisimg4=Label(self.lisframe4,borderwidth=0)
        self.lisimg5=Label(self.lisframe5,borderwidth=0)
        self.lisimg6=Label(self.lisframe6,borderwidth=0)
        self.lisimg7=Label(self.lisframe7,borderwidth=0)
        self.lisframes=[]
        
        self.lis_graphics=[self.lisframe0,self.lisframe1,self.lisframe2,self.lisframe3,self.lisframe4,self.lisframe5,self.lisframe6,self.lisframe7]

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

        self.animated_checkbox.configure(state="disabled")
        self.ShowAnimationMenu()
        self.root.mainloop()

    def MouseWheel(self,event):
        if int(-1*(event.delta/120))==-1:
            self.Scroll('up')
        elif int(-1*(event.delta/120))==1:
            self.Scroll('down')

    def PlaceAll(self):
        self.graphics_frame.place(x=(self.root.winfo_width()-200),y=(self.root.winfo_height()-264))
        self.scroll_up_button.place(x=self.root.winfo_width()-200,y=(self.root.winfo_height()-290))
        self.scroll_down_button.place(x=self.root.winfo_width()-170,y=(self.root.winfo_height()-290))
        self.level_path_button.place(x=self.root.winfo_width()-110,y=0)
        self.open_level_path.place(x=self.root.winfo_width()-110,y=26)

    def BindAllImgs(self):

        self.lisimg0.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[0]))
        self.lisimg1.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[1]))
        self.lisimg2.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[2]))
        self.lisimg3.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[3]))
        self.lisimg4.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[4]))
        self.lisimg5.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[5]))
        self.lisimg6.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[6]))
        self.lisimg7.bind('<Button-1>',lambda event: self.LoadGraphic(self.lis_graphics[7]))

    def Scroll(self,direction):

        if self.level_path!=None:
            if direction=='down':
                self.scroll_index+=1
            else:
                self.scroll_index-=1
            if self.scroll_index<0:
                self.scroll_index=0
            if self.len_graphics-8-self.scroll_index<0:
                self.scroll_index=self.len_graphics-8
            self.LoadCustomGraphics()

    def LoadGraphic(self,graphic):

        self.graphic_num.delete(0,END)
        self.graphic_num.insert(0,self.ClearGraphicName(graphic))
        self.custom_graphic_choosen=self.level_path+'\\'+graphic
        self.animated_checkbox.configure(state="normal")
        self.graphic_type.set(self.RMInt(graphic))
        self.ShowCurrentGraphic()

    def OpenLevelPath(self):
        if self.level_path!=None:
            os.startfile(self.level_path)
        else:
            msg=messagebox.showerror(title='Error',message='You need to select a level folder first to open it.\nhuh')

    def ClearGraphicName(self,text):
        text=text.replace('block-','').replace('effect-','').replace('npc-','').replace('background-','').replace('background2-','').replace('.png','')
        return text

    def LoadCustomGraphics(self):
        matches = ["block-", "effect-", "npc-", "background-", "background2-"]
        filelist=os.listdir(self.level_path)
        for fichier in filelist[:]:
            if not(fichier.endswith(".png")) or not any(x in fichier for x in matches):
                filelist.remove(fichier)
        self.len_graphics=len(filelist)
        y=0
        i=0
        self.lis_graphics=[]
        img_list=[]

        for j in range(8):
            
            try:

                self.lis_graphics.append(filelist[j+self.scroll_index])
                img=ImageTk.PhotoImage(PIL.Image.open(self.level_path+'\\'+filelist[j+self.scroll_index]).crop((0,0,32,32)))
                exec(f'self.lisimg{i}.configure(image=img)')
                exec(f'img_list.append([self.lisimg{i},filelist[j+self.scroll_index]])')
                exec(f'self.lisimg{i}.im=img')
                exec(f'self.lisimg{i}.place(x=0,y=0)')
                exec(f'self.lisimg{i}.bind("<MouseWheel>",self.MouseWheel)')

                exec(f'text=Label(self.lisframe{i},text=filelist[j+self.scroll_index]+"               ")')
                exec('text.place(x=40,y=6)')
                exec('text.bind("<MouseWheel>",self.MouseWheel)')

                exec(f'self.lisframe{i}.place(x=0,y=y)')
                exec(f'self.lisframe{i}.bind("<MouseWheel>",self.MouseWheel)')
                y+=32
                i+=1

            except:
                break
        self.BindAllImgs()
        
    def ShowAnimationMenu(self):

        if self.animated.get():
            self.framerate.place(x=490,y=70)
            self.framerate_label.place(x=390,y=70)
            self.framerate.insert(0,'8')
            self.anim_width.place(x=460,y=90)
            self.anim_width_label.place(x=390,y=90)
            self.anim_width.insert(0,'32')
            self.anim_height.place(x=460,y=110)
            self.anim_height_label.place(x=390,y=110)
            self.anim_height.insert(0,'32')
            self.frames_nb.place(x=440,y=130)
            self.frames_nb_label.place(x=390,y=130)
            self.frames_nb.insert(0,'4')
            self.animation_button.configure(state='normal')

        else:
            self.framerate_label.place_forget()
            self.framerate.place_forget()
            self.anim_width.place_forget()
            self.anim_width_label.place_forget()
            self.anim_height.place_forget()
            self.anim_height_label.place_forget()
            self.frames_nb.place_forget()
            self.frames_nb_label.place_forget()
            self.animation_button.configure(state='disabled')

    def SelectCustomGraphic(self):
        path=easygui.fileopenbox(title='Choose your custom graphic',filetypes=[['*.png','*.jpg','*.jpeg','Images only']])
        if path!=None:
            self.custom_graphic_choosen=path
            self.animated_checkbox.configure(state="normal")
        self.ShowCurrentGraphic()

    def RMInt(self,text):
        text=text.replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('.png','')
        return text

    def SaveGraphic(self):

        if self.level_path==None:
            msg=messagebox.showerror(title='Error',message='Please choose an level folder first')
        else:
            PIL.Image.open(self.custom_graphic_choosen).save(f'{self.level_path}\\{self.graphic_type.get()}{self.graphic_num.get()}.png')

    def AnimationToggle(self):
        self.animation_running = not self.animation_running
        if self.animation_running:
            self.animation_button.configure(text='Stop animation')
            thread=Thread(target=self.AnimationLoop)
            thread.start()

    def AnimationLoop(self):
        self.cur_frame=0
        self.index=0
        self.anim_height.configure(state='disabled')
        self.anim_width.configure(state='disabled')
        self.framerate.configure(state='disabled')
        self.frames_nb.configure(state='disabled')
        while True:
            img=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen).crop((0,int(self.cur_frame)*int(self.anim_height.get()),int(self.anim_width.get()),int(self.cur_frame)*int(self.anim_height.get())+int(self.anim_height.get()))))
            self.custom_graphic.configure(image=img)
            self.custom_graphic.im=img
            self.index+=1
            if self.index%(1/int(self.framerate.get()))<=0:
                self.cur_frame+=1
                print(self.cur_frame)
            if self.cur_frame>=int(self.frames_nb.get()):
                self.cur_frame=0
            tm.sleep(1/(int(self.framerate.get())))
            if not self.animation_running:
                img=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen))
                self.custom_graphic.configure(image=img)
                self.custom_graphic.im=img
                self.animation_button.configure(text='Start animation')
                self.anim_height.configure(state='normal')
                self.anim_width.configure(state='normal')
                self.framerate.configure(state='normal')
                self.frames_nb.configure(state='normal')
                break
        
    def ShowCurrentGraphic(self):

        path=f'smbxdata\\{self.graphic_type.get().replace("-","")}\\{self.graphic_type.get()}{self.graphic_num.get()}.png'

        try:
            if self.graphic_type.get()=='background2-':
                h_,w_,c_=cv2.imread(path).shape
                img=ImageTk.PhotoImage(PIL.Image.open(path).crop((0,h_-256,128,h_)))
            else:
                img=ImageTk.PhotoImage(PIL.Image.open(path))
            h,w,c=cv2.imread(path).shape
        except Exception as e:
            print(e)
            img=ImageTk.PhotoImage(file='assets/no-img.png')
            h,w=32,32

        self.img.configure(image=img)
        self.img.im=img

        arrow_im=ImageTk.PhotoImage(file='assets/arrow.png')
        self.arrow.configure(image=arrow_im)
        self.arrow.im=arrow_im

        self.arrow.place_forget()

        if self.custom_graphic_choosen!=None:
            img=ImageTk.PhotoImage(file=self.custom_graphic_choosen)
            self.custom_graphic.configure(image=img)
            self.custom_graphic.im=img
            self.custom_graphic.place(x=90+w,y=100)
            self.arrow.place(x=54+w,y=100)

        self.graphics_frame.lift()

    def ChooselevelPath(self):

        path=easygui.diropenbox(title='Choose your level folder')
        if path!=None:
            self.root.title(f'SMBX 1/2 Graphic Editor ({self.version}) => level: {os.path.basename(path)}')
            self.level_path=path
            self.scroll_down_button.configure(state='normal')
            self.scroll_up_button.configure(state='normal')
            self.LoadCustomGraphics()

    def GetLastVersion(self):

        content=urllib.request.urlopen('https://mcrhubarb.net/softwares/index.html')
        content=bs4.BeautifulSoup(content, 'html.parser')
        verspan = content.find(id='smbxgever')
        self.last_ver=verspan=float(verspan.text)

# class Animation:

#     def __init__(self,framespeed,frames,width,height,graphic):
#         self.framespeed=int(framespeed)
#         self.frames=int(frames)
#         self.width=int(width)
#         self.height=int(height)
#         self.index=0
#         self.cur_frame=0
#         self.frames_graphic=graphic
#         self.clock=time.Clock()

#     def Animate(self,win):
#         # self.screen.blit(self.frames_graphic,(0,0),(0,self.cur_frame*self.height,self.width,self.height))
        

Main=MainWindow()