import time

import socket

from machine import UART
from machine import Pin

import network

port = 10000
uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network..')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def InitLight():
    global P2
    P2 = Pin(2, Pin.OUT)
    P2.off()


def do_ap():
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='esp32', password='12345678', authmode=network.AUTH_WPA_WPA2_PSK)
    ap.active(True)


def Check_Ap(a):
    if (ap.isconnected()):
        P2.on()
        ip = ap.ifconfig()[0]
        if a == True:
            print("Connected")
            print(ip)
            return False
    else:
        P2.on()
        time.sleep(0.5)
        P2.off()
        time.sleep(0.5)
        print("Waitting for connecting...")
        return True


def SocketProc():
    ip = ap.ifconfig()[0]
    print(ip)
    listenSocket = socket.socket()
    listenSocket.bind((ip, port))
    listenSocket.listen(1)
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenSocket.settimeout(5)
    print("TCP,Waitting...")
    while True:
        try:
            #完成连接P2常亮
            P2.on()
            #print(ap.isconnected())
            if(ap.isconnected()==False):
                GetIp = Check_Ap(GetIp)
            print("accepting")
            #建立socket连接
            conn, addr = listenSocket.accept()
            print(addr, "connected")
            while True:
                try:
                    #进入数据接收
                    data = conn.recv(1024)
                    print(data)
                    #检查断联
                    if (len(data) == 0):
                        print("Disconnected")
                        conn.close()
                        break
                    
                    if(ap.isconnected() == 0):
                        print("Disconnected")
                        return
                except Exception as e:
                    conn.close()
                    print(addr," Disconnected")
                    break
        except Exception as e:
            continue

def _main_():
    InitLight()
    do_ap()
    GetIp = True
    while True:
        GetIp = Check_Ap(GetIp)
        SocketProc()

_main_()

