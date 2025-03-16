from cloud_manager import CloudManager
cloud = CloudManager('cloud.o2online.es', 'user@gmail.com', 'xxxxxx')
# Movistar Cloud -> micloud.movistar.es
# Zefiro -> zefiro.me
# O2 Cloud -> cloud.o2online.es

folders = cloud.get_folders()
print(folders)

files = cloud.list_folder_files(999999)
print(files)

upload_response = cloud.upload_file("test.txt", 99999)
print(upload_response)

download_path = cloud.download_file(99999999, "/local/path")
print(download_path)