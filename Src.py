import os, shutil
import requests as r
from Util import Authenticate, Create, Save

api = 'https://mghcloudapi.up.railway.app/cloud/'
status=False

#user=input("Enter Username.: ")

#password=input("Enter Password.: ")
def init(username,passwd):
        if Authenticate(username,passwd):
                try:
                        req=r.get(api)
                        if req.status_code==200:
                                status=True
                                print("Internet Connected!!!")
                except (r.ConnectionError, r.Timeout) as exceptions:
                        print("No Internet")
                        print('''You can still upload files!!!, your files will be stored locally and
                               uploaded to cloud once internet is available...''')
                        print("Initiating File Upload Protocol")

                def initiate():
                        f=os.getcwd().replace('\\','/') + '/' + 'BacklogFiles/'
                        if os.path.exists(f):
                                print('Checking for Backlog files...')
                                filedir = os.listdir(f)
                                if len(filedir) > 0:
                                        print(len(fildir),' Backlog File(s) Found')
                                        for i in filedir:
                                                print(i)
                                                filepath = f+i
                                                file = open(filepath,'rb')
                                                send = r.post(api,files={'file':file})
                                                resp=send.text
                                                print(resp)
                                                file.close()
                                                os.remove(filepath)
                                                print('Uploaded' + filepath)
                                        Upload_files()
                                else:
                                        Upload_files()
                        else:
                                os.mkdir(f)
                                print('Backlog Files dir was not found, so it was created')
                                Upload_files()
                def Upload_files(f_path):
                        f=os.getcwd().replace('\\','/') + '/' + 'BacklogFiles/'
                        path=f_path
                        filename=path.split("\\")
                        length=len(filename)
                        filename=filename[length-1]
                        if status==True:
                             file=open(r''+path,'rb')
                             send = r.post(api,files={'file':file})
                             if send.status_code==200:
                                  print("File Uploaded Succesfully ", send.text)
                                  global apidata
                                  apidata = send.json()
                                  ref_id=apidata['id']
                                  print(ref_id,filename)
                                  Save(ref_id,filename)
                                  print(apidata,type(apidata))
                                  
                                  
                             else:
                                  print('Error uploading file')
                        else:
                             print(' NO INTERNET !!! ')
                             th=path.split('/')
                             a=shutil.copyfile(path,f+th[len(th)-1])
                             print(a)
                             print('File Uploaded locally')

                        if status==True:
                                initiate()
                        else:
                                #print(''' || No Internet || will be uploaded locally, and once there is internet connection it will uploaded to cloud :)''')
                                Upload_files()
        else:
                print("Acces Denied")
        












# kl=open(r'D:\CS_Project\RESTAPI\Fileapi\requirements.txt','rb')
# send = requests.delete('http://127.0.0.1:8000/cloud/3/')
# #send = requests.post(link,files={'file':kl})

# #send = requests.get('https://web-production-e7c7.up.railway.app/cloud/15')
# print(send)
# print(send.text)
