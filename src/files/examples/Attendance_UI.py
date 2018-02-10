import wx
import time
import  wx.gizmos   as  gizmos
import manage_db
from pyfingerprint.pyfingerprint import PyFingerprint
import array
import Fingerprint_Controller



########################################################################
class EmailVerified(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self,parent):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Secondary Frame")
        panel = wx.Panel(self)
        self.ShowFullScreen(True)
        self.frame = parent

        heading = wx.StaticText(self, -1, label="RMUTK ATTENDANCE", pos=(110, 20))
        headingFont = wx.Font(40, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        heading.SetFont(headingFont)

        title1 = wx.StaticText(self, -1, label="Your can get activated code from ", pos=(70, 100))
        title1Font = wx.Font(30, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title1.SetFont(title1Font)

        title2 = wx.StaticText(self, -1, label="RMUTK attendance website", pos=(140, 160))
        title2Font = wx.Font(30, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title2.SetFont(title2Font)

        self.txt = wx.TextCtrl(self, -1,pos=(279,240), size=(140, -1))

        zeroBtn = wx.Button(self, label="0", pos=(120, 300), size=(70, -1))
        zeroBtn.Bind(wx.EVT_BUTTON, self.zeroPad)

        oneBtn = wx.Button(self, label="1", pos=(200, 300), size=(70, -1))
        oneBtn.Bind(wx.EVT_BUTTON, self.onePad)

        twoBtn = wx.Button(self, label="2", pos=(280, 300), size=(70, -1))
        twoBtn.Bind(wx.EVT_BUTTON, self.twoPad)

        threeBtn = wx.Button(self, label="3", pos=(360, 300), size=(70, -1))
        threeBtn.Bind(wx.EVT_BUTTON, self.threePad)

        fourBtn = wx.Button(self, label="4", pos=(440, 300), size=(70, -1))
        fourBtn.Bind(wx.EVT_BUTTON, self.fourPad)

        fiveBtn = wx.Button(self, label="5", pos=(520, 300), size=(70, -1))
        fiveBtn.Bind(wx.EVT_BUTTON, self.fivePad)

        sixBtn = wx.Button(self, label="6", pos=(120, 350), size=(70, -1))
        sixBtn.Bind(wx.EVT_BUTTON, self.sixPad)

        sevenBtn = wx.Button(self, label="7", pos=(200, 350), size=(70, -1))
        sevenBtn.Bind(wx.EVT_BUTTON, self.sevenPad)

        eightBtn = wx.Button(self, label="8", pos=(280, 350), size=(70, -1))
        eightBtn.Bind(wx.EVT_BUTTON, self.eightPad)

        nineBtn = wx.Button(self, label="9", pos=(360, 350), size=(70, -1))
        nineBtn.Bind(wx.EVT_BUTTON, self.ninePad)

        tenBtn = wx.Button(self, label="0", pos=(440, 350), size=(70, -1))
        tenBtn.Bind(wx.EVT_BUTTON, self.zeroPad)

        delBtn = wx.Button(self, label="reset", pos=(520, 350), size=(70, -1))
        delBtn.Bind(wx.EVT_BUTTON, self.resetPad)

        insertFingerBtn = wx.Button(self, label="Submit", pos=(250, 420))
        insertFingerBtn.Bind(wx.EVT_BUTTON, self.newInsertFingerFrame)


        returnBtn = wx.Button(self, label="Return", pos=(400, 420))
        returnBtn.Bind(wx.EVT_BUTTON, self.newMainFrame)


    # ----------------------------------------------------------------------
    def zeroPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '0')

    def onePad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '1')

    def twoPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '2')

    def threePad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '3')

    def fourPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '4')

    def fivePad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '5')

    def sixPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '6')

    def sevenPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '7')

    def eightPad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '8')

    def ninePad(self,evt):
        self.txt.SetValue(str(self.txt.GetValue()) + '9')

    def resetPad(self,evt):
        self.txt.SetValue("")

    def newMainFrame(self, event):
        """
        Close insert frame and open main frame
        """
        # msg = self.msgTxt.GetValue()
        # # Publisher().sendMessage(("show.mainframe"), msg)
        # self.Close()

        self.Hide()
        new_frame = MainFrame()
        new_frame.Show()
        self.Destroy()

    def newInsertFingerFrame(self, event):
        """
        Close insert frame and open main frame
        """
        # msg = self.msgTxt.GetValue()
        # # Publisher().sendMessage(("show.mainframe"), msg)
        # self.Close()
        user = manage_db.getUserByAcCode(self.txt.GetValue())
        if(user == None):
            dlg = wx.MessageDialog(self, "No user found! Please try again", "Error", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        if(user != None):
            dlg = wx.MessageDialog(self, "Authentication passed! Press Ok and print your finger\n\n Place your figner twice when the grenn light shows up", "Registration", wx.OK)
            val = dlg.ShowModal()
            dlg.Destroy()
            if(val == wx.ID_OK):
                # heighestId = manage_db.getHighestId()
                data = Fingerprint_Controller.enrollFinger(user[0])
                if(str(data) == str(user[0])):
                    manage_db.registerFinger(data)
                    dlg = wx.MessageDialog(self, "Registration completed!", "Registration",
                                           wx.OK)
                    val1 = dlg.ShowModal()
                    dlg.Destroy()
                    if(val1 == wx.ID_OK):
                        self.Hide()
                        new_frame = MainFrame()
                        new_frame.Show()
                        self.Destroy()
                if (data != user[0]):
                    dlg = wx.MessageDialog(self, "Finger doesn't match!\n\n Please try again", "Registration",
                                           wx.OK)
                    val1 = dlg.ShowModal()
                    dlg.Destroy()

class ClockinFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self,parent):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Secondary Frame")
        panel = wx.Panel(self)
        self.ShowFullScreen(True)
        self.frame = parent
        self.isPassed = True

        heading = wx.StaticText(self, -1, label="RMUTK ATTENDANCE", pos=(120, 20))
        headingFont = wx.Font(40, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        heading.SetFont(headingFont)

        subject = wx.StaticText(self, -1, pos=(240, 100))
        subjectFont = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        subject.SetFont(subjectFont)

        status = wx.StaticText(self,-1,pos=(250,160))
        statusFont = wx.Font(25, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        status.SetFont(statusFont)
        self.statuslbl = status

        userInfo = wx.StaticText(self, -1, pos=(190, 220))
        userInfoFont = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        userInfo.SetFont(userInfoFont)

        clockInStatuslbl = wx.StaticText(self, -1, pos=(150, 360))
        clockInStatuslblFont = wx.Font(20, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        clockInStatuslbl.SetFont(clockInStatuslblFont)

        clockinBtn = wx.Button(self, label="Press to scan", pos=(320, 275))
        returnBtn = wx.Button(self, label="Return to Main menu", pos=(295, 325))
        self.userInfo = None


        result = manage_db.getNowClass()
        if(result != None):
            self.userInfo = result[0]
            subjectTxt1 = "Subject: "
            subjectTxt2 = str(result[1][2])
            statusTxt1 = "Status: "
            statusTxt2 = str(result[3][2])
            userInfoTxt1 = "Teacher: "
            userInfoTxt2 = str(result[0][1]) + " " + str(result[0][2])
            self.isPassed = False
            self.sectionlogId = result[3][0]
            self.clockInTime = result[2][4]
            if(result[3][2] != "waiting"):
                self.isPassed = True
        else:
            result = manage_db.getDetailFromLocalDB()
            if(result[3] == None):
                self.userInfo = result[0]
                subjectTxt1 = "Subject: "
                subjectTxt2 = "No class now"
                statusTxt1 = "Status: "
                statusTxt2 = "No class now"
                userInfoTxt1 = "Teacher: "
                userInfoTxt2 = "No class now"
                status.SetPosition((190,160))
                self.isPassed = True
            else:
                self.userInfo = result[0]
                subjectTxt1 = "Subject: "
                subjectTxt2 = str(result[1][2])
                statusTxt1 = "Status: "
                statusTxt2 = str(result[3][2])
                userInfoTxt1 = "Teacher: "
                userInfoTxt2 = str(result[0][1]) + " " + str(result[0][2])
                self.isPassed = False
                self.sectionlogId = result[3][0]
                self.clockInTime = result[2][4]
                self.userInfo[4] = str(self.userInfo[4]).replace("[","")
                self.userInfo[4] = str(self.userInfo[4]).replace("]","")
                self.userInfo[4] = str(self.userInfo[4]).replace("'","")
                if (result[3][2] != "waiting"):
                    self.isPassed = True
        if(subjectTxt2.__len__() > 9):
            subject.SetPosition((200,100))

        if (userInfoTxt2.__len__() > 16):
            userInfo.SetPosition((120,220))

        subject.SetLabel(subjectTxt1 + subjectTxt2)
        status.SetLabel(statusTxt1 + statusTxt2)
        userInfo.SetLabel(userInfoTxt1 + userInfoTxt2)
        self.clockInStatuslbl = clockInStatuslbl
        clockinBtn.Bind(wx.EVT_BUTTON, self.clockIn)
        returnBtn.Bind(wx.EVT_BUTTON,self.newMainFrame)

    def clockIn(self,evt):
        self.clockInStatuslbl.SetLabel("")
        if(self.isPassed == False):
            score = Fingerprint_Controller.clockIn(self.userInfo[0])
            if (score != 0):
                self.clockInStatuslbl.SetLabel(
                    "Auhorization: Passed! Accuracy score: " + str(score))
                self.isPassed = True
                if(manage_db.is_connected()):
                    statusResult = manage_db.clock_in(self.sectionlogId, self.clockInTime)
                else:
                    statusResult = manage_db.clock_in_to_text(self.sectionlogId, self.clockInTime)
                self.statuslbl.SetLabel("Status:" + statusResult);
            else:
                self.clockInStatuslbl.SetLabel("Authorization: Failed. Please Try Again")

    ## ----------------------------------------------------------------------


    def newMainFrame(self, event):
        """
        Close insert frame and open main frame
        """
        # msg = self.msgTxt.GetValue()
        # # Publisher().sendMessage(("show.mainframe"), msg)
        # self.Close()

        self.Hide()
        new_frame = MainFrame()
        new_frame.Show()
        self.Destroy()



########################################################################
class MainPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent


        # Publisher().subscribe(self.showFrame, ("show.mainframe"))

        heading = wx.StaticText(self,-1,label="RMUTK ATTENDANCE",pos=(120,10))
        headingFont = wx.Font(40, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        heading.SetFont(headingFont)

        roomNumber = wx.StaticText(self, -1, pos=(260, 100))
        roomNumberFont = wx.Font(30, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        roomNumber.SetFont(roomNumberFont)

        #
        # clock = AnalogClockWindow(self)
        # clock.SetBackgroundColour("yellow")

        roomTxt1 = "Room: "
        roomTxt2 = manage_db.getRoom("pi-server")

        clockinBtn = wx.Button(self, label="Press to clock in",pos=(320,240))
        clockinBtn.Bind(wx.EVT_BUTTON, self.clockin)

        enrollBtn = wx.Button(self, label="Enroll user fingerprint",pos=(300,290))
        enrollBtn.Bind(wx.EVT_BUTTON, self.regFinger)

        led = gizmos.LEDNumberCtrl(self, -1, (250, 170), (280, 50),
                                   gizmos.LED_ALIGN_CENTER)  # | gizmos.LED_DRAW_FADED)
        self.clock = led
        self.OnTimer(None)


        self.timer = wx.Timer(self)
        self.timer.Start(1)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        roomNumber.SetLabel(roomTxt1 + roomTxt2)

    def OnTimer(self, evt):
        t = time.localtime(time.time())
        st = time.strftime("%I-%M-%S", t)
        self.clock.SetValue(st)

    # ----------------------------------------------------------------------
    def regFinger(self, event):
        """"""
        if(manage_db.is_connected()):
            self.frame.Hide()
            new_frame = EmailVerified(self)
            new_frame.Show()
            self.Close()
        if(manage_db.is_connected() == False):
            dlg = wx.MessageDialog(self, "Cannot connect Database", "Error", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def clockin(self,evt):
        self.frame.Hide()
        new_frame = ClockinFrame(self)
        new_frame.Show()
        self.Destroy()
########################################################################
class MainFrame(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY)
        self.ShowFullScreen(True)
        panel = MainPanel(self)

# ----------------------------------------------------------------------
def job():
    print("I'm working...")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
