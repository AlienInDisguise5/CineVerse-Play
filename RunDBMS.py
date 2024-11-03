import mysql.connector as sql
import os
from tkinter import *
from tkinter.ttk import *

conn=sql.connect(user='<YOUR MYSQL USERNAME>',host='localhost',password='<YOUR MYSQL PASSWORD>',db='DBMS_Mini_Project_Final')
csr=conn.cursor()

print(os.getcwd())

#ClearingScreen
def clear_window():
    for child in Win.winfo_children():
        child.destroy()
        
#QuittingProgram
def close():
    conn.close()
    quit()

#Verify Login information
def verify_login(M_ID, Phone):
    global Username, Name
    Username=M_ID.get()
    Password=Phone.get()
    csr.execute(f"select Full_Name, Member_ID from Member where Member_ID ='{Username}' and Phone_Number='{Password}'")
    Result=csr.fetchall()
    if Result:
        Name=Result[0][0]
        Username=Result[0][1]
        print(Username)
        main_window()
    else:
        print("Incorrect Member ID or Phone Number")

#Search by Movie window
def movie_name_search(moviename):
    name=moviename.get()
    print(name)
    csr.execute(f"select Movie_Name, Language, Year_Of_Release, Rental_Cost_Per_Day from Movie where Movie_Name like '{name}%'")
    MovieData=csr.fetchall()
    print(MovieData)
    select_movie_window(MovieData)

#Search by Genre window
def genre_search(genre_value):
    genre=genre_value.get()
    print(genre)
    csr.execute(f"select Movie_Name, Language, Year_Of_Release, Rental_Cost_Per_Day from Movie where Movie_ID in (select Movie_ID from Movie_Genre where Genre_ID in (select Genre_ID from Genre where Genre='{genre}'))")
    MovieData=csr.fetchall()
    print(MovieData)
    select_movie_window(MovieData)

#Search by Cast window
def cast_search(moviecast):
    cast=moviecast.get()
    print(cast)
    csr.execute(f"select Movie_Name, Language, Year_Of_Release, Rental_Cost_Per_Day from Movie where Movie_ID in (select Movie_ID from Movie_Cast where Cast_ID in (select Cast_ID from Cast where Director like '%{cast}%' or Lead_Actor like '%{cast}%' or Lead_Actress like '% {cast}%'))")
    MovieData=csr.fetchall()
    print(MovieData)
    select_movie_window(MovieData)

#Confirm Movie
def confirm_movie(tree):
    curItem=tree.focus()
    for i in tree.item(curItem):
        items=tree.item(curItem)['values']
    confirm_purchase_window(items)

#Confirm Purchase
def verify_purchase(rental_date,expiry_date,rate):
    global rental, expiry, totalcost
    rental=rental_date.get()
    expiry=expiry_date.get()
    if expiry>rental and rental[0:7]==expiry[0:7]: 
        rentdate=int(rental[8:])
        print(rentdate)
        expirydate=int(expiry[8:])
        print(expirydate)
        totalcost=int(rate)*(expirydate-rentdate)
        print(totalcost)
        billing_window(totalcost)
    else:
        print("Enter valid date please")

#Verify CVV
def verify_CVV(CVV):
    CVVcheck=CVV.get()
    csr.execute(f"select * from payment_Info where Member_ID ='{Username}' and CVV={CVVcheck}")
    Result=csr.fetchall()
    if Result:
        print(Username)
        print(CVVcheck)
        final_window()
    else:
        print("Incorrect CVV")
    

#LoginWindow
def login_window():
    
    global BgImage, BgImage2
    BgImage=PhotoImage(file=r"Images\CineVerse2.gif")
    BgImage2=PhotoImage(file=r"Images\CineVerse2Blank.gif")
    Label(Win,image=BgImage).place(relx=0.5,rely=0.5,anchor='center')
    Win.title("CineVerse PLAY")

    Login=Frame(Win)
    Label(Login,text="Member ID").grid(row=0,column=0)
    Label(Login,text="Phone No.").grid(row=1,column=0)

    M_ID=StringVar()
    Phone=StringVar()
    Entry(Login,textvariable=M_ID).grid(row=0, column=1)
    Entry(Login,textvariable=Phone).grid(row=1, column=1)

    Button(Login, text="Login", command=lambda:verify_login(M_ID,Phone)).grid(row=3, column=0, columnspan=2)

    Login.place(relx=0.15, rely=0.5)

