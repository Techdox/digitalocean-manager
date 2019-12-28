#Import Start
import digitalocean
from digitalocean import SSHKey
import os
from alive_progress import alive_bar
#Import End

#Gloabl Variables Start
USER = os.environ.get("USER")
API_SECRET = os.environ.get("TOKEN")
manager = digitalocean.Manager(token=API_SECRET)
my_droplets = manager.get_all_droplets()
keys = manager.get_all_sshkeys()
#Global Varibles End

#Functions Start
def dropletsList():
    for droplet in my_droplets:
        print(droplet, droplet.ip_address)
    input("Press [Enter] to return to the main screen")
    main()

def dropletsLog():
    with alive_bar() as bar:
        for droplet in my_droplets:
            print(f"Pulling logs for {droplet}")
            print(f" NAME: {droplet.name}, Public IP: {droplet.ip_address}, DROPLET STATUS: {droplet.status}", file=open("droplet_events.txt", "a"))
            bar()
    input("Press [Enter] to return to the main screen")

def dropletDelete():
    for droplet in my_droplets:
        print((droplet.id, droplet.name))
    delChoice = input("Enter in Droplet ID")
    for droplet in my_droplets:
        if droplet.name == delChoice:
            confirm = input(f"Do you want to delete {droplet.name}?: Y|N").lower()
            if confirm == 'y':
                print(f'Deleting {droplet.name}')
                droplet.destroy()
            else:
                main()
    

def main():
    print("""
----------------------
Digital Ocean Manager
----------------------   

[1] List All Droplets
[2] Export Droplet Logs
[3] Create Droplet
[4] Upload local SSH key to Digital Ocean
[5] Delete Droplet
    """)
    choice = input("Select from the menu: ")
    if choice == '1':
        dropletsList()
    elif choice == '2':
        dropletsLog()
    elif choice == '3':
        createDroplet()
    elif choice == '4':
        dropletSSHKey()
    elif choice == '5':
        dropletDelete()
    else:
        print(":(")

def dropletSSHKey():
    user_ssh_key = open(f'/home/{USER}/.ssh/id_rsa.pub').read()
    key = SSHKey(token=API_SECRET,
             name='archyDesktop',
             public_key=user_ssh_key)
    key.create()
    print("Key Created")
    input("Press [Enter] to return to the main screen")
    main()

def createDroplet():
    newDroplet = digitalocean.Droplet(token=API_SECRET,
    name='testserver',
    region='SGP1',
    image='ubuntu-14-04-x64',
    size_slug='512mb',
    ssh_keys=keys,
    backups=False)
    newDroplet.create()
    print(f"{newDroplet.name} Created. The IP Address for SSH Connection is: {newDroplet.ip_address}")
    input("Press [Enter] to return to the main screen")
    main()
#Functions End


if __name__ == "__main__":
    main()