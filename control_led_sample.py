"""
本スクリプトはオムロン製環境センサ(2JCIE-BU01)のLED操作サンプルスクリプトです。
LEDを設定値の色で光らせる処理を行っています。

アプリケーション開発時の参考資料としてご使用ください。

詳細については、公式ユーザマニュアルを参照してください。
https://www.fa.omron.co.jp/products/family/3724/download/manual.html
2.4.5 Advertise setting

■スクリプト開始方法
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id

sudo python3 本スクリプトパス

"""

import serial

"""
設定値
"""
# LEDの色。0～255のRGB値で指定すること
RED_VALUE = 0
GEEN_VALUE = 255
BLUE_VALUE = 0
# LED表示ルール。詳細はマニュアル4.5.8章参照。
DISPLAY_RULE = 1

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


# シリアル接続開始
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE)

# 命令コマンド生成
command = bytearray([0x52, 0x42, 0x0a, 0x00 ,0x02, 0x11, 0x51, DISPLAY_RULE, 0x00, RED_VALUE, GEEN_VALUE, BLUE_VALUE])
crc = calc_crc(command,len(command))
command = command + crc

# 命令
tmp = ser.write(command)


