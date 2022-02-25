# VESM3-Vorönn-2022-Pong
Lokaverkefni í Verksmiðju 3


![](https://github.com/Anton-Benediktsson/VESM3-V8/blob/main/Myndir/IMG_20220225_121459.jpg)

# Lýsing 

Stefna verkefnsins er að búa til tveggja manna pingpong leik á LED skjá sem er samsettur af fjórum 64x64 LED Matrix skjáum sem eru tengdir við Raspberry Pi Zero og er stýrður af Leap Motion tækni í gegnum vefþjónustu.

---

# Samsetning

Samsetning var mestmegnis byggð á [sand toy verkefni frá adafruit](https://learn.adafruit.com/matrix-led-sand) frá adafruit og hjálp frá [led matrix libraryinu](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/examples-api-use#remapping-coordinates).

Raspberry Pi var festur á 3D prentaða festingu sem var síðan fest við einn af skjáunum síðan var tengt tölvuna við RGB Matrix Bonnet. Mikilvægt er að lóða vír á GPIO 18 og 4 eins og á mynd 1 til þess að skjárinn keyri betur ásamt því að lóða bút milli 8 og miðju eins og á seinni myndinni til þess að bonnettinn virki með 64x64 skjáinn

![](https://github.com/Anton-Benediktsson/VESM3-V8/blob/main/raspberry_pi_bonnet-jump.jpg)
![](https://github.com/Anton-Benediktsson/VESM3-V8/blob/main/raspberry_pi_bonnet-bridge.jpg)

Bonnettinn og raspberry pi fá rafmagn frá 5v 8 amper batterí sem tengist síðan frá bonettinum í tvo skjái, hinir tveir fá sér 5v 8 amper batterí.

- 64x64 can draw up to 7.68A so you will want to be using a 5V @ 10A power supply with this device.
- Each pixel can draw up to 0.06 Amps each if on full white. The total max per panel is thus 64 * 0.06 = 3.95 Amps or 128 * 0.06 = 7.68 Amps

![](https://github.com/Anton-Benediktsson/VESM3-V8/blob/main/Myndir/IMG_20220224_154714.jpg)

Þegar það er verið að raðtengja skjáinna þá er mikilvægt að tengja þá eins og sýnt er fyrir neðan tið að forðast allt mapping vesen. 

    [<][<] }----- Raspberry Pi connector
    [>][>]



Notast var við fjórar grindur skrúfaðar saman og segla sem skrúfast á skjáinna og sett voru fjórar litlar festingar í miðjunni á skjánum. Best væri að setja fleiri festingar til þess að tryggja að engin bil myndist frá þyngd. 


![](https://github.com/Anton-Benediktsson/VESM3-V8/blob/main/Myndir/IMG_20220224_154910_edited.jpeg)

 








---

# Leap motion controller

## Að setja upp
 Til að setja upp leap motion á **Linux** þarf að setja upp leap deamon, þessi daemon er bara executable sem verður settur upp í /usr/sbin/leapd svo það þarf að búa til service skráina.
 
 `/lib/systemd/system/leapd.service`

    [Unit]
    Description=LeapMotion Daemon
    After=syslog.target
    
    
    [Service]
    Type=simple
    ExecStart=/usr/sbin/leapd
    
    
    [Install]
    WantedBy=multi-user.target

og svo nota `sudo systemctl start leapd.service` þegar maður ætlar að nota leap motion controller

Frá minni reynslu er daemonin frekar lélegur, það tók ca mínútu að stoppa eða enduræsa deamonin, þess vegna er **ekki góð hugmynd að nota** `sudo systemctl enable leapd.service` því að þá mun það alltaf taka mínútu að slökkva á tölvuni. Eftir þetta ættu leap motion forrit eins og visualizer að virka.

## Python 3
 Vandamálið með python 3 á leap motion controller er að leap motion virkar ekki á python 3. Lausnin á þessu er að taka saman Leap sdk uppá nýtt með swig.

 Við notuðum [Leap sdk Python3](https://github.com/BlackLight/leap-sdk-python3) til að gera þetta, en því að við notuðum Swig 4.0.2 þá virkaði það ekki, því að `__swig_getmethods__`, `_swig_property` og smá fleira er ekki lengur til í þessari útgáfu. Þessar línur eru sammt ekki mikilvægar svo það var hægt að taka það út. Sjáðu **leap-modified** í code/ á línu 830, 885, 1317.

---

# Leikurinn

## OpenGL
 Það er **mikilvægt** að vita að *Raspberry Pi Zero* getur ekki notað nýjari en **OpenGL 4.6** og **OpenGL ES 3.2**, sem þýðir að sum libraries fyrir leiki gætu ekki virkað, við notuðum bara Pillow fyrir rendering og bygðum leikinn frá grunni til þess að vera viss um að við þurfum ekki nýajri útgáfu af OpenGL.

## Að búa til on_update
 Til þess að gera update function erum við að gera `start_time = time.time()` og svo **í while loop** `current_time = time.time()` svo er hægt að finna munin með því að nota `start_time - current_time` það er svo hægt að nota if statement til þess að framkvæma update functions hverja **0.1 sekondur**.

## Að rendera mynd
 Til að rendera leikinn erum við að nota **Pillow** *(ImageDraw og Image)*, það virkar með því að búa til nýja mynd (þarf að vera RGB því að matrix tekur ekki svart-hvítt). Það er svo notað Player.draw() function til að teikna rétthyrningana fyrir spilarana, Ball.draw() sem teiknar rétthyrning fyrir kúluna og svo teiknum við textan bara beint.

---

# MQTT

## Að setja upp server
 Við notuðum eigin MQTT server sem var létt að setja upp, það þurfti bara að gera `sudo apt install mosquitto`, og búa til config skrá eins og í code/mosquitto-config. Eftir það var hægt að nota `mosquitto` command til þess að kveikja á serverinum.

## MQTT python
 Við notuðum svo paho.mqtt.client til þess að tala við MQTT serverinn

---
# Myndbönd #


---
# Kóði #
 
* [Adafruit Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix)
 
* [Leap SDK](https://developer-archive.leapmotion.com/documentation/csharp/devguide/Leap_SDK_Overview.html)

* [LMC Python 3](https://github.com/BlackLight/leap-sdk-python3)
---
