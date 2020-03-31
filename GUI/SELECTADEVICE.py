#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import os

class DEVICE(tk.Frame):

    def __init__(self, config, *args, **kwargs):
        #--------------------Windows-----------------------------------------
        self.window = tk.Tk()
        tk.Frame.__init__(self, self.window, *args, **kwargs)
        self.config = config

        self.window.title("Select A Devices")
        self.window.resizable(width = False, height = False)

        # ADB find connect devices
        self.devices = self.get_devices()

        def set_devices(i):
            self.window.destroy()
            self.config['device'] =  self.devices[i]


        n = len(self.devices)

        if not n > 0:
            messagebox.showinfo("Didn't find a device", "Please enable the development mode for Android \n or using an emulator")
            exit()

        for i in range(n):
            tk.Button(self.window, text = self.devices[i] ,anchor = "ne" ,width = 20,
             command = lambda id=i:set_devices(id) ).grid(row=i,column=0)
        
        self.window.geometry("200x" + str(n*30))

    def start(self):
        self.window.mainloop()


    def get_devices(self):
        #restart = 'adb/adb kill-server && adb/adb start-server'
        #os.system(restart)

        get_devices = 'adb/adb devices'
        stream = os.popen(get_devices)

        devices_adb = stream.read()
        #devices_adb = devices_adb.decode("utf-8")
        devices_adb = devices_adb.replace("List of devices attached","")
        devices_adb = devices_adb.strip().split()

        #port=os.system('netstat -aon|findstr "555"')#25端口号
        #out=os.system('tasklist|findstr "3316"')#3316进是程

        print("Found Device:")
        devices = list()
        for i in range(0,len(devices_adb),2):
            if devices_adb[i + 1] != "offline":
                devices.append( devices_adb[i] )
                print(devices_adb[i])

        return devices