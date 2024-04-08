import os
import hashlib
#import wget
import json
import requests

# for each patch check if it exists, if not download it
# if it exists, check if the checksum is correct
# if the checksum is correct, print 'checksum correct'
# if the checksum is incorrect, download the patch
# this could in theroy replace download_client_part_2_dropbox in the current Launcher.bat file
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
#create folder _Client\Data if it doesnt exist
if not os.path.exists('_Client\Data'):
    os.makedirs('_Client\Data')

def get_latest_patch_list():
    #get the latest patch list from the server
    url = 'https://raw.githubusercontent.com/Shalkith/dinklepack_client_patcher/main/patch_list.json'
    r = requests.get(url)
    with open('patch_list.json', 'wb') as f:
        f.write(r.content)

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    pass

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
    # using the wget.exe file to download the patch like the current launcher.bat file does
    # for example: _Tools\wget.exe -k --no-check-certificate --show-progress --content-disposition --directory-prefix=.\_Client\Data\ -c "https://www.dropbox.com/sh/7wto7lnj635qjws/AAC_-aNGG-swSXJZ-uFg1M46a/patch-8.mpq"
    url = patch['downloadurl_1']
    filename = patch['filename']
    os.system('_Tools\wget.exe -k --no-check-certificate --show-progress --content-disposition --directory-prefix=.\_Client\Data\ -c "{}"'.format(url))
    
    

def print_program_banner():
    remove_temp_files()
    clear()
    # Dinkledork Patch Downloader
    print('''
      ____  _       __   __     ____             __  
     / __ \(_)___  / /__/ /__  / __ \____  _____/ /__
    / / / / / __ \/ //_/ / _ \/ /_/ / __ `/ ___/ //_/
   / /_/ / / / / / ,( / /  __/ ____/ /_/ / /__/ ,(   
  /_____/_/_/ /_/_/\_/_/\___/_/    \__,_/\___/_/\_\  v13.0
   Dinkledork @ https://www.patreon.com/Dinklepack5
''')
 # print('Dinkledork Patch Downloader')
    print('By Shalkith')

def announcement():
    print('''
__________________________Downloading Dinklepack Client Patches__________________________

If you get any "unspecified" files when downloading, then try again after 24 hours, as 
the links get disabled for 24 hours by Dropbox when they reach a certain unknown limit.

If it still doesn't work, after waiting, then something on your PC is preventing the 
launcher from downloading the files and I can't do anything about that, unfortunately.''')

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
            try:
                download_patch(patch)
            except Exception as e:
                print('Error downloading file: {}'.format(e))
                input('Press Enter to exit' )
    else:
        print('File does not exist - downloading...')
        try:
            download_patch(patch)
        except Exception as e:
            print('Error downloading file: {}'.format(e))
            input('Press Enter to exit' )
        

def main():
    get_latest_patch_list()
    jsonfilename = 'patch_list.json'

    with open(jsonfilename, 'r') as f:
        data = json.load(f)

    for key in data:
        print_program_banner()
        announcement()
        print()
        print(data[key]['filename'])
        check_patch(data[key])
        print('')
        clear()

    print('All patches checked and downloaded if needed')

if __name__ == '__main__':

    main()
    input('Press Enter to exit')
    clear()
    os.remove('patch_list.json')
    exit()