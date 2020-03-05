#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from COC.COC_GUI import *
from COC.GUI.GUI_util import GUI_Tools as G


class Emulator(tk.Frame):

    def __init__(self, devices,root, *args, **kwargs):
        #--------------------Windows-----------------------------------------
        self.window = tk.Tk()
        tk.Frame.__init__(self, self.window, *args, **kwargs)

        n = len(devices)
        self.d = StringVar()

        self.window.title("Select A Emulator")
        self.window.geometry("420x" + str(n*30))
        self.window.resizable(width = False, height = False)
        GUI_Tools.set_close(self.window)
        
        def set_devices(pid = -1):
            self.window.destroy()
            root.d = self.d.get()
            root.pid = pid

        emu_row = 0
        for i in range(n):
            name = devices[i]
            if 'emulator' in name:
                emu_row = i
                tk.Radiobutton(self.window, text=name, value=name, var=self.d ,width = 20).grid(row=i,column=0)
                #Label(text = , relief=tk.RIDGE, width=20).grid(row=i,column=0)
                if self.d.get() == '':
                    self.d.set(name)
            else:
                tk.Label(text = "Android " + str(i + 1), width=20).grid(row=i,column=0)
                tk.Button(self.window, text = name ,anchor = "ne" ,width = 20, command = set_devices).grid(row=i,column=1)
        
        #--------------------Emulator-------------------------------------------- 
        emu = self.find_emulator()
        for i in range(len(emu)):
            tk.Button(self.window, text = emu[i][0] ,anchor = "ne" ,width = 20, command = lambda pid=emu[i][2]:set_devices(pid = pid) ).grid(row=emu_row + i,column=1)


    def start(self):
        self.window.mainloop()


    def find_emulator(self):
        global Win

        devices = list()
        Emulator = {'dnplayer.exe':'雷电模拟器',
                    'NemuPlayer':'MacOs网易MuMu',
                    'BlueStacks':'蓝叠'
                    }
        # show processes info
        pids = psutil.pids()
        try:
            for pid in pids:
                p = psutil.Process(pid)# get process name according to pid
                process_name = p.name()
                if process_name in Emulator.keys():
                    if Win:
                        handle  = p.num_handles()
                        print("Process name is: %s, pid is: %s, num of handles : %s" %(process_name, pid, handle))
                        devices.append([Emulator[process_name],process_name,handle])
                    else:
                        print("Process name is: %s, pid is: %s" %(process_name, pid))
                        devices.append([Emulator[process_name],process_name,pid])
        except Exception as e:
            pass

        return devices