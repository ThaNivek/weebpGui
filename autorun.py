import winreg as reg
import os

path = os.getcwd() + "\\AnimatedBackground.exe startup"

key = reg.HKEY_CURRENT_USER 
key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS) 
reg.SetValueEx(open,"Animation Background(Experimental on Windows Boot mode)",0,reg.REG_SZ,path) 
reg.CloseKey(open) 