"""
本スクリプトはオムロン製環境センサ(2JCIE-BU01)のデータ取得サンプルスクリプトです。
アプリケーション開発時の参考資料としてご使用ください。

Python3を使用して最新計測値(命令アドレス :  0x5021)を取得しています。
取得した値の詳細については、公式ユーザマニュアルを参照してください。
https://www.fa.omron.co.jp/products/family/3724/download/manual.html

■スクリプト開始方法
sudo modprobe ftdi_sio
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id

sudo python3 get_latest_data_sample.py


■スクリプト停止方法
Ctrl + C で停止させてください。

"""

import serial
import time
from datetime import datetime

def calc_crc(buf, length):
    """
    CRC計算処理
    
    """
    crc = 0xFFFF
    for i in range(length):
        crc = crc ^ buf[i]
        for i in range(8):
            carrayFlag = crc & 1
            crc = crc >> 1
            if (carrayFlag == 1) : 
                crc = crc ^ 0xA001
    crcH = crc >> 8
    crcL = crc & 0x00FF
    
    return(bytearray([crcL,crcH]))

def print_long_data(data):
    """
    計測値表示処理
    
    """
    # 現在日時を標準出力
    print("measure Time:" +  datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    # データを10進数に変換して標準出力
    print("temperature:" + str(int(hex(data[9])+format(data[8],'x'),16)/100))
    print("Relative humidity:" + str(int(hex(data[11])+format(data[10],'x'),16)/100))
    print("Ambient light:" + str(int(hex(data[13])+format(data[12],'x'),16)))
    print("Barometric pressure:" + str(int(hex(data[17])+format(data[16],'x')+format(data[15],'x')+format(data[14],'x'),16)/1000))
    print("Sound noise:" + str(int(hex(data[19])+format(data[18],'x'),16)/100))
    print("eTVOC:" + str(int(hex(data[21])+format(data[20],'x'),16)))
    print("eCO2:" + str(int(hex(data[23])+format(data[22],'x'),16)))
    print("Discomfort index:" + str(int(hex(data[25])+format(data[24],'x'),16)/100))
    print("Heat stroke:" + str(int(hex(data[27])+format(data[26],'x'),16)/100))
    print("Vibration information:" + str(int(hex(data[28]),16)))
    print("SI value:" + str(int(hex(data[30])+format(data[29],'x'),16)/10))
    print("PGA:" + str(int(hex(data[32])+format(data[31],'x'),16)/10))
    print("Seismic intensity:" + str(int(hex(data[34])+format(data[33],'x'),16)/1000))
    print("Temperature flag:" + str(int(hex(data[36])+format(data[35],'x'),16)))
    print("Relative humidity flag:" + str(int(hex(data[38])+format(data[37],'x'),16)))
    print("Ambient light flag:" + str(int(hex(data[40])+format(data[39],'x'),16)))
    print("Barometric pressure flag:" + str(int(hex(data[42])+format(data[41],'x'),16)))
    print("Sound noise flag:" + str(int(hex(data[44])+format(data[43],'x'),16)))
    print("eTVOC flag:" + str(int(hex(data[46])+format(data[45],'x'),16)))
    print("eCO2 flag:" + str(int(hex(data[48])+format(data[47],'x'),16)))
    print("Discomfort index flag:" + str(int(hex(data[50])+format(data[49],'x'),16)))
    print("Heat stroke flag:" + str(int(hex(data[52])+format(data[51],'x'),16)))
    print("SI value flag:" + str(int(hex(data[53]),16)))
    print("PGA flag:" + str(int(hex(data[54]),16)))
    print("Seismic intensity flag:" + str(int(hex(data[55]),16)))
    print("")


## 以下メイン処理
# シリアル通信開始
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE)
while(ser.isOpen() == True):
    
    # 最新計測値(Longデータ)取得用命令コマンドを生成
    command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
    crc = calc_crc(command,len(command))
    command = command + crc
    # 命令
    tmp = ser.write(command)
    
    # USB環境センサ側の処理完了を待つために1秒待機
    time.sleep(1)
    
    # 命令結果の受信
    data = ser.read(58)
    
    # 命令結果を加工して標準出力
    print_long_data(data)

