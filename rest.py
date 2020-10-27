from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg 
from PIL import Image, ImageTk
from random import *
import pickle,random,os,time,datetime,subprocess


top_bg_color = 'gray5'
top_fg_colour = 'snow'
menu_board_color = 'gray10'
bill_board_color = 'gray80'
menu_color = 'gray10'
label_color = 'gray95'
label_fg_color = 'snow'
fg_color='snow'


dish_list = []
price = []
dict_menu = {}
logs = {}
select_dish = {}
remain_qty=[]
qty=[]
time_now = datetime.datetime.now().strftime("%H:%M:%S")
cont=0

with open("data/docs/menu.txt") as f:
    for line in f:
        (key, val,q) = line.split()
        dict_menu[(key)] = int(val)
        qty.append(int(q))
for key, values in dict_menu.items():
    dish_list.append(key)
    price.append(values)

if os.path.isfile('data/store.p'):
    f = open('data/store.p', 'rb')
    for i in range(1,len(qty)+1):
        globals()['total_qty%s'%i] = pickle.load(f)
    f.close()
else:
    for i in range(1,len(qty)+1):
            globals()['total_qty%s'%i] = int(qty[i-1])


if os.path.isfile('data/app_data.p'):
    f1 = open('data/app_data.p','rb')
    theme = pickle.load(f1)
    gst = pickle.load(f1)
    f1.close()
else:
    theme=1
    gst= 1.25

if os.path.isfile('data/name.p'):
    fx = open('data/name.p','rb')
    Res_name=pickle.load(fx)
    fx.close()
else:
    Res_name='RESTAURANT'

if os.path.isfile('data/pass.p'):
    f5 = open('data/pass.p', 'rb')
    listt=pickle.load(f5)
else: 
    listt=['root','toor']



class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry('1000x560')
        self.maxsize(1200,560)
        self.wm_iconbitmap("data/img/icon.ico")
        self.title('Restaurant')

        global name,phone_number 
        name = StringVar()
        phone_number = StringVar() 

        if theme == 1:
            self.light()
        elif theme == 2:
            self.dark()

        menubar = MenuBar(self)
        self.config(menu=menubar)

        self._frame = None
        self.switch_frame(Order_page)
        


    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if frame_class == Order_page:
            self.geometry('1000x560')
        else :
            pass
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(anchor='center',fill=X)

   
    def dark(self):
        global top_bg_color,menu_board_color,bill_board_color,menu_color,label_color,label_fg_color,top_fg_colour,fg_color,bg_color
        self.config(bg='gray10')
        top_bg_color = 'gray5'
        top_fg_colour = 'snow'
        menu_board_color = 'gray10'
        bill_board_color = 'gray80'
        menu_color = 'gray10'
        label_color = 'gray95'
        label_fg_color = 'snow'
        fg_color='snow'
        bg_color=menu_board_color


    def light(self):
        global top_bg_color,menu_board_color,bill_board_color,menu_color,label_color,label_fg_color,top_fg_colour,fg_color,bg_color
        self.config(bg='lightblue')
        top_bg_color = 'deepskyblue'
        top_fg_colour = 'black'
        menu_board_color = 'lightblue'
        bill_board_color = 'aliceblue'
        menu_color = 'aliceblue'
        label_color = 'skyblue'
        label_fg_color = 'black'
        fg_color='black'
        bg_color=menu_board_color



