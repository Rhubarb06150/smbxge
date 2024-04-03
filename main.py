from tkinter import messagebox,ttk
from PIL import Image,ImageTk
from tkinter import *
from threading import Thread
from idlelib.tooltip import Hovertip
from datetime import datetime
from random import randint
import PIL.Image
import platform
import os.path
import easygui
import urllib.request
import bs4
import cv2
import re
import time as tm


class MainWindow:
    
    def __init__(self):
        #HEAD_____________________________________________________________________________________
        self.version=0.11
        self.root=Tk()
        self.root.geometry('680x480')
        self.root.minsize(680,480)
        self.root.title(f'SMBX Graphic Editor ({self.version})')
        self.root.iconphoto(True,PhotoImage(file='assets/icon.png'))
        self.title_label=Label(text='SMBX Graphic Editor by Rhubarb06150').place(x=2,y=2)

        #DEFAULT WIDGETS _________________________________________________________________________

        self.level_path=None
        self.custom_graphic_choosen=None
        self.level_path_button=Button(text='Choose level folder',command= lambda: self.ChooselevelPath(),height=1)
        self.level_path_button.place(x=570,y=0)
        self.open_level_path=Button(text='Open level folder',command= lambda: self.OpenLevelPath(),height=1,state='disabled')
        self.open_level_path.place(x=570,y=26)
        self.gte=Label(self.root,text='Graphic you want to edit:').place(x=25,y=50)
        self.graphic_type=ttk.Combobox(self.root,values=['block-','effect-','npc-','background-','background2-'],width=13)
        self.graphic_type.set('block-')
        self.graphic_type.place(x=18,y=74)
        self.graphic_num=Entry(self.root,width=7)
        self.graphic_num.place(x=120,y=75)
        self.graphic_num.insert(0,"1")
        self.graphic_select_button=Button(text='Select custom graphic',command= lambda: self.SelectCustomGraphic(),state='disabled')
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
        self.upscale=ttk.Combobox(self.root,values=['x0.5','x1','x2','x3','x4'],width=4,state='disabled')
        self.upscale.place(x=250,y=46)
        self.upscale.set('x1')
        self.open_level_in_te=Button(self.root,text='Open level in text editor',command=lambda :self.OpenLevelInTextEditor(),state='disabled')
        self.open_level_in_te.place(x=450,y=80)
        # self.settings_button=Button(self.root,text='Open settings',command=lambda :SettingsWindow(self))
        # self.settings_button.place(x=50,y=50)

        #IMAGES __________________________________________________________________________________
        
        self.arrow=Label(self.root,image=ImageTk.PhotoImage(file='assets/arrow.png'),borderwidth=0)
        self.arrow.place(x=82,y=100)
        self.arrow.im=ImageTk.PhotoImage(file='assets/no-img.png')

        self.custom_graphic=Label(self.root,image=ImageTk.PhotoImage(file='assets/arrow.png'),borderwidth=0)
        self.custom_graphic.place(x=82,y=100)

        self.graphic_img=Label(self.root,borderwidth=0)
        self.graphic_img.place(x=50,y=100)

        #BINDS ___________________________________________________________________________________

        self.root.bind('<Configure>', lambda event:self.PlaceAll())
        self.root.bind('<Return>', lambda event:self.ShowCurrentGraphic())
        self.root.bind('<Control-S>', lambda event:self.SaveGraphic())
        self.root.bind('<Control-s>', lambda event:self.SaveGraphic())
        self.root.bind('<Control-D>', lambda event:self.GetDimension())
        self.root.bind('<Control-d>', lambda event:self.GetDimension())
        self.root.bind('<Up>', lambda event:self.Scroll('up'))
        self.root.bind('<Down>', lambda event:self.Scroll('down'))
        self.graphic_type.bind('<ComboboxSelected>',self.ShowCurrentGraphic())
        if platform.system()=='Windows':
            self.graphics_frame.bind('<MouseWheel>',self.MouseWheel)
        self.upscale.bind('<<ComboboxSelected>>',lambda event:self.ShowCurrentGraphic())

        #LIST IMAGES _____________________________________________________________________________
        
        self.lisframe0=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe1=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe2=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe3=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe4=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe5=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe6=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisframe7=Frame(master=self.graphics_frame,height=34,width=200,borderwidth=1,relief='sunken')
        self.lisimg0=Label(self.lisframe0,borderwidth=0)
        self.lisimg1=Label(self.lisframe1,borderwidth=0)
        self.lisimg2=Label(self.lisframe2,borderwidth=0)
        self.lisimg3=Label(self.lisframe3,borderwidth=0)
        self.lisimg4=Label(self.lisframe4,borderwidth=0)
        self.lisimg5=Label(self.lisframe5,borderwidth=0)
        self.lisimg6=Label(self.lisframe6,borderwidth=0)
        self.lisimg7=Label(self.lisframe7,borderwidth=0)
        self.textlabel0=Label(self.lisframe0,borderwidth=0)
        self.textlabel1=Label(self.lisframe1,borderwidth=0)
        self.textlabel2=Label(self.lisframe2,borderwidth=0)
        self.textlabel3=Label(self.lisframe3,borderwidth=0)
        self.textlabel4=Label(self.lisframe4,borderwidth=0)
        self.textlabel5=Label(self.lisframe5,borderwidth=0)
        self.textlabel6=Label(self.lisframe6,borderwidth=0)
        self.textlabel7=Label(self.lisframe7,borderwidth=0)
        self.rm_button0=Button(self.lisframe0,text='  -  ',command= lambda :self.RMGraphic(0))
        self.rm_button1=Button(self.lisframe1,text='  -  ',command= lambda :self.RMGraphic(1))
        self.rm_button2=Button(self.lisframe2,text='  -  ',command= lambda :self.RMGraphic(2))
        self.rm_button3=Button(self.lisframe3,text='  -  ',command= lambda :self.RMGraphic(3))
        self.rm_button4=Button(self.lisframe4,text='  -  ',command= lambda :self.RMGraphic(4))
        self.rm_button5=Button(self.lisframe5,text='  -  ',command= lambda :self.RMGraphic(5))
        self.rm_button6=Button(self.lisframe6,text='  -  ',command= lambda :self.RMGraphic(6))
        self.rm_button7=Button(self.lisframe7,text='  -  ',command= lambda :self.RMGraphic(7))
        self.BindAllImgs()
        
        self.lis_graphics=[self.lisframe0,self.lisframe1,self.lisframe2,self.lisframe3,self.lisframe4,self.lisframe5,self.lisframe6,self.lisframe7]
        self.lis_frames=[self.lisframe0,self.lisframe1,self.lisframe2,self.lisframe3,self.lisframe4,self.lisframe5,self.lisframe6,self.lisframe7]

        #ANIMATION _______________________________________________________________________________

        self.framerate=Entry(self.root,width=5)
        self.framerate.place(x=496,y=20)
        self.framerate_label=Label(self.root,text='Framespeed (t/s):')
        self.framerate_label.place(x=396,y=20)

        self.anim_width=Entry(self.root,width=5)
        self.anim_width.place(x=466,y=40)
        self.anim_width_label=Label(self.root,text='Width (px):')
        self.anim_width_label.place(x=396,y=40)

        self.anim_height=Entry(self.root,width=5)
        self.anim_height.place(x=466,y=60)
        self.anim_height_label=Label(self.root,text='Height (px):')
        self.anim_height_label.place(x=396,y=60)

        self.frames_nb=Entry(self.root,width=5)
        self.frames_nb.place(x=446,y=80)
        self.frames_nb_label=Label(self.root,text='Frames:')
        self.frames_nb_label.place(x=396,y=80)

        self.animated=BooleanVar()
        self.animated_checkbox=Checkbutton(self.root,text='Animated?',onvalue=True,offvalue=False,var=self.animated,command=self.ShowAnimationMenu)
        self.animated_checkbox.place(x=306,y=68)
        self.animated.set(False)

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
        self.open_level_in_te.place(x=self.root.winfo_width()-136,y=52)

    def RMGraphic(self,index):
        self.matches = ["block-", "effect-", "npc-", "background-", "background2-"]
        self.filelist=os.listdir(self.level_path)
        for fichier in self.filelist[:]:
            if not(fichier.endswith(".png")) or not any(x in fichier for x in self.matches):
                self.filelist.remove(fichier)
        msg=messagebox.askyesno(title='Warning',message=f'Are you sure you want to delete {self.filelist[index+self.scroll_index]}?\nThis is irreversible!!!')
        if msg:
            os.remove(self.level_path+'\\'+self.filelist[index+self.scroll_index].replace('.png','')+'.png')
            try:
                    #CHECK IF LEVEL IS SMBX 1
                    open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl')
                    if 'block-' in self.filelist[index+self.scroll_index]:
                        self.ind=f'CB|{self.graphic_num.get()}'
                    elif 'background-' in self.filelist[index+self.scroll_index]:
                        self.ind=f'CT|{self.graphic_num.get()}'
                    elif 'effect-' in self.filelist[index+self.scroll_index]:
                        self.ind=f'CE|{self.graphic_num.get()}'

                    #DELETE IF ANIMATION TAG ALREADY IN .LVL FILE - YEAH I TOTALLY COPY PASTED MY OWN CODE FROM BELOW
                    with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','r') as f:
                        lines = f.readlines()
                    with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','w') as f:
                        for line in lines:
                            if self.ind not in line.strip("\n"):
                                f.write(line)
                    try:
                        os.remove(self.level_path+'\\'+self.filelist[index+self.scroll_index].replace('.png','')+'.txt')
                    except:
                        pass

            except:
                try:
                    open(self.GoParentFolder(self.level_path)+self.level_name+'.lvlx')
                    try:
                        os.remove(self.level_path+'\\'+self.filelist[index+self.scroll_index].replace('.png','')+'.txt')
                    except:
                        pass
                except:
                    msg=messagebox.showerror(title='Error',message="The level file can't be found!")
            self.LoadCustomGraphics()

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
            if self.len_graphics>8:
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
        self.upscale.configure(state="readonly")
        self.graphic_type.set(self.RMInt(graphic))
        self.upscale.set('x1')
        self.animated.set(False)

        if self.GetVersion()==1:

            if self.graphic_type.get()!='npc-':

                if self.graphic_type.get()=='block-':
                    self.ind=f'CB|{self.graphic_num.get()}'
                elif self.graphic_type.get()=='background-':
                    self.ind=f'CT|{self.graphic_num.get()}'
                elif self.graphic_type.get()=='effect-':
                    self.ind=f'CE|{self.graphic_num.get()}'
                ln=None
                with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','r') as f:
                    lines = f.readlines()
                for line in lines:
                    if self.ind in line:
                        ln=line
                        break
                if ln!=None:
                    ln=ln.replace(self.ind+'|','')
                    res=ln.split(',')
                    for tag in res:
                        tag=str(tag).replace('\n','')
                    res=tuple(res)
                    h,w,c=cv2.imread(self.initial_block).shape
                    if '0001' not in tag:
                        self.anim_width.delete(0,END)
                        self.anim_width.insert(0,w)
                    if '0002' not in tag:
                        self.anim_height.delete(0,END)
                    if '0004' not in tag:
                        self.framerate.delete(0,END)
                        self.framerate.insert(0,8)
                    for tag in res:
                        if re.match('^0001',tag):
                            self.anim_width.delete(0,END)
                            self.anim_width.insert(0,tag.replace('0001',''))
                        elif re.match('^0002',tag):
                            self.anim_height.delete(0,END)
                            self.anim_height.insert(0,tag.replace('0002',''))
                        elif re.match('^0003',tag):
                            self.animated.set(True)
                            self.frames_nb.delete(0,END)
                            self.frames_nb.insert(0,tag.replace('0003',''))
                        elif re.match('^0004',tag):
                            self.animated.set(True)
                            self.framerate.delete(0,END)
                            self.framerate.insert(0,tag.replace('0004',''))
            try:
                lines=open(self.level_path+'\\'+self.graphic_type.get()+self.graphic_num.get()+'.txt').readlines()
                for line in lines:
                    if 'gfxwidth=' in line:
                        self.anim_width.delete(0,END)
                        self.anim_width.insert(0,line.replace('gfxwidth=','').replace('\n',''))
                    if 'gfxheight=' in line:
                        self.anim_height.delete(0,END)
                        self.anim_height.insert(0,line.replace('gfxheight=','').replace('\n',''))
                    if 'frames=' in line:
                        self.frames_nb.delete(0,END)
                        self.frames_nb.insert(0,line.replace('frames=','').replace('\n',''))
                        self.animated.set(True)
                    if 'framespeed=' in line:
                        self.framerate.delete(0,END)
                        self.framerate.insert(0,line.replace('framespeed=','').replace('\n',''))
                        self.animated.set(True)
            except:
                pass
        else:
            pass

        self.root.title(f'SMBX Graphic Editor ({self.version}) - level: {self.level_name} - graphic: {graphic} (SMBX {self.GetVersion()})')
        self.ShowCurrentGraphic()
        self.ShowAnimationMenu()


    def OpenLevelPath(self):

        if self.level_path!=None:
            os.startfile(self.level_path)
        else:
            msg=messagebox.showerror(title='Error',message='You need to select a level folder first to open it.\nhuh')

    def ClearGraphicName(self,text):
        text=text.replace('block-','').replace('effect-','').replace('npc-','').replace('background-','').replace('background2-','').replace('.png','')
        return text

    def LoadCustomGraphics(self):
        self.matches = ["block-", "effect-", "npc-", "background-", "background2-"]
        self.filelist=os.listdir(self.level_path)
        for fichier in self.filelist[:]:
            if not(fichier.endswith(".png")) or not any(x in fichier for x in self.matches):
                self.filelist.remove(fichier)
                
        self.len_graphics=len(self.filelist)
        self.y=0
        self.i=0
        self.lis_graphics=[]
        self.img_list=[]
        try:
            for frame in self.frames_list:
                frame.place_forget()
        except:
            pass
        self.frames_list=[]

        for j in range(8):
            
            try:

                self.lis_graphics.append(self.filelist[j+self.scroll_index])
                img=ImageTk.PhotoImage(PIL.Image.open(self.level_path+'\\'+self.filelist[j+self.scroll_index]).crop((0,0,32,32)))
                exec(f'self.lisimg{self.i}.configure(image=img)')
                exec(f'self.img_list.append([self.lisimg{self.i},self.filelist[j+self.scroll_index]])')
                exec(f'self.lisimg{self.i}.im=img')
                exec(f'self.lisimg{self.i}.place(x=0,y=0)')
                exec(f'self.lisimg{self.i}.bind("<MouseWheel>",self.MouseWheel)')

                exec(f'self.textlabel{self.i}.configure(text=self.filelist[j+self.scroll_index])')
                exec(f'self.textlabel{self.i}.place(x=40,y=6)')
                exec(f'self.textlabel{self.i}.bind("<MouseWheel>",self.MouseWheel)')

                exec(f'self.lisframe{self.i}.place(x=0,y=self.y)')
                exec(f'self.rm_button{self.i}.place(x=170,y=3)')

                exec(f'self.lisframe{self.i}.bind("<MouseWheel>",self.MouseWheel)')
                exec(f'self.frames_list.append(self.lisframe{self.i})')
                self.y+=32
                self.i+=1

            except Exception as e:
                break

