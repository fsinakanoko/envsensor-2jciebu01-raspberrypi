"""
本スクリプトはオムロン製環境センサ(2JCIE-BU01)の地震回数及び振動回数取得サンプルスクリプトです。
アプリケーション開発時の参考資料としてご使用ください。

詳細については、公式ユーザマニュアルを参照してください。
https://www.fa.omron.co.jp/products/family/3724/download/manual.html
4.5.7 Vibration count

■スクリプト開始方法
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id

sudo python3 本スクリプトパス

"""

import serial
import time

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


ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE, timeout=1)

# アドバタイズパケット設定を取得
command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x31, 0x50])
crc = calc_crc(command,len(command))
command = command + crc

# 命令
tmp = ser.write(command)

# USB環境センサ側の処理完了を待つために1秒待機
time.sleep(1)

# 命令結果の受信
data = ser.read(100)

# 受信結果パース
dict = {}
dict["Earthquake count"] = int(hex(data[10]) + format(data[9],'x') + format(data[8],'x')  + format(data[7],'x'),16)
dict["Vibration count"] = int(hex(data[14]) + format(data[13],'x') + format(data[12],'x')  + format(data[11],'x'),16)

# パース結果表示
for k, v in dict.items():
    print(k +" : " +  str(v))