#MainWindow
def main_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')

    MainMenu=Frame(Win)
    Label(MainMenu,text="Hello, %s!"%Name).grid(row=0,column=0)
    B1=Button(MainMenu,text="Rent Movie", command=rent_movie_window).grid(row=1,column=0, columnspan=2)
    B2=Button(MainMenu,text="View Past Purchases", command=past_purchases_window).grid(row=2,column=0, columnspan=2)
    B3=Button(MainMenu,text="View Payment Info", command=payment_info_window).grid(row=3,column=0, columnspan=2)
    B4=Button(MainMenu,text="Exit",command=close).grid(row=4,column=0)
    MainMenu.place(relx=0.375, rely=0.425)
  
#RentMovieWindow
def rent_movie_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')

    RentMenu=Frame(Win)
    B1=Button(RentMenu,text="Search by Movie Name", command=search_by_movie_name_window).grid(row=1,column=0, columnspan=2)
    B2=Button(RentMenu,text="Search by Genre", command=search_by_genre_window).grid(row=2,column=0, columnspan=2)
    B3=Button(RentMenu,text="Search by Cast member", command=search_by_cast_window).grid(row=3,column=0, columnspan=2)
    B4=Button(RentMenu,text="Back",command=main_window).grid(row=4,column=0)
    RentMenu.place(relx=0.375, rely=0.425)

#MovieNameWindow
def search_by_movie_name_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')
    MovienameMenu=Frame(Win)
    
    Label(MovienameMenu,text="Enter Movie Name").grid(row=0,column=0)
    moviename=StringVar()
    Entry(MovienameMenu,textvariable=moviename).grid(row=0, column=1)

    B1=Button(MovienameMenu,text="Confirm", command=lambda: movie_name_search(moviename)).grid(row=1,column=0, columnspan=2)
    MovienameMenu.place(relx=0.2, rely=0.425)
    
