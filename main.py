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
        print(droplet)

def dropletsLog():
    with alive_bar() as bar:
        for droplet in my_droplets:
            print(f"Pulling logs for {droplet}")
            print(f" NAME: {droplet.name}, Public IP: {droplet.ip_address}, DROPLET STATUS: {droplet.status}", file=open("droplet_events.txt", "a"))
            bar()

def main():
    print("""
----------------------
Digital Ocean Manager
----------------------   

[1] List All Droplets
[2] Export Droplet Logs
[3] Create Droplet
[4] Upload local SSH key to Digital Ocean
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
    else:
        print(":(")

def dropletSSHKey():
    user_ssh_key = open(f'/home/{USER}/.ssh/id_rsa.pub').read()
    key = SSHKey(token=API_SECRET,
             name='archyDesktop',
             public_key=user_ssh_key)
    key.create()
    print("Key Created")

def createDroplet():
    newDroplet = digitalocean.Droplet(token=API_SECRET,
    name='testserver',
    region='SGP1',
    image='ubuntu-14-04-x64',
    size_slug='512mb',
    ssh_keys=keys,
    backups=False)

    newDroplet.create()
#Functions End


if __name__ == "__main__":
    main()