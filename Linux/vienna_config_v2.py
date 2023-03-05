#import modules
import os, sys, shutil 
import subprocess

sys.stdout = open("tempoutput.txt","w")
#Find the executable
find_exe = shutil.which("RNAfold")

#Remove the comment for debugging
#print os.path.dirname(find_exe)

#Get the directory of executable
exe_path = os.path.dirname(find_exe)



#Check if directory is in PATH
if os.path.isdir(exe_path) == True:
   print ("ViennaRNA - RNAfold..........ok")
   
else:
   sys.path.insert(0, exe_path)
   print ("ViennaRNA - RNAfold..........added")

#Check if ghostscript is installed
find_gs = shutil.which("gs")
gs_path = os.path.dirname(find_gs)

if gs_path is not None:
   print ("Ghostscript.................ok")
   
else:
   print ("Ghostscript not found, try\n\nsudo apt install ghostscript")
   sys.exit()

#Check is modules are installed
try:
   import tkinter
   import PIL
except ModuleNotFoundError as msg:
   print (msg)
   sys.exit()   
   
   
#Create tmp directory if it does not exist
current_path = os.getcwd()
temp_dir = "tmp"
new_path = os.path.join(current_path, temp_dir)

if os.path.isdir(new_path) == False:
   os.mkdir(new_path)
   print ("tmp directory...........created")
   os.chdir(new_path)
   
else:
   print("tmp directory............ok")
   os.chdir(new_path)

sys.stdout.flush()
os.fsync(sys.stdout.fileno())

