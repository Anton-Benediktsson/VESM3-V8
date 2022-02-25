# VESM3-Vorönn-2022-Pong
Lokaverkefni í Verksmiðju 3
# Lýsing 
Stefna verkefnsins er að búa til tveggja manna pingpong leik á LED skjá sem er stýrður af Leap Motion tækni í gegnum vefþjónustu.


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
# Myndbönd #


---
# Kóði #
 
* [Adafruit Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix)
 
* [Leap SDK](https://developer-archive.leapmotion.com/documentation/csharp/devguide/Leap_SDK_Overview.html)

* [LMC Python 3](https://github.com/BlackLight/leap-sdk-python3)
---
