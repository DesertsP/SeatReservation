# coding=utf-8

# Created by Deserts
# email: i@panjunwen.com
# site: https://panjunwen.com/
# date: 2016-08-19

from Tkinter import *
from threading import Thread
import datetime
from Seat import *
from ysuWlan import *


class SeatReservationGUI(object):
    def __init__(self):
        # create the window and frames
        self.window = Tk()
        self.window.title("Library Seat Reservation")
        self.inputFrame = Frame(self.window, borderwidth=10)
        self.inputFrame.grid(row=1, column=1)
        self.signInFrame = Frame(self.inputFrame, borderwidth=15)
        self.signInFrame.grid(row=1, column=1)
        self.seatFrame = Frame(self.inputFrame, borderwidth=0)
        self.seatFrame.grid(row=3, column=1)
        self.optionFrame = Frame(self.inputFrame, borderwidth=0)
        self.optionFrame.grid(row=5, column=1)
        self.infoFrame = Frame(self.window, borderwidth=3)
        self.infoFrame.grid(row=1, column=2)
        self.createWidgets()
        self.center_window()
        # read configs
        url = "http://202.206.242.87/"
        user = None
        pwd = None
        room = None
        seat = None
        start = None
        end = None
        # initialize
        self.session = SeatReservation(url)

    def center_window(self, w=500, h=200):
        self.window.minsize(w, h)
        self.window.maxsize(w, h)
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 100
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def createWidgets(self):
        label1 = Label(self.signInFrame, text="学号")
        label2 = Label(self.signInFrame, text="密码")
        label3 = Label(self.seatFrame, text="房间")
        label4 = Label(self.seatFrame, text="座号")
        label5 = Label(self.seatFrame, text="开始")
        label6 = Label(self.seatFrame, text="结束")
        self.username = StringVar()
        self.password = StringVar()
        self.room = IntVar()
        self.seat = IntVar()
        self.start = StringVar()
        self.end = StringVar()
        self.randomSel = IntVar()
        self.randomSel.set(1)
        usernameEntry = Entry(self.signInFrame, width=13,
                              textvariable=self.username)
        passwordEntry = Entry(self.signInFrame, show='*', width=13,
                              textvariable=self.password)
        roomEntry = Entry(self.seatFrame, width=4, textvariable=self.room)
        seatEntry = Entry(self.seatFrame, textvariable=self.seat, width=4)
        startEntry = Entry(self.seatFrame, textvariable=self.start, width=4)
        endEntry = Entry(self.seatFrame, textvariable=self.end, width=4)
        signInButton = Button(self.signInFrame, text="登入",
                              command=lambda: self.thread_it(self.login))
        selSeatButton = Button(self.seatFrame, text="预约",
                               command=lambda: self.thread_it(self.reserve))
        autoSelButton = Button(self.seatFrame, text="自动",
                               command=lambda: self.thread_it(self.auto))
        randomSelBtn = Checkbutton(self.optionFrame, text="随机派座（目标位置无法选中时）",
                                   variable=self.randomSel)
        wlanButton = Button(self.signInFrame, text="联网",
                            command=lambda: self.thread_it(self.wlan))
        label1.grid(row=1, column=1)
        label2.grid(row=2, column=1)
        label3.grid(row=1, column=1)
        label4.grid(row=2, column=1)
        label5.grid(row=1, column=3)
        label6.grid(row=2, column=3)
        usernameEntry.grid(row=1, column=2)
        passwordEntry.grid(row=2, column=2)
        roomEntry.grid(row=1, column=2)
        seatEntry.grid(row=2, column=2)
        startEntry.grid(row=1, column=4)
        endEntry.grid(row=2, column=4)
        signInButton.grid(row=2, column=3)
        wlanButton.grid(row=1, column=3)
        selSeatButton.grid(row=1, column=5)
        autoSelButton.grid(row=2, column=5)
        randomSelBtn.grid()
        self.text = Text(self.infoFrame, width=30, height=8, )
        self.text.configure(highlightbackground="white",
                            highlightcolor="white")
        self.text.grid()
        self.text.insert(END, "欢迎！\n本工具用于燕山大学图书馆。\n")
        self.text.insert(END, "请勿恶意刷、抢、占座!\n\n\n")
        self.text.insert(END, "Copyleft © Deserts\nhttps://panjunwen.com/\n")

    @staticmethod
    def thread_it(func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def wlan(self):
        self.text.delete("1.0", END)
        self.text.insert(END, "连接到校园网……\n\n")
        wlan = YsuWireless(self.username.get(), self.password.get())
        status = wlan.connect()
        if status == 0:
            self.text.insert(END, "连接成功！\n")
            self.text.insert(END, "剩余流量： %s\n" % wlan.flux())
        elif status == 1:
            self.text.insert(END, "学号或密码错误！\n")
        else:
            self.text.insert(END, "请检查网络环境！\n")

    def login(self):
        self.text.delete("1.0", END)
        status = self.session.login(self.username.get(), self.password.get())
        if status == 0:
            self.text.insert(END, "登入成功！\n")
        elif status == 1:
            self.text.insert(END, "登入失败！\n用户不存在，检查学号。\n")
        elif status == 2:
            self.text.insert(END, "登入失败！\n密码错误，请重新输入。\n")
        else:
            self.text.insert(END, "登入失败！\n请检查网络环境！\n")

    def reserve(self):
        if self.session.loginStatusCheck() is False:
            self.login()
        seat, start, end = self.preProcess()
        if seat and start and end:
            self.session.reserve(seat, start, end)

    def preProcess(self):
        room = self.room.get()
        seat = self.seat.get()
        seatID = self.session.getSeatID(room, seat)
        start = 0
        end = 0
        try:
            start = int(self.start.get().split(":")[0]) * 60
            end = int(self.end.get().split(":")[0]) * 60
        except:
            self.text.insert(END, '错误：时间格式为纯数字或由":"隔开。\n')
            self.text.insert(END, '如，早八点：8或8:00\n下午一点：13或13:00')
        if seatID == 0:
            self.text.insert(END, "错误：不存在的座位号\n请前往选座系统页面核对.")
        # conf = ConfigParser.ConfigParser()
        # conf.read("default.config")
        # conf.set("seat", "room", room)
        # conf.set("seat", "seat", seat)
        # conf.set("seat", "start", start)
        # conf.set("seat", "end", end)
        # conf.write(open("default.config", "w"))
        return (seatID, start, end)

    def auto(self):
        if self.session.loginStatusCheck() is False:
            self.login()
        seat, start, end = self.preProcess()
        room = self.room.get()
        if seat and start and end:
            self.session.autoReserve()



app = SeatReservationGUI()
app.window.mainloop()












