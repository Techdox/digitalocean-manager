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
images = manager.get_global_images()


#Global Varibles End

#Functions Start

def dropletsListImages():
    for image in images:
        print(image.slug)
    input("Press [Enter] to return to the main screen")
    main()

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
    main()

def dropletDelete():
    for droplet in my_droplets:
        print((droplet.id, droplet.name))
    delChoice = input("Enter in Droplet name: ")
    for droplet in my_droplets:
        if droplet.name == delChoice:
            confirm = input(f"Do you want to delete {droplet.name}?: Y|N").lower()
            if confirm == 'y':
                print(f'Deleting {droplet.name}')
                droplet.destroy()
                my_droplets.remove(droplet)
                main()
            else:
                main()
    

def main():
    print("""
----------------------
Digital Ocean Manager
----------------------   

[1] List all Droplets
[2] List all Droplet images
[3] Create Droplet
[4] Delete Droplet
[5] Upload local SSH key to Digital Ocean
[6] Export Droplet Logs

    """)
    choice = input("Select from the menu: ")
    if choice == '1':
        dropletsList()
    elif choice == '2':
        dropletsListImages()
    elif choice == '3':
        dropletCreate()
    elif choice == '4':
        dropletDelete()
    elif choice == '5':
        dropletSSHKey()
    elif choice == '6':
        dropletsLog()
    else:
        print("Invalid choice!")
        main()

def dropletSSHKey():
    user_ssh_key = open(f'/home/{USER}/.ssh/id_rsa.pub').read()
    key = SSHKey(token=API_SECRET,
             name='archyDesktop',
             public_key=user_ssh_key)
    key.create()
    print("Key Created")
    input("Press [Enter] to return to the main screen")
    main()

def dropletCreate():
    dropletName = input("Enter in your droplet name: (No spaces of underscores) ")
    dropletRegion = input("Enter in droplet region: ")
    dropletImage = input("Enter in droplet image: ")
    dropletSize = input("Enter in droplet Size: ")
    newDroplet = digitalocean.Droplet(token=API_SECRET,
    name=dropletName,
    region=dropletRegion,
    image=dropletImage,
    size_slug=dropletSize,
    ssh_keys=keys,
    backups=False)
    newDroplet.create()
    my_droplets.append(newDroplet)
    print(f"{newDroplet.name} Created. The IP Address for SSH Connection is: {newDroplet.ip_address}")
    input("Press [Enter] to return to the main screen")
    main()
#Functions End


if __name__ == "__main__":
    main()