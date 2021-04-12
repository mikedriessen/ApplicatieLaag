verStr = "PingChecker v0.1"

# -- constants -----------------------------------------------------------------
pingTarg = "8.8.8.8"
pingSlow = 100
pingBad = 300

# -- colors --------------------------------------------------------------------
colStart = "#00D000"
colStop = "#D00000"
colGood = "#00D000"
colSlow = "#D0D000"
colBad = "#D00000"
colFail = "#FFD0D0"
colAxis = "#000000"
colBack = "#F0F0F0"
colChart = "#FFFFFF"
colLogBG = "#FFFFFF"

# -- includes ------------------------------------------------------------------
from datetime import datetime, date, time, timedelta
from time import sleep
import subprocess, platform
from tkinter import *
import tkinter.messagebox


# ------------------------------------------------------------------------------
class Application(Frame):
    running = False
    dataSet = []
    graphWidth = 450
    graphHeight = 128
    pingMean = 0
    pingMax = 0
    pingBad = 0

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # action buttons
        self.startButton = Button(self, text="Start", width=10, bg=colStart, command=self.cmdStart,
                                  font=("Helvetica", "12"))
        self.startButton.grid(column=1, row=1, padx=4)
        self.saveButton = Button(self, text="Save", width=10, command=self.cmdSave, font=("Helvetica", "12"))
        self.saveButton.grid(column=1, row=6, padx=4)
        self.quitButton = Button(self, text="Quit", width=10, command=self.checkQuit, font=("Helvetica", "12"))
        self.quitButton.grid(column=1, row=7, padx=4)
        # option menus
        self.freqOptions = ("5s", "10s", "60s", "600s")
        self.freqList = (5000, 10000, 60000, 600000)
        self.freqSelect = StringVar(self)
        self.freqSelect.set(self.freqOptions[2])
        self.freqSelectMenu = OptionMenu(self, self.freqSelect, *self.freqOptions)
        self.freqSelectMenu.config(width=6, font=("Helvetica", "12"))
        self.freqSelectMenu.grid(column=1, row=2)
        self.lookOptions = (
        "Sample", "30min", "1hour", "2hours", "4hours", "12hours", "1day", "2days", "10days", "30days")
        self.lookList = (1, 0.5, 1, 2, 4, 12, 24, 48, 240, 720)
        self.lookSelect = StringVar(self)
        self.lookSelect.set(self.lookOptions[0])
        self.lookSelectMenu = OptionMenu(self, self.lookSelect, *self.lookOptions)
        self.lookSelectMenu.config(width=6, font=("Helvetica", "12"))
        self.lookSelectMenu.grid(column=1, row=3)
        # labels
        self.aboutLabel = Label(self, text=verStr)
        self.aboutLabel.grid(column=4, row=0, columnspan=3, sticky=E)

        self.meanLabel = Label(self, text='Avg: ')
        self.meanLabel.grid(column=3, row=5, sticky=W)
        self.maxLabel = Label(self, text='Max: ')
        self.maxLabel.grid(column=4, row=5, sticky=W)
        self.badLabel = Label(self, text='Bad: ')
        self.badLabel.grid(column=5, row=5, sticky=W)
        # data canvas
        self.graph = Canvas(self, width=self.graphWidth, height=self.graphHeight, bg=colChart)
        self.graph.grid(column=3, row=1, sticky=NW, columnspan=4, rowspan=4)
        # log window
        self.log = Text(self, width=54, height=5, bg=colLogBG)
        self.log.grid(column=3, row=6, padx=0, pady=3, rowspan=2, columnspan=3)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.log.yview)
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=6, row=6, padx=0, pady=3, rowspan=2, sticky=N + S)
        # spacers
        self.space1Label = Label(self, text=" ")
        self.space1Label.grid(column=0, row=0)
        self.space2Label = Label(self, text=" ")
        self.space2Label.grid(column=2, row=5)
        self.space3Label = Label(self, text=" ")
        self.space3Label.grid(column=7, row=8)

    # log event
    def logEvent(self, event, time):
        if time:
            self.log.insert(END, '{:%Y-%m-%d %H:%M:%S} '.format(datetime.now()))
        self.log.insert(END, event + "\n")
        self.log.see(END)

    def logResponse(self, msg):
        if len(msg) > 0:
            for byte in msg:
                self.log.insert(END, chr(byte))
        else:
            self.log.insert(END, "No Data!!")
        self.log.insert(END, "\n")
        self.log.see(END)

    # handle the start/stop button
    def cmdStart(self):
        if not self.running:
            self.startButton.config(text="Stop", bg=colStop)
            self.running = True
            self.logEvent("Started pinging", True)
            self.ping()
        else:
            self.startButton.config(text="Start", bg=colStart)
            self.running = False
            self.logEvent("Stopped pinging", True)

    # handle the save button
    def cmdSave(self):
        fileName = 'NetData{:%Y%m%d%H%M%S}.dat'.format(datetime.now())
        good = False
        try:
            file = open(fileName, 'w')
        except:
            self.logEvent("Error! Unable to open file {} for save".format(fileName), True)
            return
        file.write('{} data file\n'.format(verStr))
        file.write('{:%Y-%m-%d %H:%M:%S}\n\n'.format(datetime.now()))
        file.write('Date       Time     Stat Ping(ms)\n')
        for point in self.dataSet:
            file.write('{:%Y-%m-%d %H:%M:%S} '.format(point[0]))
            if point[1]:
                file.write('Good ')
            else:
                file.write('Fail ')
            file.write('{:d}\n'.format(point[2]))
        file.close()
        self.logEvent("Save {}".format(fileName), True)

    # handle the quit button
    def checkQuit(self):
        self.quit()

    # ping the target
    def ping(self):
        good = False
        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
        cmd = "ping " + " " + ping_str + " " + pingTarg
        useShell = not (platform.system().lower() == "windows")
        # ping it
        result = subprocess.run(args=cmd, universal_newlines=True, shell=useShell, stdout=subprocess.PIPE)
        output = result.stdout.splitlines()
        if result.returncode == 0:
            good = True
        if good:
            try:
                rTime = int(output[7].split()[-1][:-2])
            except:
                rTime = 0
            self.dataSet.append((datetime.now(), good, rTime))
            self.logEvent("Ping {} success at {:d}ms".format(pingTarg, rTime), True)
        else:
            self.dataSet.append((datetime.now(), good, -1))
            self.logEvent("Ping {} failure".format(pingTarg), True)
        # gather statistics
        self.pingMean = 0
        self.pingMax = 50
        self.pingBad = 0
        for point in self.dataSet:
            if point[1]:
                self.pingMean = self.pingMean + point[2]
                if point[2] > self.pingMax: self.pingMax = point[2]
            else:
                self.pingBad += 1
        if (len(self.dataSet) - self.pingBad) > 4:
            self.pingMean = int(self.pingMean / (len(self.dataSet) - self.pingBad))
        self.drawGraph()
        self.meanLabel.config(text='Avg: {:d}'.format(self.pingMean))
        self.maxLabel.config(text='Max: {:d}'.format(self.pingMax))
        self.badLabel.config(text='Bad: {:d}'.format(self.pingBad))
        if self.running:
            interval = self.freqList[self.freqOptions.index(self.freqSelect.get())]
            root.after(interval, self.ping)

    # draw graph contents
    def drawGraph(self):
        xMarg = 40
        yMarg = 20
        for i in self.graph.find_all():
            self.graph.delete(i)
        if len(self.dataSet) < 1:
            return
        if self.lookSelect.get() == 'Sample':  # plot one pixel per sample on chart
            data = self.dataSet[-(self.graphWidth - xMarg):]
            # find max for scale
            yMax = 50
            for point in data:
                if point[2] > yMax: yMax = point[2]
            # plot it
            x = self.graphWidth - len(data)
            zero = self.graphHeight - yMarg
            yScale = zero / yMax
            for point in data:
                x += 1
                if point[1]:
                    val = point[2]
                    color = colGood
                    if val > pingSlow: color = colSlow
                    if val > pingBad:  color = colBad
                    if val == -1:      color = colBad
                    y = int(zero - (val * yScale))
                    dLine = self.graph.create_line(x, zero, x, y, fill=color)
                else:
                    dLine = self.graph.create_line(x, zero, x, 0, fill=colFail)
            self.graph.create_text(xMarg, zero + 1, text="{:%Y-%m-%d %H:%M:%S}".format(data[0][0]), anchor=NW)
            self.graph.create_text(self.graphWidth, zero + 1,
                                   text="{:%Y-%m-%d %H:%M:%S}".format(data[len(data) - 1][0]), anchor=NE)
        else:  # plot time period as selected
            period = self.lookList[self.lookOptions.index(self.lookSelect.get())] * 3600
            stop = datetime.timestamp(datetime.now())
            start = stop - period
            data = []
            for point in self.dataSet:
                if datetime.timestamp(point[0]) >= start and datetime.timestamp(point[0]) <= stop:
                    data.append(point)
            # find max for scale
            yMax = 50
            for point in data:
                if point[2] > yMax: yMax = point[2]
            # plot it
            zero = self.graphHeight - yMarg
            yScale = zero / yMax
            for point in data:
                x = (((datetime.timestamp(point[0]) - start) / period) * (self.graphWidth - xMarg)) + xMarg
                if point[1]:
                    val = point[2]
                    color = colGood
                    if val > pingSlow: color = colSlow
                    if val > pingBad:  color = colBad
                    if val == -1:      color = colBad
                    y = int(zero - (val * yScale))
                    dLine = self.graph.create_line(x, zero, x, y, fill=color)
                else:
                    dLine = self.graph.create_line(x, zero, x, 0, fill=colFail)
            self.graph.create_text(xMarg, zero + 1, text="{:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(start)),
                                   anchor=NW)
            self.graph.create_text(self.graphWidth, zero + 1,
                                   text="{:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(stop)), anchor=NE)
        # draw axis
        self.graph.create_line(xMarg, 0, xMarg, self.graphHeight - yMarg, fill=colAxis)
        self.graph.create_line(xMarg, self.graphHeight - yMarg, self.graphWidth, self.graphHeight - yMarg, fill=colAxis)
        self.graph.create_text(xMarg - 1, zero, text="0ms", anchor=SE)
        self.graph.create_text(xMarg - 1, 0, text="{:d}ms".format(yMax), anchor=NE)


# --GUI-------------------------------------------------------------------------
root = Tk()
app = Application(master=root)
app.master.title("NetCheck")
app.mainloop()
root.destroy()

# -- End NetCheck --------------------------------------------------------------


