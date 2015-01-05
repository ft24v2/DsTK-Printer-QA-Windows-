#################################
#                               #
# Printer Import/Export Script  #
#     By Team Crypto 2014       #
#      Developed for CRC        #
#                               #
#################################


from thread import start_new_thread
import win32gui, win32con
import re
import threading
from threading import Thread
import sys, time, shutil, os, subprocess
from subprocess import Popen
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
                 
class FilePicker(QtGui.QWidget):
      
    #Actions that Occur on Startup    
    def __init__(self):
        
        # Create Gui for Application
        QtGui.QMainWindow.__init__(self)        
        self.setWindowTitle('Printer Migration Utility 1.1')
        
        # Set the window dimensions
        self.resize(320,120)
        
        # Set Layout for Application
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # Create a label which displays the path to our chosen file
        self.lbl = QtGui.QLabel('Select a Printer Backup File to Restore')
        self.lbl.setAlignment(Qt.AlignCenter)

        self.vbox.addWidget(self.lbl)

        # Create a push button labelled 'choose' and add it to our layout
        backupbtn = QtGui.QPushButton('Backup Printers', self)
        self.vbox.addWidget(backupbtn)
        btn = QtGui.QPushButton('Restore Printers', self)
        self.vbox.addWidget(btn)

        # Connect the clicked signal to the get_fname handler                      
        self.connect(btn, QtCore.SIGNAL('clicked()'), self.restore)
        self.connect(backupbtn, QtCore.SIGNAL('clicked()'), self.backup)
   
    
    def bprinters(self):
        backup = """
        set usr=%USERNAME% &rem
        set usr=%usr: =%
        set hostname=%COMPUTERNAME% &rem
        set hostname=%hostname: =%
        DEL %usr%_%hostname%.printerExport
        %WINDIR%\System32\Spool\Tools\Printbrm -b -O FORCE -f %usr%_%hostname%.printerExport
        """
        f = open('C:/Windows/Temp/backupp.bat','w')
        f.write(backup)
        f.close() 

        # Code to make stupid window invisible... hopefully        
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = win32con.SW_HIDE
        
        p = subprocess.Popen('C:/Windows/Temp/backupp.bat', startupinfo = info)# 'C:/Windows/Temp/backupp.bat'
        stdout, stderr = p.communicate()
        print "good"
        self.lbl.setText("Printer Backup Completed!!!")
        self.lbl.setAlignment(Qt.AlignCenter)


    def backup(self):
        self.lbl.setText("Backing Up Printers, Please Wait...")
        self.lbl.setAlignment(Qt.AlignCenter)
        t = threading.Thread(target=self.bprinters, args = ())
        t.start()

    def restore(self):
        self.lbl.setText("Restore in Progress, Please Wait...")
        self.lbl.setAlignment(Qt.AlignCenter)
        t = threading.Thread(target=self.get_fname, args = ())
        t.start()
    
        
                                   
    def get_fname(self):
        """
        Handler called when 'choose file' is clicked
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if fname:
            # Sets Status
            self.lbl.setText("Restoring Printers. Please Wait")
            self.lbl.setAlignment(Qt.AlignCenter)

            # Define Temp Folder and Copy Selected File to Temp
            dstroot = "C:/Windows/Temp/"
            srcfile = str(fname)
            regex = re.compile(r"\w+(.printerExport)")
            printre = regex.search(srcfile) 
            printfile = printre.group(0)            
            dstdir = dstroot + printfile               
            shutil.copy(srcfile, dstdir)

            #Final Path to Printer Backup File
            filepath = dstdir.replace("/", "\\")
            admintext = """
            @echo off
            CLS 
            ECHO.
            ECHO =============================
            ECHO Running Admin shell
            ECHO =============================

            :checkPrivileges 
            NET FILE 1>NUL 2>NUL
            if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges ) 

            :getPrivileges 
            if '%1'=='ELEV' (shift & goto gotPrivileges)  
            ECHO. 
            ECHO **************************************
            ECHO Invoking UAC for Privilege Escalation 
            ECHO **************************************

            setlocal DisableDelayedExpansion
            set "batchPath=%~0"
            setlocal EnableDelayedExpansion
            ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPrivileges.vbs" 
            ECHO UAC.ShellExecute "!batchPath!", "ELEV", "", "runas", 1 >> "%temp%\OEgetPrivileges.vbs" 
            "%temp%\OEgetPrivileges.vbs" 
            exit /B 

            :gotPrivileges 
            ::::::::::::::::::::::::::::
            ::START
            ::::::::::::::::::::::::::::
            setlocal & pushd .
            """
            command = "%WINDIR%\System32\Spool\Tools\Printbrm -r -O FORCE -P ALL -f {}".format(filepath)
                        
            f = open('C:/Windows/Temp/restorep.bat','w')
            f.write(admintext)
            f.write(command) 
            f.close() 

            # Code to make stupid window invisible... hopefully        
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = win32con.SW_HIDE
            
            p = subprocess.Popen('C:/Windows/Temp/restorep.bat', startupinfo = info)# 'C:/Windows/Temp/backupp.bat'
            stdout, stderr = p.communicate()
            print "good"
            self.lbl.setText("Restoration Executed.")
            self.lbl.setAlignment(Qt.AlignCenter)
                       
        else:
            self.lbl.setText('Select an Action')

# If the program is run directly or passed as an argument to the python
# interpreter then create a FilePicker instance and show it

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    gui = FilePicker()
    gui.show()
    app.setWindowIcon(QtGui.QIcon(resource_path('chalk.ico')))
    app.exec_()


