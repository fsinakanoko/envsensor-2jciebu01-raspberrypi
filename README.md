
# envsensor-2jciebu01-raspberrypi

## [1] 概要
OMRON製環境センサ(2JCIE-BU01)をRasPi Python3で操作するプログラムです。  
2JCIE-BU01を使用したシステムを構築する際の参考資料(サンプルプログラム)としてお使いください。  
なお、ソースコード確認前にオムロン社が公開している通信仕様もしくは、envsensor-2jciebu01-wincsharpの(参考) 通信仕様解説を御一読ください。  

公開通信仕様 :  
https://www.fa.omron.co.jp/data_pdf/mnu/cdsc-016a-web1_2jcie-bu01.pdf?id=3724


通信仕様解説:  
https://github.com/fsinakanoko/envsensor-2jciebu01-wincsharp#%E5%8F%82%E8%80%83-%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98%E8%A7%A3%E8%AA%AC

TODO : 納品時にURLを以下に変更するのを忘れないこと  
https://github.com/OmronIXI/envsensor-2jciebu01-wincsharp#%E5%8F%82%E8%80%83-%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98%E8%A7%A3%E8%AA%AC



![全体.PNG](/img/全体.PNG)

## [2]使用方法(環境データ受信)

### (1) ドライバ読込  
スクリプト実行前に、以下の手順で2JCIE-BU01のドライバを読み込んでください。

``` bash
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
```

### (3) 操作説明
スクリプトをRasPiの任意の位置に配置し、スーパーユーザー権限で実行してください。

```bash
sudo python3 get_latest_data_sample.py
```

### （参考）ソースコード解説

#### (1) 概要
本項ではサンプルプログラムソースコードの重要箇所の解説を行います。   

#### (2) Commandデータ送信プログラムについて

実際のサンプルプログラムの送信処理部は以下の通りです。

```python
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE)
while(ser.isOpen() == True):

    # 最新計測値(Longデータ)取得用命令コマンドを生成
    command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x21, 0x50])
    crc = calc_crc(command,len(command))
    command = command + crc
    # 命令
    tmp = ser.write(command)
```

#### (3) Responseデータ受信プログラムについて

実際のサンプルプログラムの受信処理部は以下の通りです。

```python
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE)
while(ser.isOpen() == True):

  ～送信処理省略～

  # 命令結果の受信
  data = ser.read(58)

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
```


## [3]使用方法(LED制御)

### (1) ドライバ読込  
スクリプト実行前に、以下の手順で2JCIE-BU01のドライバを読み込んでください。

``` bash
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
```

### (3) 操作説明
スクリプトをRasPiの任意の位置に配置し、スーパーユーザー権限で実行してください。

```bash
sudo python3 control_led_sample.py
```

### （参考）ソースコード解説

#### (1) 概要
本項ではサンプルプログラムソースコードの重要箇所の解説を行います。   

#### (2) Commandデータ送信仕様について

**1. CommandデータのPayload部の仕様は以下の通りです。**

参考 : 4.5.8 LED setting [normal state]  
![4_5_8_LED_setting.PNG](/img/4_5_8_LED_setting.PNG)

**2. 役割と実データ例は以下の通りです。**

|番地|役割|実データ例|説明|
|:---|:---|:---|:---|
|0|Header|0x52|固定|
|1|Header|0x42|固定|
|2|Length|0x0a|PayloadからCRCまでのデータ長の1バイト目。(Payload(8) + CRC(2) = 0x000a)|
|3|Length|0x00|PayloadからCRCまでのデータ長の2バイト目。(Payload(8) + CRC(2) = 0x000a)|
|4|Payload|0x02|Read,Writeを指定。(0x01 : Read 0x02 : Write)|
|5|Payload|0x11|実行する内容に応じたAddressの1バイト目。(0x5011 :LED setting)|
|6|Payload|0x50|実行する内容に応じたAddressの2バイト目。(0x5011 :LED setting)|
|7|Payload|0x01|Display ruleの1バイト目。 光の色を指定する場合はNormally ON(0x0001)|
|8|Payload|0x00|Display ruleの2バイト目。 光の色を指定する場合はNormally ON(0x0001)|
|9|Payload|0x00|赤色の強さ。0～255(0x00～0xFF)の値を設定。Display ruleがNormally ONの時に指定する。|
|10|Payload|0xFF|緑色の強さ。0～255(0x00～0xFF)の値を設定。Display ruleがNormally ONの時に指定する。|
|11|Payload|0x00|青色の強さ。0～255(0x00～0xFF)の値を設定。Display ruleがNormally ONの時に指定する。|
|12|CRC-16|0xD2|計算したCRC値の1バイト目。|
|13|CRC-16|0x35|計算したCRC値の２バイト目。|

**3. 実際のサンプルプログラムの送信処理は以下の通りです。**  