class Fuctions():


    def manager(master):
        master.switch_frame(Manager)
    
    def logs_():
        if len(logs)==0:
            pass
        else:
            file = open("data/docs/managers_logs.txt", "a")
            file.write(f'{datetime.datetime.now().strftime("%B %d, %Y")}\n\n')
            for k,v in logs.items():
                file.write(f'{k} : {v}\n')
            file.write("\n-------------------------------------------------------------------------------------\n\n")
            file.close()
        
    @staticmethod
    def save_var():
        f = open('data/store.p', 'wb')
        for i in range(1,len(qty)+1):
            pickle.dump(globals()['total_qty%s'%i],f)
        f.close()
        f1= open('data/app_data.p','wb')
        pickle.dump(theme,f1)
        pickle.dump(gst,f1)
        f1.close()

    @staticmethod
    def quitapp(self):
        pass
        self.destroy()

    @staticmethod
    def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)

    @staticmethod
    def new_order():
        global cont
        name.set('')
        phone_number.set('')
        select_dish.clear()
        for i in range(0,len(dish_list)):
            globals()['var%s'%i].set("0")
            globals()['checkbutton%s' % i].set(0)
            globals()['r1_%s' % i].set(0)
        bill_show.delete('1.0', END)
        order_button.config(state='normal')
        cont=0

    @staticmethod
    def check():
        if name.get() == '' or phone_number.get() == '' or len(phone_number.get()) != 10:
            msg.showerror(
                'Wrong Input', 'Please enter your name or\nPhone no correctly (must of 10 digits)')
            select_dish.clear()
            name.set('')
            phone_number.set('')
            return False
        else:
            return True

    @staticmethod
    def rewive():   
        for k, v in select_dish.items():
            a=k+1
            globals()['total_qty%s'%a]=globals()['total_qty%s'%a]+v
        select_dish.clear()

    @staticmethod
    def make_order_list():
        checkk= Fuctions.check()
        global cont
        if checkk == True:
            if cont==0:
                pass
            else:
                Fuctions.rewive()
        else:
            pass


        # checkk = True
        if checkk == True:
            cont=cont+1
            a = 0
            for i in range(0, len(dish_list)): 
                if globals()['checkbutton%s' % i].get() == 1:
                    a= i+1
                    x= int(globals()['qty%s' % i].get())+globals()['r1_%s' % i].get()
                    if globals()['total_qty%s'%a]>=x :
                        select_dish.update({i:x})
                        globals()['total_qty%s'%a]=globals()['total_qty%s'%a]-x
                            
                    elif globals()['total_qty%s'%a] == 0 :
                        msg.showinfo('Not avaliable',f'Sorry,We Dont have any more of {dish_list[i].capitalize()}')          
                    elif globals()['total_qty%s'%a]<x:
                        y= globals()['total_qty%s'%a]
                        msg.showinfo('Not avaliable',f'Sorry,We Dont have enough quantity of it.\nWe have only {y} quantity of {dish_list[i].capitalize()}.')
                else:
                    pass    
        else:
            pass


    @staticmethod
    def make_bill():
        f = open('data/docs/bill.txt', 'a')
        f.write(f"{time.asctime(time.localtime(time.time()))}\n")
        f.write(f'Name : {name.get()} Phone no : {phone_number.get()}\n\n')
        total = 0
        i = 0
        gst_total =0
        for k, v in select_dish.items():
            f.write(f'{i+1}]   {v} X {dish_list[k].capitalize()} @{price[k]}\n     Rs {price[k]*v}\n\n')
            i += 1
            total += price[k]*v
            gst_total +=v*gst

        f.write(f'\nTotal Bill is Rs.{total+gst_total}\n')
        f.write('-------------------------------------------------------\n\n')


    @staticmethod
    def bill():
        bill_show.delete('1.0', END)
        total = 0
        gst_total =0
        i = 0
        # bill_show.insert(INSERT, f'\n')
        bill_show.tag_config('m',justify='center',font=("Courier", 20, "bold"))
        bill_show.tag_config('p',justify='center',font=("Courier", 11, "bold"),foreground='red')
        bill_show.tag_config('g', foreground="green",)
        bill_show.tag_config('r', foreground="red",)
        bill_show.tag_config('b', foreground="lightblue",)
        bill_show.tag_config('c', foreground="hotpink",)
        bill_show.tag_config('v', foreground="blueviolet",)
        
        bill_show.insert(INSERT, f'BILL\n\n','m')
        for k, v in select_dish.items():
            bill_show.insert(INSERT, f'{i+1}] ')
            bill_show.insert(INSERT,f'{v}','v')
            bill_show.insert(INSERT,f' x','c')
            bill_show.insert(INSERT, f' {dish_list[k].capitalize()}')
            bill_show.insert(INSERT, f' @{price[k]}\n','v')
            bill_show.insert(INSERT,f'   Rs {price[k]*v}\n\n','v')
            i += 1
            total += price[k]*v
            # gst_qty +=v
            gst_total +=v*gst

        bill_show.insert(INSERT, f'\n#  Sub total Bill       Rs {total}',"g")
        bill_show.insert(INSERT, f'\n#  GST                  Rs {gst_total}','g')
        bill_show.insert(INSERT, f'\n#  Total Bill           Rs {total+gst_total}','g')
        bill_show.insert(INSERT,f'\n\n Total to Pay  Rs {total+gst_total}','p')
        if total == 0:
            pass
        else:
            Fuctions.make_bill()
            

    @staticmethod
    def print_bill():
        f = open('C:/Users/pc/Documents/tempbill.txt', 'w+')
        f.write(f"{time.asctime(time.localtime(time.time()))}\n")
        f.write(f'Name : {name.get()} Phone no : {phone_number.get()}\n\n')
        total = 0
        i = 0
        gst_total=0
        for k, v in select_dish.items():
            f.write(f'{i+1}]   {v} X {dish_list[k].capitalize()} @{price[k]}\n     Rs {price[k]*v}\n\n')
            i += 1
            total += price[k]*v
            gst_total +=v*gst
        f.write(f'\nTotal Bill is Rs.{total+gst_total}\n')
        f.close()

        os.startfile('C:/Users/pc/Documents/tempbill.txt', "print")


    @staticmethod
    def cancal():
        make_it=False
        res = msg.askquestion('It`s Confirm', 'Confirm do you want to cancal your order')
        if res == 'yes' :
            make_it = True
        else :
            make_it=False
        
        if make_it == True:
            Fuctions.rewive()
            Fuctions.new_order()




