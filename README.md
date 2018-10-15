
# envsensor-2jciebu01-raspberrypi

## [1] 概要
OMRON製環境センサ(2JCIE-BU01)をRasPi Python3で操作するプログラムです。  
2JCIE-BU01を使用したシステムを構築する際の参考資料(サンプルプログラム)としてお使いください。

![全体.PNG](/img/全体.PNG)

## [2]使用方法(環境データ受信)

### (1) ドライバ読込  
スクリプト実行前に、以下の手順で2JCIE-BU01のドライバを読み込んでください。

``` bash
sudo modprobe ftdi_sio
sudo echo 0590 00d4 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id
sudo chmod 777 /sys/bus/usb-serial/drivers/ftdi_sio/new_id
```

### (3) 操作説明
スクリプトをRasPiの任意の位置に配置し、スーパーユーザー権限で実行してください。

```bash
sudo python3 get_latest_data_sample.py
```

### （参考）ソースコード解説

#### (1) 概要
本項ではサンプルプログラムソースコードの重要箇所の解説を行います。   
尚、本項を読むまえにオムロン社が公開している通信仕様もしくは、envsensor-2jciebu01-wincsharpの(参考) 通信仕様解説を御一読ください。  

公開通信仕様 :  
https://www.fa.omron.co.jp/data_pdf/mnu/cdsc-016a-web1_2jcie-bu01.pdf?id=3724


通信仕様解説:  
https://github.com/fsinakanoko/envsensor-2jciebu01-wincsharp#%E5%8F%82%E8%80%83-%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98%E8%A7%A3%E8%AA%AC

TODO : 納品時にURLを以下に変更するのを忘れないこと  
https://github.com/OmronIXI/envsensor-2jciebu01-wincsharp#%E5%8F%82%E8%80%83-%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98%E8%A7%A3%E8%AA%AC


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
```


## [3]使用方法(LED制御)

TODO :　作成中



## [4]使用方法(地震/振動カウント)

TODO :　作成中


以上
