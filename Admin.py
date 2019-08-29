import pymysql
conn=pymysql.connect(host='localhost',user='root',password='',db='jpr')
a1=conn.cursor()
#s1="SELECT * FROM user_data"
ch=int(input("\n1.Date based \n2.Date and id based"))
if ch==1:
    dat=input("Enter date(yyyy-mm-dd)")
    print("\n")
    print("**********************************************************")
    print("                         INDATA                           ")
    print("\n")
    s1="SELECT * FROM inat WHERE date (%s)"
    a1.execute(s1,[dat])
    data=a1.fetchall()
    print("Id               Name             intime          date")
    for i in data:
        print(i[0],"     ",i[1],"     ",i[2],"     ",i[3])
    print("\n")
    print("***********************************************************")
    print("                         OUTDATA                           ")
    print("\n")
    s1="SELECT * FROM outat WHERE date (%s)"
    a1.execute(s1,[dat])
    data=a1.fetchall()
    print("Id               Name             outtime         date")
    for i in data:
        print(i[0],"     ",i[1],"     ",i[2],"     ",i[3])
elif ch==2:
    dat=input("Enter date(yyyy-mm-dd)")
    id=input("Enter student id")
    print("\n")
    print("**********************************************************")
    print("                         INDATA                           ")
    print("\n")
    s1="SELECT * FROM inat WHERE date=(%s) AND id=(%s)"
    a1.execute(s1,[dat,id])
    data=a1.fetchall()
    print("Id               Name             intime          date")
    for i in data:
        print(i[0],"     ",i[1],"     ",i[2],"     ",i[3])
    print("\n")
    print("***********************************************************")
    print("                         OUTDATA                           ")
    print("\n")
    s1="SELECT * FROM outat WHERE date=(%s) AND id=(%s)"
    a1.execute(s1,[dat,id])
    data=a1.fetchall()
    print("Id               Name             outtime         date")
    for i in data:
        print(i[0],"     ",i[1],"     ",i[2],"     ",i[3])
else:
    print("Invalid choice")