#GenreWindow
def search_by_genre_window():
    clear_window()
    Label(image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')
    global genre_value
    GenreMenu=Frame(Win)

    Label(GenreMenu,text="Choose Genre").grid(row=1,column=0)
    list1=['','Drama','Comedy','Thriller','Action','Crime','Romance','Mystery','Sci-fi','Adventure','Fantasy','Music','War','Animation','Horror']
    genre_value=StringVar()
    droplist=OptionMenu(GenreMenu,genre_value,*list1)
    genre_value.set("Select")
    droplist.grid(row=1,column=1)
    
    B1=Button(GenreMenu,text="Confirm",command=lambda: genre_search(genre_value)).grid(row=2,column=0, columnspan=2)
    GenreMenu.place(relx=0.375, rely=0.425)

#CastWindow
def search_by_cast_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')
    CastMenu=Frame(Win)
    
    Label(CastMenu,text="Enter Director/Actor/Actress").grid(row=0,column=0)
    moviecast=StringVar()
    Entry(CastMenu,textvariable=moviecast).grid(row=0, column=1)

    B1=Button(CastMenu,text="Confirm", command=lambda: cast_search(moviecast)).grid(row=1,column=0, columnspan=2)
    CastMenu.place(relx=0.2, rely=0.425)

#Select Movie Window
def select_movie_window(Data):
    clear_window()
    MovieMenu=Frame(Win)

    MovieTree=Treeview(Win)
    MovieTree['show'] = 'headings'
    MovieTree['columns']=(0,1,2,3)
    
    MovieTree.column(0,width=200)
    MovieTree.column(1,width=100)
    MovieTree.column(2,width=100)
    MovieTree.column(3,width=100)

    
    MovieTree.heading(0,text="Movie Name")
    MovieTree.heading(1,text="Language")
    MovieTree.heading(2,text="Year")
    MovieTree.heading(3,text="Rental Cost/Day")

    MovieMenu.place(relx=0, rely=0, relheight=1, relwidth=1)
    MovieTree.pack()
    
    for index in range (len(Data)):
        MovieTree.insert('','end',values=(Data[index]))

    Button(MovieMenu,text="Choose a Movie",command=lambda: confirm_movie(MovieTree)).place(relx=0.5,rely=0.55, anchor='center')

   
#Confirm Purchase Window
def confirm_purchase_window(movie):
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')
    global MovieName
    print(movie)
    MovieName=movie[0]
    ConfirmMenu=Frame(Win)
    Label(ConfirmMenu,text="Movie: %s"%movie[0]).grid(row=0,column=0)
    Label(ConfirmMenu,text="Rent: %s"%movie[3]).grid(row=1,column=0)
    
    Label(ConfirmMenu,text="Enter Rental Date(YYYY-MM-DD)").grid(row=2,column=0)
    Label(ConfirmMenu,text="Enter Expiry Date(YYYY-MM-DD)").grid(row=3,column=0)
    Rental_Date=StringVar()
    Expiry_Date=StringVar()
    Entry(ConfirmMenu,textvariable=Rental_Date).grid(row=2, column=1)
    Entry(ConfirmMenu,textvariable=Expiry_Date).grid(row=3, column=1)

    B1=Button(ConfirmMenu,text="Confirm", command=lambda: verify_purchase(Rental_Date,Expiry_Date,movie[3])).grid(row=4,column=0, columnspan=2)
    ConfirmMenu.place(relx=0.2, rely=0.425)

   
#Billing Window 
def billing_window(cost):
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')

    BillingMenu=Frame(Win)
    Label(BillingMenu,text="Total Cost: %s"%cost).grid(row=0,column=0)
    Label(BillingMenu,text="Enter CVV").grid(row=2,column=0)
    CVV=IntVar()
    Entry(BillingMenu,textvariable=CVV).grid(row=2, column=1)

    B1=Button(BillingMenu,text="Confirm", command=lambda: verify_CVV(CVV)).grid(row=4,column=0, columnspan=2)
    BillingMenu.place(relx=0.2, rely=0.425)

#Thank you for buying
def final_window():

    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')

    FinalMenu=Frame(Win)
    Label(FinalMenu,text="Thank you for making a purchase!").grid(row=0,column=0)

    csr.execute(f"select Rental_ID from Rental order by Rental_ID desc")
    Result=(csr.fetchall())[0][0]
    temp=int((Result)[1:])
    temp+=1
    newRentalID=f"R{temp:0>2}"
    print(newRentalID)

    
    csr.execute("insert into Rental values('{}','{}','{}','{}',{})".format(newRentalID, Username, rental, expiry, totalcost))

    csr.execute(f"select Movie_ID from Movie where Movie_Name = '{MovieName}'")
    MovieID=csr.fetchall()[0][0]
    print(MovieID)
    
    csr.execute("insert into Movie_Rental values('{}','{}')".format(newRentalID, MovieID))
    conn.commit()
    
    
    B1=Button(FinalMenu,text="Exit", command=close).grid(row=1,column=0, columnspan=2)
    FinalMenu.place(relx=0.2, rely=0.425)
    
#PastPurchasesWindow
def past_purchases_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')
    PurchasesMenu=Frame(Win)

    tree=Treeview(Win)
    tree['show'] = 'headings'
    tree['columns']=(0,1,2,3,4)
    
    tree.column(0,width=220)
    tree.column(1,width=60)
    tree.column(2,width=80)
    tree.column(3,width=80)
    tree.column(4,width=60)
    
    tree.heading(0,text="Movie Name")
    tree.heading(1,text="Rental ID")
    tree.heading(2,text="Rental Date")
    tree.heading(3,text="Expiry Date")
    tree.heading(4,text="Total Cost")

    PurchasesMenu.place(relx=0, rely=0, relheight=1, relwidth=1)
    tree.pack()
    
    Button(PurchasesMenu,text="Back",command=main_window).place(relx=0.5,rely=0.55, anchor='center')

    csr.execute(f"select Rental_ID, Rental_Date, Rental_Expiry, Total_Cost from Rental where Member_ID ='{Username}'")
    ResultData=csr.fetchall()
    print(Username)
  
    csr.execute(f"select Movie_Name from Movie where Movie_ID in (select Movie_ID from Movie_Rental where Rental_ID in (select Rental_ID from Rental where Member_ID='{Username}'))")
    ResultMovie=csr.fetchall()

    for index in range (len(ResultData)):
        tree.insert('','end',values=(ResultMovie[index]+ResultData[index]))    
  
#PaymentInfoWindow
def payment_info_window():
    clear_window()
    Label(Win,image=BgImage2).place(relx=0.5,rely=0.5,anchor='center')

    csr.execute(f"select Details_ID, Card_Number, Expiry, CVV from Payment_Info where Member_ID ='{Username}'")
    Result=csr.fetchall()
    D_ID=Result[0][0]
    Card=Result[0][1]
    Expiry=Result[0][2]
    CVV=Result[0][3]

    print(Username)
    
    PaymentMenu=Frame(Win)
    Label(PaymentMenu,text="Details ID: %s"%D_ID).grid(row=0,column=0)
    Label(PaymentMenu,text="Card Number: %s"%Card).grid(row=1,column=0)
    Label(PaymentMenu,text="Expiry: %s"%Expiry).grid(row=2,column=0)
    Label(PaymentMenu,text="CVV: %s"%CVV).grid(row=3,column=0)
    B1=Button(PaymentMenu,text="Back",command=main_window).grid(row=4,column=0)
    
    PaymentMenu.place(relx=0.375, rely=0.425)

if __name__=='__main__':
    Win=Tk()
    Win.geometry("500x500+500+200")
    login_window()
    Win.mainloop()