class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        


        m1 = Menu(self, tearoff=0, bg=menu_color, fg=label_fg_color,activebackground=label_color, activeforeground='black')
        m1.add_command(label='New Order',command=lambda :Fuctions.new_order())
        m1.add_command(label='Bill', command=lambda: Fuctions.bill())
        m1.add_command(label='Cancal', command=lambda:Fuctions.cancal())
        m1.add_command(label='Print',command=lambda:Fuctions.print_bill())
        m1.add_separator()
        m1.add_command(label='Exit',command=lambda:Fuctions.quitapp(parent))
        self.add_cascade(label='Menu', menu=m1)

        m2 = Menu(self, tearoff=0, bg=menu_color, fg=label_fg_color,activebackground=label_color, activeforeground='black')

        def temp_light():
            global theme
            theme=1
            msg.showinfo("RESTART", 'Please restart the application for appling the Theme')
        def temp_dark():
            global theme
            theme=2
            msg.showinfo("RESTART", 'Please restart the application for appling the Theme')

        m2_sub = Menu(m2,tearoff=0, bg=menu_color, fg=label_fg_color,activebackground=label_color, activeforeground='black')
        m2_sub.add_command(label='Dark', command=temp_dark)
        m2_sub.add_command(label='Light', command=temp_light)
        m2.add_cascade(label='Theme',menu=m2_sub)
        m2.add_command(label='Manager Tool',command=lambda: Fuctions.manager(parent))
        m2.add_command(label='Restart',command=lambda: Fuctions.restart_program())
        self.add_cascade(label='Settings', menu=m2)

        m3 = Menu(self, tearoff=0, bg=menu_color, fg=label_fg_color,activebackground=label_color, activeforeground='black')
        self.add_cascade(label='About', menu=m3)
        m3.add_command(label='Help', command=lambda: msg.showinfo('Help', 'We will help you soon'))
        m3.add_command(label='About', command=lambda: msg.showinfo('More About This', "Our mission is to be the most sustainable restaurant in New York by sourcing our ingredients locally, supplementing produce with herbs grown on our rooftop garden, and giving back to the community through urban farming education."))
        m3.add_command(label='More About', command=lambda: msg.showinfo('About', 'This GUI is created by AKG007\n            Made in India'))





