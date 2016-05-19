# deprecated
import requests
import pymongo
import gridfs

connection = pymongo.MongoClient("127.0.0.1",27017)
db = connection["itjuzitest"]
collection = db["itjuzitest"]
fs = gridfs.GridFS(db)
img = requests.get("http://www.itjuzi.com/images/dc980995d9a0ce3ffb39ebef3bcb068e.png")
#write to file
#file = open('logo.png','wb')
#file.write(img.content)
fs.put(img.content,filename="logo.png")