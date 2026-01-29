bank_data = {}
with open("data base.txt", mode='r') as file:
    PAN = None
    for line in file:
        stripped_line = line.strip()
        if not line.startswith("\t"):
            PAN = stripped_line
            bank_data[PAN] = {}
        else:
            key, value = stripped_line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if PAN is not None:
                bank_data[PAN][key] = value
               
from tkinter import *

c = 3
home_window = Tk()
home_window.title("ELBANK ELAHLY")
home_window.geometry("700x700+500+50")
home_window.resizable(False, False)


def show_error(message, color="red",width="500"):
     error_id_window=Tk()
     error_id_window.geometry(f"{width}x50+600+400")
     error=Label(error_id_window,text=message,fg=color).place(x=30,y=0)

def reset_home_window():
    for widget in home_window.winfo_children():
        widget.destroy()
    setup_home_window()
    
btn = Button(home_window, text="Home window",command = reset_home_window,bg="black",fg="white").place(x=300,y=600)
def setup_home_window():
    idlabel = Label(home_window, text="Enter your account number", font=("Arial", 15))
    idlabel.place(x=0, y=0)
    global identer
    identer = Entry(home_window)
    identer.place(x=250, y=6)
    btn = Button(home_window, text="Enter", command=idcheck)
    btn.place(x=250, y=30)
    btn = Button(home_window, text="Home window",command = reset_home_window,bg="black",fg="white").place(x=300,y=600)
    

def idcheck():
    account_id = identer.get()
    if account_id not in bank_data:
        identer.delete(0, END)
        show_error("The ID is not found. Please enter the correct ID")
    elif bank_data[account_id]["status"] == "active":
        home_window.update()           
        home_window.after(100, nextstep)  
    elif bank_data[account_id]["status"] == "blocked":
        identer.delete(0, END)
        show_error("Your account is locked. You have to go to any branch to get it activated")

def nextstep():
    passlabel = Label(home_window, text="Enter your password", font=("Arial", 15))
    passlabel.place(x=0, y=60)
    global passenter
    passenter = Entry(home_window, show="*")
    passenter.place(x=250, y=66)

    def passcheck():
        global c
        account_id = identer.get()
        if passenter.get() != bank_data[account_id]["password"]:
            passenter.delete(0, END)
            c -= 1
            if c > 0:
                show_error(f"wrong password Please enter the correct one. You have {c} tries")
        if c == 0:
            bank_data[account_id]['status'] = 'blocked'
            with open("data base.txt", mode='w') as file:
                for main_key, nested_dict in bank_data.items():
                    file.write(f'{main_key}\n')
                    for key, value in nested_dict.items():
                        file.write(f'\t{key}: {value}\n')
            identer.delete(0, END)
            passenter.delete(0, END)
            show_error("Your account is locked. You have to go to any branch to get it activated")
            home_window.after(1000, reset_home_window)
        elif passenter.get() == bank_data[account_id]["password"]:
            home_window.update()
            #show_error("if there is an option you can make another option after it you will find return back button \n                                 else you must click the main return back button if you want as this option will return you to the home page after finishing","blue","700")
            home_window.after(100, nextstep2)

    btn = Button(home_window, text="Enter", command=passcheck)
    btn.place(x=250, y=90)