class Order_page(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self,bg=menu_board_color)
        root=self
        top_frame = Frame(root, height=15, background=top_bg_color)
        top_frame.pack(side=TOP, anchor='n', fill=X)

        style_for_heading = ttk.Style()
        # logo=ImageTk.PhotoImage(Image.open(f"img/logo.png"))
        style_for_heading.configure('heading.TLabel',background=top_bg_color, font='Helvetica 25 bold',foreground=top_fg_colour)
        # logo_label=Label(top_frame,image=logo)
        # logo_label.grid(row=0,column=0,pady=30)
        global heading
        heading = ttk.Label(top_frame, text=Res_name,style='heading.TLabel')
        heading.pack(side=TOP, pady=20)
        # heading.grid(row=0,column=1,pady=30)

        info_frame = Frame(top_frame, bg=top_bg_color)
        info_frame.pack(anchor='nw', pady=10)
        # info_frame.grid(row=1,column=0)

        frame1 = Frame(info_frame)
        frame1.grid(row=0, column=0)
        name_label = Label(frame1, text='Name', bg=top_bg_color, font='Helvetica 10 bold',fg=top_fg_colour)
        name_label.grid(row=0, column=0,)

        name_entry_style=ttk.Style()
        name_entry_style.configure('name_entry.TEntry',font='Helvetica')
        name_entry = ttk.Entry(
                    frame1,style='name_entry.TEntry',textvariable=name)
        name_entry.grid(row=0, column=1)


        frame2 = Frame(info_frame)
        frame2.grid(row=0, column=1, padx=15)

        name_entry_style=ttk.Style()
        phone_number_label = Label(
                    frame2, text='Phone Number', bg=top_bg_color, font='Helvetica 10 bold',fg=top_fg_colour)
        phone_number_label.grid(row=0, column=0)

        name_entry_style.configure('phone_num_entry.TEntry',font='Helvetica ', )
        phone_number_entry = ttk.Entry(frame2,style='phone_num_entry.TEntry',textvariable=phone_number,)
        phone_number_entry.grid(row=0, column=1,)





        # -----------------------------------------------------------------------ITEMS------------------------------------------------------------------

        Scrollbar2 = ttk.Scrollbar(root)

        canvas=Canvas(root,yscrollcommand=Scrollbar2.set,width=470,bg=menu_board_color)
        canvas.pack(side=LEFT,anchor='nw', fill=Y,padx=10,pady=10)

        Scrollbar2.pack(side=LEFT, fill=Y)
        Scrollbar2.config(command=canvas.yview)

        main_frame = Frame(canvas, bg=menu_board_color,)
        main_frame.config(padx=10)
        # main_frame.pack(side=LEFT, anchor='nw', fill=Y,padx=10)
        canvas.create_window(0,0,window=main_frame,anchor='nw')


        Dish = Label(main_frame, text='MENU BORAD',
                            font='Helvetica 13 bold', bg=menu_board_color,fg=fg_color)
        Dish.pack(anchor='n',pady=(0,10))

        main_frame2 = Frame(main_frame, bg=menu_board_color, height=10)
                
        main_frame2.pack(anchor='sw')

        frame = Frame(main_frame2, bg=menu_board_color, width=300, height=200,)
        frame.grid(row=0, column=0)
        for i in range(0, len(dish_list)):
            globals()['no%s' % i] = Label(frame, text=f'{i+1}]', bg=menu_board_color,fg=fg_color)
            globals()['no%s' % i].pack(anchor='w', pady=2)

        frame2 = Frame(main_frame2, bg=menu_board_color, width=300, height=20,)
        frame2.grid(row=0, column=1)
        for i in range(0, len(dish_list)):
            globals()['checkbutton%s' % i] = IntVar()
            Checkbutton_style = ttk.Style()
            Checkbutton_style.configure('checkbutton.TCheckbutton', background=menu_board_color,foreground=fg_color,padx=10, pady=0,)
            a = ttk.Checkbutton(frame2, text=f'{dish_list[i].capitalize()}',style='checkbutton.TCheckbutton', onvalue=1, offvalue=0, variable=globals()['checkbutton%s' % i])
            globals()['dish%s' % i] = a
            globals()['dish%s' % i].pack(anchor='w', padx=10, pady=2)

        frame3 = Frame(main_frame2, bg=menu_board_color)
        frame3.grid(row=0, column=2, padx=8)
        for i in range(0, len(dish_list)):
            globals()['dish_price_label%s' % i] = Label(frame3, text=f'Rs.{price[i]}', bg=menu_board_color,fg=fg_color)
            globals()['dish_price_label%s' % i].grid(row=i,column=0, padx=(0, 30))
            globals()['r1_%s' % i] = DoubleVar()

            Checkbutton_style2 = ttk.Style()
            Checkbutton_style2.configure('checkbutton2.TCheckbutton', background=menu_board_color,foreground=fg_color,padx=10, pady=0,)
            c = ttk.Checkbutton(frame3, text='1/2p',style='checkbutton2.TCheckbutton',onvalue=0.5, offvalue=0, variable=globals()['r1_%s' % i])


            globals()['half_plate%s' % i] = c
            globals()['half_plate%s' % i].grid(row=i, column=1,padx=(20,5))
            globals()['var%s'%i] = StringVar(root)
            globals()['var%s'%i].set("0")
            Spinbox_style= ttk.Style()
            Spinbox_style.configure('w.TSpinbox',background=menu_board_color)
            c2 = ttk.Spinbox(frame3,from_=0,to=1000,font='Helvetica 10', textvariable=globals()['var%s'%i])
            globals()['qty%s'%i] = c2
            globals()['qty%s'%i].grid(row=i,column=2,pady=2)

        def disable(event=None):
            Fuctions.make_order_list()

        root.update()
        canvas.config(scrollregion=canvas.bbox("all"))





        # --------------------------------------------------------------------------BILL SHOW ----------------------------------------------------------

        mainframe3 = Frame(root, bg=menu_board_color, padx=12)
        mainframe3.pack(side=LEFT, anchor='n', fill=X)
        frame5 = Frame(mainframe3)
        frame5.pack()

        Scrollbar1 = ttk.Scrollbar(frame5)
        Scrollbar1.pack(side=RIGHT, fill=Y)

        def focus_next_window(event):
            event.widget.tk_focusNext().focus()
            return("break")


        global bill_show
        bill_show = Text(frame5, bg=bill_board_color, yscrollcommand=Scrollbar1.set,height=21.4)
        bill_show.pack(side=TOP, anchor='n', padx=4, pady=(25, 9), fill=BOTH)
        bill_show.bind("<Tab>", focus_next_window)
        Scrollbar1.config(command=bill_show.yview)

        def temp(event=None):
            # bill_button.config(state='disabled')
            Fuctions.bill()

        global order_button ,bill_button
        order_button = ttk.Button(mainframe3, text='Order', width=10, command=disable)
        order_button.pack(side=LEFT, anchor='n', padx=5, pady=15)
        order_button.bind('<Return>',disable)
        order_button.focus_set()

        bill_button = ttk.Button(mainframe3, text='Bill', width=10, command=temp)
        # bill_button.config(state='disabled')
        bill_button.pack(side=RIGHT, anchor='n', pady=15, padx=5)
        # bill_button.bind('<Return>',temp)
        # bill_button.focus()

