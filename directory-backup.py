import os
import shutil
from datetime import datetime
import time

def setup():
    direct = input("Enter the name of the directory you would like to backup\n")

    try:
        # handle invalid directory
        if not os.path.exists(direct):
            print('Directory not located, make sure the directory you would like to backup is contained in'
            ' the same folder as this script.')
            raise NotADirectoryError
    except NotADirectoryError:
        setup()
        return        

    if not os.path.exists("Backups"):
        os.makedirs("Backups")

    data = open('Backups/backup-info.txt', 'w')
    data.write('directory={}\n'.format(direct))

    # handle non integer backup interval
    while True:
        try:
            interval = int(input("Enter how frequently you would like the directory to"
            " be backed up (hours).\n"))
            break
        except ValueError:
            print('Invalid interval, please enter an integer amount.')

    data.write('interval={}\nbackup_number=0\n'.format(interval))

    # handle non integer backup quantity
    while True:
        try:
            nm_saved = int(input("Enter how many backups you would like to save at a time.\n"))
            break
        except ValueError:
            print('Invalid response, please enter an integer amount.')

    data.write('quantity_saved={}'.format(nm_saved))
    data.close()
    print("Settings saved to 'Backups/backup-info.txt'. These can be changed at any time.")


def backup():
    while True:
        # handle missing backup-info text file
        try:
            load = open("Backups/backup-info.txt", 'r')
        except FileNotFoundError:
            print("'backup-info.txt' not found, please re-enter backup information.")
            setup()
            continue
        
        # gather data and make it interpretable -- IndexError handles missing info in txt file
        try:
            backup_info = load.readlines()
            direct = backup_info[0].replace('directory=','').replace('\n','')
            interval = int(backup_info[1].replace('interval=','').replace('\n',''))
            backup_nm = int(backup_info[2].replace('backup_number=','').replace('\n',''))
            quantity = int(backup_info[3].replace('quantity_saved=',''))
            load.close()
        except IndexError:
            print("Information missing from 'backup-info.txt'. Please re-enter backup information.")
            setup()
            continue
        
        # create backup, check for name collision
        try:
            shutil.copytree(direct, "Backups/{}{}".format(direct, backup_nm+1))
            time_copied = datetime.now().strftime("%H:%M:%S")
            print("[{0}]: {1} was backed up to Backups/{1}{2}".format(time_copied, direct, backup_nm+1))
        except FileExistsError:
            print('Backup #{} of {} exists'.format(backup_nm+1, direct))
            backup_info[2] = backup_info[2].replace(str(backup_nm), str(backup_nm + 1))
            replace = open("Backups/backup-info.txt", "w")
            replace.writelines(backup_info)
            replace.close()
            continue
        except FileNotFoundError:
            print('Directory not found. Please re-enter backup information.')
            setup()
            continue
        
        # maintain backup quantity
        if backup_nm + 1 > quantity and os.path.exists("Backups/{}{}".format(direct, backup_nm + 1 - quantity)):
            shutil.rmtree("Backups/{}{}".format(direct, backup_nm + 1 - quantity))
            time_removed = datetime.now().strftime("%H:%M:%S")
            print("[{}]: {}{} was removed from Backups folder.".format(time_removed, direct, backup_nm + 1 - quantity))

        # update backup-info.txt
        backup_info[2] = backup_info[2].replace(str(backup_nm), str(backup_nm + 1))
        replace = open("Backups/backup-info.txt", "w")
        replace.writelines(backup_info)
        replace.close()

        time.sleep(interval*3600)
  

if not os.path.exists("Backups"):
    setup()
backup()