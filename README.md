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

 Ég notaði [Leap sdk Python3](https://github.com/BlackLight/leap-sdk-python3) til að gera þetta en því að ég notaði Swig 4.0.2 þá virkaði það ekki því að það var `__swig_getmethods__` og `_swig_property` þessar línur eru sammt ekki mikilvægar svo það var hægt að taka það út ég tók í burtu. Sjáðu **leap-modified** í code/ á línu 830, 885, 1317.

---
# Myndbönd #


---
# Kóði #
 
* [Adafruit Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix)
 
* [Leap SDK](https://developer-archive.leapmotion.com/documentation/csharp/devguide/Leap_SDK_Overview.html)

* [LMC Python 3](https://github.com/BlackLight/leap-sdk-python3)
---