class Manager(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self,bg=menu_board_color)
        master.geometry('400x500')

        global user
        user=StringVar()
        global passs
        passs=StringVar()

        
        Style1 =  ttk.Style()
        Style1.configure('TLabel',background=bg_color,foreground=fg_color)

        f1=Frame(self,bg=bg_color)
        f1.pack(anchor=CENTER,pady=200)

        user_label=ttk.Label(f1,text='USER ',style='TLabel')
        passs_label=ttk.Label(f1,text='PASSWORD ',style='TLabel')
        user_label.grid(row=0,column=0)
        passs_label.grid(row=1,column=0)

        user_entry=ttk.Entry(f1,textvariable=user)
        passs_entry=ttk.Entry(f1,textvariable=passs)
        user_entry.grid(row=0,column=1)
        passs_entry.grid(row=1,column=1)
                    
        button = ttk.Button(f1,text='Enter',command=lambda : self.enter(master))
        button.grid(row=2,column=1)
        # button.bind('<Return>',self.enter())
        button.focus()
    @staticmethod
    def enter(master):
        if user.get() == listt[0] and passs.get()==listt[1]:
            # raise_frame(f2)
            # logs.update(open_at = time_now)
            master.switch_frame(Manager_buttons)
            # print('Done')
        else:
                msg.showerror('Wrong',"Wrong user or password")
                user.set('')
                passs.set('')