def nextstep2():

    global c
    c=3
    btn = Button(home_window, text="return back",command =nextstep2,bg="black",fg="white").place(x=300,y=550)
    whitelabel=Label(home_window,text="                                                   ", font=("Arial", 162)).place(x=0,y=280)
    z = IntVar()
    def cashwithdraw():
        whitelabel=Label(home_window,text="                                                   ", font=("Arial", 105)).place(x=0,y=290)
        amountlabel = Label(home_window, text="Enter the desired amount to withdraw", font=("Arial", 15))
        amountlabel.place(x=0, y=310)
        amountenter = Entry(home_window)
        amountenter.place(x=350, y=315)

        def ATM_ACTUATOR_OUT():
            bank_data[identer.get()]["balance"] = int(bank_data[identer.get()]["balance"]) - int(amountenter.get())
            with open("data base.txt", mode='w') as file:
                for main_key, nested_dict in bank_data.items():
                    file.write(f'{main_key}\n')
                    for key, value in nested_dict.items():
                        file.write(f'\t{key}: {value}\n')
            show_error("Successful operation, thank you", "green")
            amountenter.delete(0, END)
            home_window.after(1000, reset_home_window)  # Reset home window after a delay

        def checkamount():
                amount = int(amountenter.get())
                if amount <= 5000 and amount % 100 == 0:
                    if amount <= int(bank_data[identer.get()]["balance"]):
                        ATM_ACTUATOR_OUT()
                    else:
                        amountenter.delete(0, END)
                        show_error("Insufficient balance")
                else:
                    amountenter.delete(0, END)
                    show_error("Invalid amount")
        btn = Button(home_window, text="Enter", command=checkamount)
        btn.place(x=250, y=350)
    
    def balancecheck():
        whitelabel=Label(home_window,text="                                                   ", font=("Arial", 162)).place(x=0,y=280)
        name=Label(home_window,text=f"Mr : {bank_data[identer.get()]["name"]}",relief="raised",bg="skyblue")
        name.place(x=0,y=300)
        balance=Label(home_window,text=f"your balance is : {bank_data[identer.get()]["balance"]}",relief="raised",bg="skyblue")
        balance.place(x=0,y=320)
        def gotohomepage():
            home_window.after(100, reset_home_window)
        def returnback():
            nextstep2()
        btn = Button(home_window, text="Ok",command =gotohomepage)
        btn.place(x=250, y=370)
        btn = Button(home_window, text="Return back",command =returnback)
        btn.place(x=250, y=400)
    def passchange():
        whitelabel=Label(home_window,text="                                                   ", font=("Arial", 162)).place(x=0,y=280)
        
        newpassl=Label(home_window,text="enter the new password ",font=("Arial", 15)).place(x=0,y=290)
        newpass=Entry(home_window,show="*")
        newpass.place(x=250,y=296)
        newpassl2=Label(home_window,text="confirm the new password ",font=("Arial", 15)).place(x=0,y=320)
        newpass2=Entry(home_window,show="*")
        newpass2.place(x=250,y=326)
        def checknewpass():
            if len(newpass.get())==4:
                if(newpass.get()==newpass2.get()):
                    show_error("seccessful operation","green")
                    bank_data[identer.get()]["password"]=newpass.get()
                    with open("data base.txt", mode='w') as file:
                        for main_key, nested_dict in bank_data.items():
                            file.write(f'{main_key}\n')
                            for key, value in nested_dict.items():
                                file.write(f'\t{key}: {value}\n')
                    nextstep2()   
                else:
                    show_error("no match please renter the confirmation")
                    newpass2.delete(0, END)
            else:
                 show_error("password should be 4 numbers please renter it")
                 newpass2.delete(0, END)
                 newpass.delete(0, END)
        btn = Button(home_window, text="Done",command =checknewpass)
        btn.place(x=250, y=350)
        btn = Button(home_window, text="Return back",command =nextstep2)
        btn.place(x=250, y=380)
                
    def fawryservice():
        whitelabel=Label(home_window,text="                                                   ", font=("Arial", 162)).place(x=0,y=280)
        
        def fawrycharge():
            phone=Label(home_window,text="enter the phone number need to recharge",font=("Arial", 15)).place(x=0,y=440)
            phonerecharge=Entry(home_window)
            phonerecharge.place(x=400,y=446)
            fawryrechargelabel=Label(home_window,text="enter the rechrging amount",font=("Arial", 15)).place(x=0,y=470)
            recharge=Entry(home_window)
            recharge.place(x=250,y=476)
            def checkrecharge():
                if(int(recharge.get())>int(bank_data[identer.get()]["balance"])):
                    show_error("no suffecient balance ")
                    home_window.after(100, reset_home_window) 
                else:
                    bank_data[identer.get()]["balance"]=int(bank_data[identer.get()]["balance"])-int(recharge.get())
                    show_error("successful process","green")
                    with open("data base.txt", mode='w') as file:
                        for main_key, nested_dict in bank_data.items():
                            file.write(f'{main_key}\n')
                            for key, value in nested_dict.items():
                                file.write(f'\t{key}: {value}\n')
                    nextstep2()
                    
                
            btn = Button(home_window, text="Done",command =checkrecharge).place(x=250,y=500)
            
        x=IntVar()
        btn = Radiobutton(home_window, text="1- Orange Recharge", value=10, variable=x, font=("Arial", 15),bg="grey",command=fawrycharge)
        btn.place(x=0, y=310)
        btn = Radiobutton(home_window, text="2- Etisalat Recharge", value=11, variable=x, font=("Arial", 15),bg="grey",command=fawrycharge)
        btn.place(x=0, y=340)
        btn = Radiobutton(home_window, text="3- Vodafone Recharge", value=12, variable=x, font=("Arial", 15),bg="grey",command=fawrycharge)
        btn.place(x=0, y=370)
        btn = Radiobutton(home_window, text="4- We Recharge.", value=13, variable=x, font=("Arial", 15),bg="grey",command=fawrycharge)
        btn.place(x=0,y=400)
    def exitbye():
        home_window.after(100, reset_home_window)

    btn = Radiobutton(home_window, text="Cash Withdraw", value=0, variable=z, command=cashwithdraw,font=("Arial", 15))
    btn.place(x=0, y=130)
    btn = Radiobutton(home_window, text="Balance Inquiry", value=1, variable=z,command=balancecheck,font=("Arial", 15))
    btn.place(x=0, y=160)
    btn = Radiobutton(home_window, text="Password Change", value=2, variable=z,command=passchange,font=("Arial", 15))
    btn.place(x=0, y=190)
    btn = Radiobutton(home_window, text="Fawry Service", value=3, variable=z,command=fawryservice,font=("Arial", 15))
    btn.place(x=0, y=220)
    btn = Radiobutton(home_window, text="Exit", value=4, variable=z,font=("Arial", 15),command=exitbye)
    btn.place(x=0, y=250)
setup_home_window()
home_window.mainloop()