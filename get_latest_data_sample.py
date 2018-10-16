"""
本スクリプトはオムロン製環境センサ(2JCIE-BU01)のデータ取得サンプルスクリプトです。
アプリケーション開発時の参考資料としてご使用ください。

Python3を使用して最新計測値(命令アドレス :  0x5021)を取得しています。
取得した値の詳細については、公式ユーザマニュアルを参照してください。
https://www.fa.omron.co.jp/products/family/3724/download/manual.html

■スクリプト開始方法
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id

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

def parse_long_data(data):
    """
    受信値パース処理
    
    """
    
    dict = {}
    # 現在日時を標準出力
    dict["measure Time"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # データを10進数に変換して標準出力
    dict["temperature"] = int(hex(data[9])+format(data[8],'x'),16)/100
    dict["Relative humidity"] = int(hex(data[11])+format(data[10],'x'),16)/100
    dict["Ambient light"] = int(hex(data[13])+format(data[12],'x'),16)
    dict["Barometric pressure"] = int(hex(data[17])+format(data[16],'x')+format(data[15],'x')+format(data[14],'x'),16)/1000
    dict["Sound noise"] = int(hex(data[19])+format(data[18],'x'),16)/100
    dict["eTVOC"] = int(hex(data[21])+format(data[20],'x'),16)
    dict["eCO2"] = int(hex(data[23])+format(data[22],'x'),16)
    dict["Discomfort index"] = int(hex(data[25])+format(data[24],'x'),16)/100
    dict["Heat stroke"] = int(hex(data[27])+format(data[26],'x'),16)/100
    dict["Vibration information"] = int(hex(data[28]),16)
    dict["SI value"] = int(hex(data[30])+format(data[29],'x'),16)/10
    dict["PGA"] = int(hex(data[32])+format(data[31],'x'),16)/10
    dict["Seismic intensity"] = int(hex(data[34])+format(data[33],'x'),16)/1000
    dict["Temperature flag"] = int(hex(data[36])+format(data[35],'x'),16)
    dict["Relative humidity flag"] = int(hex(data[38])+format(data[37],'x'),16)
    dict["Ambient light flag"] = int(hex(data[40])+format(data[39],'x'),16)
    dict["Barometric pressure flag"] = int(hex(data[42])+format(data[41],'x'),16)
    dict["Sound noise flag"] = int(hex(data[44])+format(data[43],'x'),16)
    dict["eTVOC flag"] = int(hex(data[46])+format(data[45],'x'),16)
    dict["eCO2 flag"] = int(hex(data[48])+format(data[47],'x'),16)
    dict["Discomfort index flag"] = int(hex(data[50])+format(data[49],'x'),16)
    dict["Heat stroke flag"] = int(hex(data[52])+format(data[51],'x'),16)
    dict["SI value flag"] = int(hex(data[53]),16)
    dict["PGA flag"] = int(hex(data[54]),16)
    dict["Seismic intensity flag"] = int(hex(data[55]),16)
    
    return(dict)


def print_data(dict):
    """
    計測値表示処理
    
    """
    
    for k, v in dict.items():
        print(k +" : " +  str(v))
    
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
    
    # 受信データをパース
    dict_data =  parse_long_data(data)
    
    # 命令結果を加工して標準出力
    print_data(dict_data)