class Manager_buttons(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self,bg=menu_board_color)
        f2=self
        global logs

        but1=ttk.Button(f2,text='See All Bill',width=30,command=self.see_bill)
        but2=ttk.Button(f2,text='Change Menu Board',width=30,command=lambda:self.change_menu_board(master))
        but3=ttk.Button(f2,text='Restart Application',width=30,command=self.reset)
        but7=ttk.Button(f2,text='Set GST and Restraturent Name',width=30,command=lambda : master.switch_frame(Set_gst))
        but6=ttk.Button(f2,text='Change Password and Username',width=30,command = lambda: master.switch_frame(Change_password))
        but4=ttk.Button(f2,text='Back',width=30,command=lambda : master.switch_frame(Order_page))
        but5=ttk.Button(f2,text='See & Set remaining products',width=30,command=lambda:self.remaing())

        but1.pack(pady=(130,5),padx=(0,0),)
        but5.pack(pady=5,padx=(0,0))
        but2.pack(pady=5,padx=(0,0))
        but6.pack(pady=5,padx=(0,0))
        but3.pack(pady=5,padx=(0,0))
        but7.pack(pady=5,padx=(0,0))
        but4.pack(pady=(28,0),padx=(0,0))

    @staticmethod
    def see_bill():
        logs.update(see_bills = time_now)
        subprocess.call(["notepad.exe","data/docsbill.txt"])

    @staticmethod
    def reset():
        logs.update(reset_at = time_now)
        if os.path.isfile('data/store.p'):
                os.remove('data/store.p')
                os.remove('data/app_data.p')
        msg.showinfo('Done','Application has been reset')

    
    def remaing(self):
        logs.update(see_change_remaing_items = time_now )
        if os.path.isfile('data/store.p'):
            f = open('data/docs/remaing.txt', 'a+')
            for i in range (0,len(qty)):
                a=i+1
                f.write(f'{dish_list[i].capitalize()} {globals()["total_qty%s"%a]}\n')
            f.close()
        else:
            f = open('data/docs/remaing.txt', 'a+')
            for i in range (0,len(qty)):
                f.write(f'{dish_list[i].capitalize()} {qty[i]}\n')
            f.close()
        subprocess.call(["notepad.exe","data//remaing.txt"])
        self.save_var()

    @staticmethod
    def save_var():
        with open("data//remaing.txt") as f:
            for line,i in zip(f,range(1,len(qty)+1)):
                (dish,qtyy) = line.split()
                qtyy=float(qtyy)
                globals()["total_qty%s"%i]=qtyy

        f = open('data/store.p', 'wb')
        for i in range(1,len(qty)+1):
            pickle.dump(globals()['total_qty%s'%i],f)
        f.close()
        os.remove('data/docs/remaing.txt')

    @staticmethod
    def change_menu_board(master):
        logs.update(change_menu_board = time_now)
        subprocess.call(["notepad.exe","data/docs/menu.txt"])
        if os.path.isfile('data/store.p'):
                os.remove('data/store.p')
        msg.showinfo('Warning','For Appling Changes Application is been Closed')
        master.destroy()
        Fuctions.logs_()
        exit(0)



    



