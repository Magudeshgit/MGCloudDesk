import mysql.connector as mysql
import requests

dbs, password  = 'mgcloud','magudeshsql'
conn = mysql.connect(host='localhost',user='root',passwd=password,db=dbs)
api = 'https://mghcloudapi.up.railway.app/cloud/'
cur=conn.cursor()

def Authenticate(user,passwd):
     global username
     username=user
     auth=False
     cur.execute('Select * from auth')
     for i in cur.fetchall():
          print(i)
          if user and passwd in i:
               print('Authenticated')
               auth=True
               return auth
     return auth
     
def Create(user,password):
     a=cur.execute("insert into auth(Username,password) values('{}','{}')".format(user,password))
     conn.commit()
     return True

def Save(username,ref_id,file_name):
     a=cur.execute("insert into files values('{}',{},'{}')".format(username,ref_id,file_name))
     conn.commit()
     return True

def Connection_status():
     try:
          req=requests.get(api)
          if req.status_code==200:
               return True
     except (requests.ConnectionError, requests.Timeout) as exceptions:
          print("No Internet")
          print('''You can still upload files!!!, your files will be stored locally and
               uploaded to cloud once internet is available...''')
          print("Initiating File Upload Protocol")
          return False
     
def fetch_data(user):
     cmd=cur.execute('Select * from files where UserID="{}"'.format(user))
     data=cur.fetchall()
     return data

def delete(ref_id):
     send = requests.delete(api+str(ref_id))
     print(send.status_code)
     cmd=cur.execute('delete from files where DBID={}'.format(ref_id))
     conn.commit()
     return True

def download(ref_id,file_name):
     recv = requests.get(api+str(ref_id)).content
     with open('D:\\'+file_name,'wb') as file:
          file.write(recv)
     return True
     
     
     
     


