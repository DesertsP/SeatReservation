# coding=utf-8

# Created by Deserts
# email: i@panjunwen.com
# site: https://panjunwen.com/
# date: 2016-08-19

from Tkinter import *
from threading import Thread
import datetime
import ConfigParser
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
        self.center_window()
        self.createWidgets()
        self.etcetera()

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
        self.randomSel = BooleanVar()
        self.randomSel.set(True)
        self.text = Text(self.infoFrame, width=30, height=8, )
        self.text.configure(highlightbackground="white",
                            highlightcolor="white")
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
        self.text.grid()

    def etcetera(self):
        # read configs
        conf = ConfigParser.ConfigParser()
        conf.read("config.ini")
        schedTm = conf.get("other", "schedule")
        url = conf.get("other", "url")
        user = conf.get("user", "username")
        pwd = conf.get("user", "password")
        room = int(conf.get("seat", "room"))
        seat = int(conf.get("seat", "seat"))
        start = conf.get("seat", "start")
        end = conf.get("seat", "end")
        schedTm = int(schedTm)
        schedH = schedTm / 60
        schedM = schedTm % 60
        now = datetime.datetime.now()
        self.schedtime = datetime.datetime(now.year, now.month,
                                           now.day, schedH, schedM)
        self.username.set(user)
        self.password.set(pwd)
        self.room.set(room)
        self.seat.set(seat)
        self.start.set(start)
        self.end.set(end)
        # initialize the session
        self.session = SeatReservation(url)
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

    def preProcess(self):
        self.text.delete("1.0", END)
        room = self.room.get()
        seat = self.seat.get()
        seatID = self.session.getSeatID(room, seat)
        start = 0
        end = 0
        try:
            start = int(self.start.get().split(":")[0]) * 60
            end = int(self.end.get().split(":")[0]) * 60
        except:
            self.text.insert(END, '错误：时间格式为纯数字或由":"隔开\n')
            self.text.insert(END, '如，下午一点：13或13:00\n')
        if seatID == 0:
            self.text.insert(END, "错误：不存在的座位号！\n请前往选座系统页面核对\n")
        if start < 420 or end > 1380 or end < start:
            start = 0
            self.text.insert(END, '错误：确保时间范围为7:00 ~ 23:00\n')
        if start and end and seatID:
            conf = ConfigParser.ConfigParser()
            conf.read("config.ini")
            conf.set("seat", "room", room)
            conf.set("seat", "seat", seat)
            conf.set("seat", "start", str(start / 60))
            conf.set("seat", "end", str(end / 60))
            conf = ConfigParser.ConfigParser()
            conf.read("config.ini")
            conf.set("user", "username", self.username.get())
            conf.set("user", "password", self.password.get())
            conf.write(open("config.ini", "w"))
        return (seatID, start, end)

    def reserve(self):
        self.text.delete("1.0", END)
        if self.session.loginStatusCheck() is False:
            self.login()
        seat, start, end = self.preProcess()
        if seat and start and end:
            status = self.session.reserve(seat, start, end)
            self.dealStatusCode(status)

    def auto(self):
        self.text.delete("1.0", END)
        if self.session.loginStatusCheck() is False:
            self.login()
        seat, start, end = self.preProcess()
        room = self.room.get()
        if seat and start and end:
            self.thread_it(self.timer)
            status = self.session.autoReserve(self.schedtime, room, seat,
                                              start, end, self.randomSel.get())
            self.dealStatusCode(status)

    def dealStatusCode(self, status):
        if status is None:
            self.text.insert(END, "预约失败！\n系统预约在")
            self.text.insert(END, "%s开放\n" % str(self.schedtime)[11:16])
            self.text.insert(END, "自动功能须在开放前使用\n你依然可以手动选座\n")
        elif status == 0:
            self.text.insert(END, "预约成功！\n")
            self.text.insert(END, self.session.myReservation())
        elif status == 1:
            self.text.insert(END, "预约失败！\n座位已经一抢而空\n")
        elif status == 2:
            self.text.insert(END, "预约失败！\n请试试其他座位\n")
        elif status == 4:
            self.text.insert(END, "预约失败！\n账户被限制预约\n")
        else:
            self.text.insert(END, "预约失败！\n出现一些未知错误\n")

    def timer(self):
        now = datetime.datetime.now()
        while now < self.schedtime:
            now = datetime.datetime.now()
            timeDelta = (self.schedtime - now).seconds
            self.text.delete("1.0", END)
            self.text.insert(END, "现在 " + str(now)[11:-7] + '\n')
            self.text.insert(END, "等待 " + str(timeDelta) + "s\n\n")
            self.text.insert(END, "请勿关闭窗口！\n")
            time.sleep(1)

SeatReservationGUI().window.mainloop()