```python

# LED表示ルール。
DISPLAY_RULE = 1
# LEDの色。0～255のRGB値で指定すること
RED_VALUE = 0
GEEN_VALUE = 255
BLUE_VALUE = 0

# シリアル接続開始
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE)

# 命令コマンド生成
command = bytearray([0x52, 0x42, 0x0a, 0x00 ,0x02, 0x11, 0x51, DISPLAY_RULE, 0x00, RED_VALUE, GEEN_VALUE, BLUE_VALUE])
crc = calc_crc(command,len(command))
command = command + crc

# 命令
tmp = ser.write(command)

```

## [4]使用方法(地震/振動カウント)

### (1) ドライバ読込  
スクリプト実行前に、以下の手順で2JCIE-BU01のドライバを読み込んでください。

``` bash
sudo modprobe ftdi_sio
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
```

### (3) 操作説明
スクリプトをRasPiの任意の位置に配置し、スーパーユーザー権限で実行してください。

```bash
sudo python3 get_vibration_count_sample.py
```

### （参考）ソースコード解説

#### (1) 概要
本項ではサンプルプログラムソースコードの重要箇所の解説を行います。   

#### (2) Commandデータ送信仕様について

**1. CommandデータのPayload部の仕様は以下の通りです。**

参考 : 4.5.7 Vibration count  
![4_5_7_Vibration_count.PNG](/img/4_5_7_Vibration_count.PNG)

**2. 役割と実データ例は以下の通りです。**

|番地|役割|実データ例|説明|
|:---|:---|:---|:---|
|0|Header|0x52|固定|
|1|Header|0x42|固定|
|2|Length|0x05|PayloadからCRCまでのデータ長の1バイト目。(Payload(3) + CRC(2) = 0x0005)|
|3|Length|0x00|PayloadからCRCまでのデータ長の2バイト目。(Payload(3) + CRC(2) = 0x0005)|
|4|Payload|0x01|Read,Writeを指定。(0x01 : Read 0x02 : Write)|
|5|Payload|0x31|実行する内容に応じたAddressの1バイト目。(0x5031 :Vibration count)|
|6|Payload|0x50|実行する内容に応じたAddressの2バイト目。(0x5031 :Vibration count)|
|7|CRC-16|0xEF|計算したCRC値の1バイト目。|
|8|CRC-16|0x8B|計算したCRC値の２バイト目。|

**3. 実際のサンプルプログラムの送信処理は以下の通りです。**  

```python
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE, timeout=1)

# アドバタイズパケット設定を取得
command = bytearray([0x52, 0x42, 0x05, 0x00, 0x01, 0x31, 0x50])
crc = calc_crc(command,len(command))
command = command + crc

# 命令
tmp = ser.write(command)

```

### (3) Responseデータ仕様について

**1. ResponseデータのPayload部の仕様は以下の通りです。**

参考 : 4.5.7 Vibration count  
![4_5_7_Vibration_count.PNG](/img/4_5_7_Vibration_count.PNG)

**2. 役割と実データ例は以下の通りです。**  

|番地|役割|実データ例|説明|
|:---|:---|:---|:---|
|0|Header|0x52|固定|
|1|Header|0x42|固定|
|2|Length|0x0D|PayloadからCRCまでのデータ長の1バイト目。(Payload(11) + CRC(2) = 0x000D)|
|3|Length|0x00|PayloadからCRCまでのデータ長の2バイト目。(Payload(11) + CRC(2) = 0x000D)|
|4|Payload|0x01|Read,Writeを指定。(0x01 : Read 0x02 : Write)|
|5|Payload|0x31|実行する内容に応じたAddressの1バイト目。(0x5031 :Vibration count)|
|6|Payload|0x50|実行する内容に応じたAddressの2バイト目。(0x5031 :Vibration count)|
|7|Payload|0x09|Earthquake countの1バイト目|
|8|Payload|0x00|Earthquake countの2バイト目|
|9|Payload|0x00|Earthquake countの3バイト目|
|10|Payload|0x00|Earthquake countの4バイト目|
|11|Payload|0x0C|Vibration countの1バイト目|
|12|Payload|0x00|Vibration countの2バイト目|
|13|Payload|0x00|Vibration countの3バイト目|
|14|Payload|0x00|Vibration countの4バイト目|
|15|CRC-16|0xA9|計算したCRC値の1バイト目|
|16|CRC-16|0x0E|計算したCRC値の２バイト目|

**3.実際のサンプルプログラムの受信処理は以下の通りです。**  
```python
ser = serial.Serial("/dev/ttyUSB0",115200,serial.EIGHTBITS, serial.PARITY_NONE, timeout=1)

～送信処理省略～

# 命令結果の受信
data = ser.read(100)

# 受信結果パース
dict = {}
dict["Earthquake count"] = int(hex(data[10]) + format(data[9],'x') + format(data[8],'x')  + format(data[7],'x'),16)
dict["Vibration count"] = int(hex(data[14]) + format(data[13],'x') + format(data[12],'x')  + format(data[11],'x'),16)

```

以上