# ANIMATION FUNCTIONS ___________________________________________________________________________________________________________________
        
    def ShowAnimationMenu(self):
        if self.animated.get():
            self.framerate.place(x=496,y=20)
            self.framerate_label.place(x=396,y=20)
            self.anim_width.place(x=466,y=40)
            self.anim_width_label.place(x=396,y=40)
            self.anim_height.place(x=466,y=60)
            self.anim_height_label.place(x=396,y=60)
            self.frames_nb.place(x=446,y=80)
            self.frames_nb_label.place(x=396,y=80)
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

    def AnimationToggle(self):
        self.animation_running = not self.animation_running
        if self.animation_running:
            try:
                int(self.framerate.get())
                int(self.frames_nb.get())
                int(self.anim_height.get())
                int(self.anim_width.get())
                self.animation_button.configure(text='Stop animation')
                self.thread=Thread(target=self.AnimationLoop)
                self.thread.start()
            except:
                self.animation_running=False
                msg=messagebox.showerror(title='Error',message='One or multiple animations fields is incorrect, please correct it.')

    def AnimationLoop(self):

        self.cur_frame=0
        self.index=0
        self.anim_height.configure(state='disabled')
        self.anim_width.configure(state='disabled')
        self.framerate.configure(state='disabled')
        self.frames_nb.configure(state='disabled')
        while True:
            h,w,c=cv2.imread(self.custom_graphic_choosen).shape
            self.img=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen).resize((int(w*float(self.upscale.get().replace('x',''))),int(h*float(self.upscale.get().replace('x','')))),PIL.Image.NEAREST).crop((0,int(self.cur_frame)*int(self.anim_height.get()),int(self.anim_width.get()),int(self.cur_frame)*int(self.anim_height.get())+int(self.anim_height.get()))))
            self.custom_graphic.configure(image=self.img)
            self.custom_graphic.im=self.img
            self.index+=1
            if self.index%(1/int(self.framerate.get()))<=0:
                self.cur_frame+=1
            if self.cur_frame>=int(self.frames_nb.get()):
                self.cur_frame=0
            tm.sleep(1/(int(self.framerate.get()))) 
            if not self.animation_running:
                self.img=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen).resize((int(w*float(self.upscale.get().replace('x',''))),int(h*float(self.upscale.get().replace('x','')))),PIL.Image.NEAREST))
                self.custom_graphic.configure(image=self.img)
                self.custom_graphic.im=self.img
                self.animation_button.configure(text='Start animation')
                self.anim_height.configure(state='normal')
                self.anim_width.configure(state='normal')
                self.framerate.configure(state='normal')
                self.frames_nb.configure(state='normal')
                break

