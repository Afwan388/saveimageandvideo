from pymongo import MongoClient
import os
import gridfs
import requests
from os.path import join, dirname
from dotenv import load_dotenv

# Koneksi ke MongoDB Atlas
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def save_file_to_mongodb(file_url, file_name):
    # Dapatkan konten dari URL
    response = requests.get(file_url)
    file_data = response.content
    
    # Gunakan GridFS untuk menyimpan file
    fs = gridfs.GridFS(db)
    file_id = fs.put(file_data, filename=file_name)
    
    return file_id

def get_file_from_mongodb(file_id):
    fs = gridfs.GridFS(db)
    file_data = fs.get(file_id).read()
    return file_data

# Contoh penggunaan
file_url_image = 'https://example.com/path/to/your/image.jpg'
file_url_video = 'https://example.com/path/to/your/video.mp4'

image_id = save_file_to_mongodb(file_url_image, 'image.jpg')
video_id = save_file_to_mongodb(file_url_video, 'video.mp4')

print(f'Image stored with ID: {image_id}')
print(f'Video stored with ID: {video_id}')

# Mengambil dan menyimpan file yang diambil ke disk (opsional)
stored_image_data = get_file_from_mongodb(image_id)
stored_video_data = get_file_from_mongodb(video_id)

with open('retrieved_image.jpg', 'wb') as image_file:
    image_file.write(stored_image_data)

with open('retrieved_video.mp4', 'wb') as video_file:
    video_file.write(stored_video_data)
