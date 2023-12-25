from tkinter import *
from tkinter import messagebox, filedialog
#from Src import *
#from Util import *
import requests
import shutil
def Connection_status():
     try:
          api='http://127.0.0.1:8000/auth/'
          req=requests.get(api)
          if req.status_code==200:
               return True
     except (requests.ConnectionError, requests.Timeout) as exceptions:
          print("No Internet")
          print('''You can still upload files!!!, your files will be stored locally and
               uploaded to cloud once internet is available...''')
          print("Initiating File Upload Protocol")
          return False
class app:
     def __init__(self):
          self.root=Tk()
          self.root.geometry('1080x960')
          self.root.title("MGCloud")
          self.uname=StringVar(self.root)
          self.pwd=StringVar(self.root)
          self.frame1=Frame(self.root)
          self.frame1.pack()

          #--------------------------API REQUESTS--------------------------#

          self.auth_url='http://127.0.0.1:8000/auth/'
          self.auth_data=requests.get(self.auth_url).json()

          Label(self.frame1,text="MGCloud",fg="black",font=('Arial',30,'bold')).pack(pady=(30,0))
          Label(self.frame1,text="Sign In",fg="black",font=('Arial',25)).pack(pady=(20,0))
          Label(self.frame1,text='Username',font=('Arial',16)).pack(padx=(0,260))
          self.inp1=Entry(self.frame1,text="Username",font=('Arial',25),textvariable=self.uname).pack()
          Label(self.frame1,text='Password',font=('Arial',16)).pack(padx=(0,260))
          self.inp2=Entry(self.frame1,text="password",font=('Arial',25),show='*',textvariable=self.pwd).pack(pady=(10,0))
          Button(self.frame1,text="Submit",font=('Arial',15),command=self.__Login).pack(ipadx=10,ipady=10,pady=(20,10))
          Button(self.frame1,text="SignUp",font=('Arial',15),command=self.__Signup).pack(ipadx=10,ipady=10)

     def __Login(self):
          authenticated=False
          username,passwd=self.uname.get(),self.pwd.get()
          for i in self.auth_data:
               if i[0]==username and i[1]==passwd:
                    print("Access Granted to user ", username)
                    self.ForeignKey=i[2]
                    print(self.ForeignKey)
                    self.frame1.destroy()
                    messagebox.showinfo('Welcome Back',f'Your Logged in as {username}')
                    self.__Files()
                    authenticated=True
          if authenticated==False:
                    Label(self.frame1,text="Your USERNAME or PASSWORD is INCORRECT!!!",font=('Arial',16)).pack(pady=(10,0))

     def __Signup(self):
          self.frame1.destroy()
          self.username=StringVar(self.root)
          self.passwd=StringVar(self.root)
          self.frame2=Frame(self.root)
          self.frame2.pack(side='top',expand=True,fill='both')
          Label(self.frame2,fg='black',text='MGCloud',font=('Arial',30,'bold')).pack(pady=30)
          Label(self.frame2,fg='black',text='Signup',font=('Arial',30)).pack(pady=20)
          Label(self.frame2,text='Username.: ',font=('Arial',16)).pack(padx=(0,260))
          self.inp1=Entry(self.frame2,font=('Arial',25),textvariable=self.username).pack()
          Label(self.frame2,text='Password.: ',font=('Arial',16)).pack(padx=(0,260))
          self.inp2=Entry(self.frame2,font=('Arial',25),show='*',textvariable=self.pwd).pack()
          Label(self.frame2,text='Re-Enter Password.: ',font=('Arial',16)).pack(padx=(0,170))
          self.inp3=Entry(self.frame2,font=('Arial',25),show='*',textvariable=self.passwd).pack()
          self.sub_btn=Button(self.frame2,text="Submit",font=('Arial',20),command=self.__Create_user).pack(pady=(20,10))
          Label(self.frame2,text="Already have an account?? SignIn").pack()
          self.sub_btn=Button(self.frame2,text="SignIn",font=('Arial',20),command=self.__Signin).pack()

     def __Signin(self):
          self.frame2.destroy()
          self.frame1=Frame(self.root)
          self.frame1.pack()
          Label(self.frame1,text="MGCloud",fg="black",font=('Arial',30,'bold')).pack(pady=(30,0))
          Label(self.frame1,text="Sign In",fg="black",font=('Arial',25)).pack(pady=(20,0))
          Label(self.frame1,text='Username.: ',font=('Arial',16)).pack(padx=(0,260))
          self.inp1=Entry(self.frame1,text="Username",font=('Arial',25),textvariable=self.uname).pack()
          Label(self.frame1,text='Password.: ',font=('Arial',16)).pack(padx=(0,260))
          self.inp2=Entry(self.frame1,text="password",font=('Arial',25),show='*',textvariable=self.pwd).pack(pady=(10,0))
          self.btn=Button(self.frame1,text="Submit",font=('Arial',15),command=self.__Login).pack(pady=(60,10))
          Label(self.frame1,text="Don't have an account?? SignUp").pack()
          self.btn2=Button(self.frame1,text="SignUp",font=('Arial',15),command=self.__Signup).pack(ipadx=10,ipady=10)

     def __Create_user(self):
          reg_url='http://127.0.0.1:8000/accounts/'
          resp=requests.post(reg_url,{"username":self.username.get(),"password":self.passwd.get()}).json()
          self.ForeignKey=resp['foreign_key']
          print(self.ForeignKey)
          print('User Created')
     
     def __Files(self):
          self.__Upload_backup
          self.frame2=Frame(self.root)
          self.frame2.pack(side='top',expand=True,fill='both')
          self.files_url='http://127.0.0.1:8000/userfiles/'
          files=requests.get(self.files_url+str(self.ForeignKey)).json()
          self.file_data=files['data']
          Label(self.frame2,text='MGCloud',font=('Verdana',32,'bold')).pack(pady=(30,0))
          Label(self.frame2,text='Your Files in MGCloud',font=('Verdana',25)).pack(pady=(10,0))
          Button(self.frame2,text="Upload",font=('Arial',15),command=self.__Upload).pack(pady=(0,20),ipadx=10,ipady=10)
          self.LB=Listbox(self.frame2,width=30,height=10,activestyle='dotbox',font=('Arial',25))
          self.LB.pack()
          for i in self.file_data:
               print(i['file'])
               filename=i['file'].split('/')
               self.LB.insert(1,filename[1])
          Button(self.frame2,text="Delete",command=self.__Delete,font=('Arial',15)).pack(pady=(0,10),ipadx=5,ipady=5)
          Button(self.frame2,text="Download",command=self.__Download,font=('Arial',15)).pack(ipadx=5,ipady=5)
          Button(self.frame2,text="SignOut",command=self.__Login,font=('Arial',15)).pack(ipadx=5,ipady=5)

     def __Upload_backup(self):
          if Connection_status():
               f=os.getcwd().replace('\\','/') + '/' + 'BacklogFiles/'
               if os.path.exists(f):
                    print('Checking for Backlog files...')
                    filedir = os.listdir(f)
                    if len(filedir) > 0:
                         print(len(fildir),' Backlog File(s) Found')
                         for i in filedir:
                              print(i)
                              filepath = f+i
                              up_api='http://127.0.0.1:8000/cloud/'
                              file = open(filepath,'rb')
                              send = requests.post(up_api,data={'foreign_key':self.ForeignKey},files={'file':file})
                              resp=send.text
                              print(resp)
                              file.close()
                              os.remove(filepath)
                              print('Uploaded' + filepath)
                    else:
                         print('No backup files')

               else:
                    os.mkdir(f)
                    print('Backlog Files dir was not found, so it was created')
                    self.__Upload
          else:
               print("no internet")
               self.__Upload

          
          
     def __Upload(self):
          filetypes=(('text files','*.txt'),('All files','*.*'))
          file_path=filedialog.askopenfilename(title='Open File',initialdir='/',filetype=filetypes)
          messagebox.showinfo('File Path',f'{file_path}')
          filename=file_path.split('/')
          filename=filename[len(filename)-1]
          if Connection_status():
               file=open(r''+file_path,'rb')
               up_api='http://127.0.0.1:8000/cloud/'
               send = requests.post(up_api,data={'foreign_key':self.ForeignKey},files={'file':file})
               if send.status_code==200:
                    messagebox.showinfo('Upload Success!!','File Uploaded to MGCloud')
                    print("File Uploaded Succesfully ", send.text)
                    self.LB.insert(1,filename)
                    self.__Files()
               else:
                    print('file upload err')
          else:
               print(' NO INTERNET !!! ')
               th=file_path.split('/')
               a=shutil.copyfile(file_path,f+th[len(th)-1])
               messagebox.showinfo('Copied Locally','You file is copied locally')
               print(a)
               print('File Uploaded locally')
          
          
     def __Download(self):
          file_name=self.LB.get('active')
          for i in self.file_data:
               if file_name in i['file']:
                    print(i['id'])
                    ref_id=i['id']
          download_url='http://127.0.0.1:8000/cloud/'
          file_bin=requests.get(download_url+str(ref_id)).content
          with open('D:\\'+file_name,'wb') as file:
               file.write(file_bin)

          messagebox.showinfo('Download Sucess!!',f'{file_name} downloaded. Saved at D:\\{file_name}')
          
     def __Delete(self):
          file_name=self.LB.get('active')
          for i in self.file_data:
               if file_name in i['file']:
                    ref_id=i['id']
          del_url='http://127.0.0.1:8000/cloud/'
          send = requests.delete(del_url+str(ref_id))
          ind=self.LB.get(0,END).index(file_name)
          self.LB.delete(ind)
          print(send.status_code)
          print('deleting',ref_id)
app()