# GUI GRAPHICS FUNCTIONS ___________________________________________________________________________________________________________________


    def SelectCustomGraphic(self):
        self.path=easygui.fileopenbox(title='Choose your custom graphic',filetypes=[['*.png','*.jpg','*.jpeg','Images only']])
        if self.path!=None:
            self.custom_graphic_choosen=self.path
            self.animated_checkbox.configure(state="normal")
            self.upscale.configure(state="readonly")    
        self.ShowCurrentGraphic()

    def ShowCurrentGraphic(self):

        self.path=f'smbxdata\\{self.graphic_type.get().replace("-","")}\\{self.graphic_type.get()}{self.graphic_num.get()}.png'
        self.initial_block=self.path

        try:
            if self.graphic_type.get()=='background2-':
                self.h_,self.w_,self.c_=cv2.imread(self.path).shape
                img=ImageTk.PhotoImage(PIL.Image.open(self.path).crop((0,self.h_-256,128,self.h_)))
                if self.custom_graphic_choosen!=None:
                    self.h_,self.w_,self.c_=cv2.imread(self.custom_graphic_choosen).shape
                    self.img_=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen).crop((0,self.h_-256,128,self.h_)))
            else:
                self.img=ImageTk.PhotoImage(PIL.Image.open(self.path))
            self.h,self.w,self.c=cv2.imread(self.path).shape
        except Exception as e:
            self.img=ImageTk.PhotoImage(file='assets/no-img.png')
            self.h,self.w=32,32

        self.graphic_img.configure(image=self.img)
        self.graphic_img.im=self.img

        self.arrow_im=ImageTk.PhotoImage(file='assets/arrow.png')
        self.arrow.configure(image=self.arrow_im)
        self.arrow.im=self.arrow_im

        self.arrow.place_forget()

        if self.custom_graphic_choosen!=None:
            h,w,c=cv2.imread(self.custom_graphic_choosen).shape
            self.img=ImageTk.PhotoImage(PIL.Image.open(self.custom_graphic_choosen).resize((int(w*float(self.upscale.get().replace('x',''))),int(h*float(self.upscale.get().replace('x','')))),PIL.Image.NEAREST))
            self.custom_graphic.configure(image=self.img)
            self.custom_graphic.im=self.img
            self.custom_graphic.place(x=90+self.w,y=100)
            self.arrow.place(x=54+self.w,y=100)

        self.tip=Hovertip(self.custom_graphic,f'Dimensions:\nWidth: {self.w}px\nHeight: {self.h}px',500)
        self.graphics_frame.lift()

