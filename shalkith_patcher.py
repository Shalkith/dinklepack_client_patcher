import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#create folder _Client\Data if it doesnt exist
if not os.path.exists('_Client\Data'):
    os.makedirs('_Client\Data')

# for each patch check if it exists, if not download it
# if it exists, check if the checksum is correct
# if the checksum is correct, print 'checksum correct'
# if the checksum is incorrect, download the patch

import hashlib
import wget
import json
import requests

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def remove_temp_files():
    #rempve all files in the _Client\Data folder that end with .tmp
    for file in os.listdir('_Client\Data'):
        if file.endswith('.tmp'):
            os.remove('_Client\Data\\'+file)


def get_checksum(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()  # to get a printable str instead of bytes

def download_patch(patch):
    url = patch['downloadurl_2']
    filename = patch['filename']
    downloadto = '_Client\Data\{}'.format(filename)
    #requests.get(url)
    wget.download(url, out=downloadto)
    
    
def print_program_banner():
    remove_temp_files()
    clear()
    # Dinkledork Patch Downloader
    print('''
┳┓•  ┓ ┓   ┓    ┓   ┏┓    ┓   ┳┓       ┓     ┓    
┃┃┓┏┓┃┏┃┏┓┏┫┏┓┏┓┃┏  ┃┃┏┓╋┏┣┓  ┃┃┏┓┓┏┏┏┓┃┏┓┏┓┏┫┏┓┏┓
┻┛┗┛┗┛┗┗┗ ┗┻┗┛┛ ┛┗  ┣┛┗┻┗┗┛┗  ┻┛┗┛┗┻┛┛┗┗┗┛┗┻┗┻┗ ┛ 
''')
 # print('Dinkledork Patch Downloader')
    print('By Shalkith')
    
def del_file(filename):
    try:
        os.remove(filename)
    except:
        print('Error deleting file: {}'.format(filename))

def check_patch(patch):
    filename = patch['filename']
    checksum = patch['checksum']
    if os.path.exists('_Client\Data\\'+filename):
        print('file exists, checking checksum...')
        if checksum == get_checksum('_Client\Data\\'+filename):
            print('Checksum correct - File is good to go!')
        else:
            print('Checksum incorrect - downloading new file...')
            del_file('_Client\Data\\'+filename)            
            download_patch(patch)
    else:
        print('File does not exist - downloading...')
        download_patch(patch)

jsonfilename = 'patch_list.json'
with open(jsonfilename, 'r') as f:
    data = json.load(f)

print_program_banner()

for key in data:
    #print(key)
    print()
    print(data[key]['filename'])
    check_patch(data[key])
    print('')

remove_temp_files()
print('All patches checked and downloaded if needed')