import tkinter, win32api, win32con, pywintypes
from tkinter import *
from tkinter.ttk import Combobox

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H
import socket
import getpass
from  Cython.Build import *
def get_replicate_text(text):
    i, space, str1, str2 = 0, 30, "", ""
    while (i <= 5):
        str1 = str1 + text + " " * space
        i = i + 1
    str2 = " " * space + str1 + "\n\n\n\n"
    str1 = str1 + "\n\n\n\n"
    str1 = (str1 + str2) * 4
    return str1
def generateQRcode(data,imgFn):
    qr=qrcode.QRCode(version=20,error_correction=ERROR_CORRECT_H,box_size=3,border=2)
    qr.add_data(data)
    qr.make()
    # 创建二维码图片
    img = qr.make_image()
    imgW, imgH = img.size
    w1, h1 = map(lambda x: x // 4, img.size)
    # 要粘贴的自定义图片，生成缩略图
    #im = Image.open(imgFn)
    #imW, imH = im.size
    #w1 = w1 if w1 < imW else imW
    #h1 = h1 if h1 < imH else imH
    #im = im.resize((w1, h1))
    # 在二维码上中间位置粘贴自定义图片
   # img.paste(im, ((imgW - w1) // 2, (imgH - h1) // 2))
    # 保存二维码图片
    img.save('qrCode.png')
    return img
def watermark(data,img,option,font,color,size):
    root = tkinter.Toplevel()
    width = win32api.GetSystemMetrics(0)  # 获取屏幕宽度
    height = win32api.GetSystemMetrics(1)  # 获取屏幕高度
    root.overrideredirect(True)  # 隐藏显示框
    root.geometry("%sx%s+0+0" % (width, height))  # 设置窗口位置或大小
    root.lift()  # 置顶层
    root.wm_attributes("-topmost", True)  # 始终置顶层
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")  # 白色背景透明
    hWindow = pywintypes.HANDLE(int(root.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    if(option==1):
        text1 = get_replicate_text(data)
        label = tkinter.Label(root, text=text1, font=(font, size), fg=color, bg='white')
        label.pack(side=RIGHT)  # 显示
        root.mainloop()  # 循环

    else:
        generateQRcode(data, img)
        imga = tkinter.PhotoImage(file='qrCode.png')
        label = tkinter.Label(root, image=imga,  fg='#d5d5d5', bg='white')
        label.pack(side=RIGHT)  # 显示
        root.mainloop()  # 循环
def set_para(data,option):
    hostname = socket.gethostname()
    Compute_addr = socket.gethostbyname(hostname)
    userName = getpass.getuser()
    para={
        'data':data+"%s%s%s"%(hostname,Compute_addr,userName),
        'img':'img.png',
        'option':option
    }
    return para
# def Setting():
#     root=tkinter.Tk()
#     root.geometry('400x400')
#     root.title('水印设置')
#     e=Entry(root,show=None,width='40')
#     e.pack()
#     def get_textwm():
#         data=e.get()
#         parameters=set_para(data,1)
#         data=parameters['data']
#         img=parameters['img']
#         option=parameters['option']
#         watermark(data,img,option)
#     def get_qrwm():
#         data=e.get()
#         parameters=set_para(data,2)
#         data = parameters['data']
#         img = parameters['img']
#         option = parameters['option']
#         watermark(data, img, option)
#     b1 = Button(root, text='明文形式',command=get_textwm)
#     b1.pack()
#     b2 = Button(root, text='二维码形式',command=get_qrwm)
#     b2.pack()
#     root.mainloop()

     # Setting()
    # parameters=set_para('ad',2)
    # data=parameters['data']
    # img=parameters['img']
    # option=parameters['option']
    # watermark(data,img,option)
root = tkinter.Tk()
root.geometry('400x400')
root.title('水印设置')
e1 = Entry(root, show=None, width='40')
e1.insert(10,'北京艾科网信科技有限公司')
e1.pack()
# e2 = Entry(root, show=None, width='40')
# e2.insert(10,'宋体')
# e2.pack()
# e3 = Entry(root, show=None, width='40')
# e3.insert(10,'#5d5d5d')
# e3.pack()
# e4 = Entry(root, show=None, width='40')
# e4.insert(10,'20')
# e4.pack()
font=StringVar()
numberChosen = Combobox(root, width=12, textvariable=font)
numberChosen['values'] = ('请选择字体','宋体', '华文行楷','微软雅黑','黑体')
numberChosen.current(0)
numberChosen.pack()
color=StringVar()
numberChosen1 = Combobox(root, width=12, textvariable=color)
numberChosen1['values'] = ('请选择颜色','#5d5d5d','red', 'green','blue')
numberChosen1.current(0)
numberChosen1.pack()
size=StringVar()
numberChosen2 = Combobox(root, width=12, textvariable=size)
numberChosen2['values'] = ('请选择字体大小','18','21','24','27','30')
numberChosen2.current(0)
numberChosen2.pack()
def get_textwm():
    data = e1.get()
    font=numberChosen.get()

    color=numberChosen1.get()
    size=numberChosen2.get()
    parameters = set_para(data, 1)
    data = parameters['data']
    img = parameters['img']
    option = parameters['option']
    watermark(data, img, option,font,color,size)
def get_qrwm():
    data = e1.get()
    font = numberChosen.get()
    color = numberChosen1.get()
    size = numberChosen2.get()
    parameters = set_para(data, 2)
    data = parameters['data']
    img = parameters['img']
    option = parameters['option']
    watermark(data, img, option,font,color,size)
menubar=Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='开始', menu=filemenu)
filemenu.add_command(label='明文形式', command=get_textwm)
filemenu.add_command(label='二维码形式', command=get_qrwm)
filemenu.add_command(label='退出', command=root.quit)
root.config(menu=menubar)
root.mainloop()