# TEXT FORMATING FUCNTIONS __________________________________________________________________________________________________________________

    def RMInt(self,text):
        text=text.replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('.png','')
        return text
    
    def GoParentFolder(self,path):
        self.res=path
        while True:
            self.res=self.res[:-1]
            if self.res[-1]=='/' or self.res[-1]=='\\':
                break
        return self.res
    
# OTHER ______________________________________________________________________________________________________________________________________
    
    def CompareSize(self):
        h,w,c=cv2.imread(f'smbxdata\\{self.graphic_type.get().replace("-","")}\\{self.graphic_type.get()}{self.graphic_num.get()}.png').shape
        h_,w_,c=cv2.imread(self.custom_graphic_choosen).shape
        if h==h_ and w==w_:
            print('same size')
            return True
        else:
            print('not same size')
            return False
    
    def GetVersion(self):
        try:
            open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl')
            return 1
        except:
            try:
                open(self.GoParentFolder(self.level_path)+self.level_name+'.lvlx')
                return 2
            except:
                return None
            
    def OpenLevelInTextEditor(self):
        print(self.GetVersion())
        if self.GetVersion()==1:

            try:
                thread=Thread(target= lambda:os.system('notepad '+str(self.GoParentFolder(self.level_path)+self.level_name+'.lvl')))
                thread.start()
            except:
                msg=messagebox.showerror(title='Error',message=f"Can't open the file {self.level_name}.lvl") 
    def GetDimension(self):
        h,w,c=cv2.imread(f'smbxdata\\{self.graphic_type.get().replace("-","")}\\{self.graphic_type.get()}{self.graphic_num.get()}.png').shape
        message=f'Dimensions:               \n\n{self.graphic_type.get()}{self.graphic_num.get()}:\n  Width: {w}px\n  Height:{h}px'
        if self.custom_graphic_choosen!=None:
            h,w,c=cv2.imread(self.custom_graphic_choosen).shape
            message+=f'\n\n{os.path.basename(self.custom_graphic_choosen)}: (without upscaling)\n  Width:{w}px\n  Height:{h}px\n\nDimensions (with upscaling)\n  Width:{int(w*float(self.upscale.get().replace("x","")))}px\n  Height:{int(h*float(self.upscale.get().replace("x","")))}px'
        msg=messagebox.showinfo(title='Dimensions',message=message)

    def SaveGraphic(self):

        if self.level_path==None:
            msg=messagebox.showerror(title='Error',message='Please choose an level folder first')
        else:
            h,w,c=cv2.imread(self.custom_graphic_choosen).shape
            PIL.Image.open(self.custom_graphic_choosen).resize((int(w*float(self.upscale.get().replace('x',''))),int(h*float(self.upscale.get().replace('x','')))),PIL.Image.NEAREST).save(f'{self.level_path}\\{self.graphic_type.get()}{self.graphic_num.get()}.png')
            if self.animated.get():

                if self.GetVersion()==1:
                    if self.graphic_type.get()=='npc-':
                        self.file=open(f'{(self.level_path)}\\{self.graphic_type.get()}{self.graphic_num.get()}.txt','w+')
                        self.file.write(f'gfxwidth={self.anim_width.get()}\ngfxheight={self.anim_height.get()}\nframes={self.frames_nb.get()}\nframespeed={self.framerate.get()}')
                        self.file.close()
                    else:

                        if self.graphic_type.get()=='block-':
                            self.ind=f'CB|{self.graphic_num.get()}'
                        elif self.graphic_type.get()=='background-':
                            self.ind=f'CT|{self.graphic_num.get()}'
                        elif self.graphic_type.get()=='effect-':
                            self.ind=f'CE|{self.graphic_num.get()}'

                        #DELETE IF ANIMATION TAG ALREADY IN .LVL FILE
                        with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','r') as f:
                            lines = f.readlines()
                        found=False
                        with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','w') as f:
                            for line in lines:
                                if self.ind not in line.strip("\n"):
                                    f.write(line)
                                else:
                                    found=True
                                    print('r1')
                                    f.write(f'{self.ind}|0001{self.anim_width.get()},0002{self.anim_height.get()},0003{self.frames_nb.get()},0004{self.framerate.get()}')
                        if not found:
                            print('r2')
                            self.file=open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','a+')
                            open('e.txt','w+').write('aaa'+self.frames_nb.get()+'aaa')
                            self.file.write(f'\n{self.ind}|0001{self.anim_width.get()},0002{self.anim_height.get()},0003{self.frames_nb.get()},0004{self.framerate.get()}')
                            self.file.close()
                        
                elif self.GetVersion()==2:
                    #IF NOT SMBX 1 SO IS SMBX 2     
                    open(self.GoParentFolder(self.level_path)+self.level_name+'.lvlx')
                    self.file=open(f'{(self.level_path)}\\{self.graphic_type.get()}{self.graphic_num.get()}.txt','w+')
                    self.file.write(f'gfxwidth={self.anim_width.get()}\ngfxheight={self.anim_height.get()}\nframes={self.frames_nb.get()}\nframespeed={self.framerate.get()}')
                    self.file.close()
                else:
                    msg=messagebox.showerror(title='Error',message="The level file cant be found!")

            else:

                if self.GetVersion()==1:
                    if self.graphic_type.get()!='npc-':
                        if self.graphic_type.get()=='block-':
                            self.ind=f'CB|{self.graphic_num.get()}'
                        elif self.graphic_type.get()=='background-':
                            self.ind=f'CT|{self.graphic_num.get()}'
                        elif self.graphic_type.get()=='effect-':
                            self.ind=f'CE|{self.graphic_num.get()}'
                        with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','r') as f:
                            lines = f.readlines()
                        found=False
                        with open(self.GoParentFolder(self.level_path)+self.level_name+'.lvl','w') as f:    
                            for line in lines:
                                if self.ind not in line.strip("\n"):
                                    f.write(line)
                                else:
                                    found=True
                                    if self.CompareSize()==False:
                                        h,w,c=cv2.imread(self.custom_graphic_choosen).shape
                            if not found:
                                if self.CompareSize()==False:
                                    h,w,c=cv2.imread(self.custom_graphic_choosen).shape
                    else:
                        try:
                            os.remove(f'{self.GoParentFolder(self.level_path)}\\{self.graphic_type.get()}{self.graphic_num.get()}.txt')
                        except:
                            pass
                elif self.GetVersion()==2:
                    open(self.GoParentFolder(self.level_path)+self.level_name+'.lvlx')
                    try:
                        os.remove(f'{self.GoParentFolder(self.level_path)}\\{self.graphic_type.get()}{self.graphic_num.get()}.txt')
                    except:
                        pass
                else:
                    msg=messagebox.showerror(title='Error',message="The level file cant be found!")
            self.LoadCustomGraphics()

    def ChooselevelPath(self):
        
        path=easygui.diropenbox(title='Choose your level folder')
        if path!=None:
            self.level_path=path
            self.level_name=os.path.basename(self.level_path)
            self.root.title(f'SMBX Graphic Editor ({self.version}) - level: {self.level_name} (SMBX {self.GetVersion()})')
            self.scroll_down_button.configure(state='normal')
            self.scroll_up_button.configure(state='normal')
            self.open_level_in_te.configure(state="normal")
            self.open_level_path.configure(state="normal")
            self.graphic_select_button.configure(state="normal")
            for frame in self.lis_frames:
                frame.place_forget()
            self.LoadCustomGraphics()
            now = datetime.now()
            today = datetime.today()
            d1 = today.strftime("%Y_%m_%d")
            current_time = now.strftime("%H_%M_%S")
            try:
                file=open(self.GoParentFolder(self.level_path)+'\\'+self.level_name+'.lvl','r')
                file2=open('backups\\'+self.level_name+d1+'_'+current_time+'.lvl','w+')
                for line in file.readlines():
                    file2.write(line)
            except Exception as e:
                try:
                    file=open(self.GoParentFolder(self.level_path)+'\\'+self.level_name+'.lvlx','r')
                    file2=open('backups\\'+self.level_name+d1+'_'+current_time+'.lvlx','w+')
                    for line in file.readlines():
                        file2.write(line)
                except:
                    msg=messagebox.showerror(title='Error',message='Backup of this level in impossible, considering this software is still unstable\nconsider not use it please.')

    def GetLastVersion(self):

        content=urllib.request.urlopen('https://mcrhubarb.net/softwares/index.html')
        content=bs4.BeautifulSoup(content, 'html.parser')
        verspan = content.find(id='smbxgever')
        self.last_ver=verspan=float(verspan.text)

class SettingsWindow:

    def __init__(self,root):
        self.master=root
        self.root=Toplevel(self.master.root)
        self.root.geometry('480x480')
        self.root.title(f'SMBX Graphic Editor ({self.master.version}) Settings')
        self.root.resizable(False,False)
        self.root.mainloop()

Main=MainWindow()