class Set_gst(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self,bg=menu_board_color)
        global logs

        Style1 =  ttk.Style()
        Style1.configure('TLabel',background=bg_color,foreground=fg_color)

        f4=Frame(self,bg=bg_color)
        f4.pack(pady=200)

        gst_set_value_label=ttk.Label(f4,text='Enter GST',style='TLabel')
        gst_set_value_label.grid(row=0,column=0)
        self._gst=StringVar()
        self._gst.set(gst)
        Enter_gst=ttk.Entry(f4,textvariable=self._gst)
        Enter_gst.grid(row=0,column=1)

        name_set_value_label=ttk.Label(f4,text='Enter Restrutent Name',style='TLabel')
        name_set_value_label.grid(row=1,column=0)
        self._res_name=StringVar()
        self._res_name.set(Res_name)
        enter_name=ttk.Entry(f4,textvariable=self._res_name)
        enter_name.grid(row=1,column=1)

        button2=ttk.Button(f4,text="Enter",command=lambda:self.set_gst(master))
        button2.grid(row=2,column=1,pady=10)

    def set_gst(self,master):
        try:
            if type(float(self._gst.get()))==float:
                f1= open('data/app_data.p','wb')
                pickle.dump(theme,f1)
                pickle.dump(float(self._gst.get()),f1)
                f1.close()
                f=open("data/name.p",'wb')
                pickle.dump(self._res_name.get(),f)
                Res_name = self._res_name.get()
                # heading.config(text=Res_name)
                msg.showinfo('Done',"GST and Name value has been change")
                logs.update(change_gst = f'{time_now}, set the value {self._gst.get()}')
                logs.update(change_Name = f'{time_now}, set the name {self._res_name.get()}')
                msg.showinfo('Warning','For Appling Changes Application is been Closed')
                master.destroy()
                Fuctions.logs_()
                exit(0)
                # master.switch_frame(Manager_buttons)

        except ValueError :
            msg.showerror('Wrong Input','Please input valid gst(must be a numerical value)')
            self._gst.set('')



class Change_password(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self,bg=menu_board_color)
        f3=Frame(self,bg=bg_color)
        f3.pack(pady=200)
        global logs

        Style2 =  ttk.Style()
        new_user_label=ttk.Label(f3,text='NEW USER ',style='TLabel')
        new_passs_label=ttk.Label(f3,text='NEW PASSWORD ',style='TLabel')
        new_user_label.grid(row=0,column=0)
        new_passs_label.grid(row=1,column=0)
        new_user= StringVar()
        new_passs= StringVar()
        new_user_entry=ttk.Entry(f3,textvariable=new_user)
        new_passs_entry=ttk.Entry(f3,textvariable=new_passs)
        new_user_entry.grid(row=0,column=1)
        new_passs_entry.grid(row=1,column=1)

        def change_new(master):
            f = open('data/pass.p', 'wb')
            pickle.dump([str(new_user.get()),str(new_passs.get())],f)
            f.close()
            logs.update(change_password_and_username = time_now)
            msg.showinfo('Done','Password and Username has been change')
            master.switch_frame(Manager_buttons)
            

        button1 = ttk.Button(f3,text='Enter',command=lambda:change_new(master))
        button1.grid(row=2,column=1)
        button1.bind('<Return>',lambda:change_new(master))
        button1.focus()





app = SampleApp()
app.mainloop()
Fuctions.save_var()
Fuctions.logs_()
