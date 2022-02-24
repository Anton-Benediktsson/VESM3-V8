# VESM3-Vorönn-2022-Pong
Lokaverkefni í Verksmiðju 3
# Lýsing 
Stefna verkefnsins er að búa til tveggja manna pingpong leik á LED skjá sem er stýrður af Leap Motion tækni í gegnum vefþjónustu sem heldur einnig uppá stigafjölda á vefsíðu.

---
# Leap motion controller

## Að setja upp
 Til að setja upp 

## Python 3
 Vandamálið með python 3 á leap motion controller er að leap motion virkar ekki á python 3. Lausnin á þessu er að taka saman Leap sdk uppá nýtt með swig.

 Ég notaði [Leap sdk Python3](https://github.com/BlackLight/leap-sdk-python3) til að gera þetta en því að ég notaði Swig 4.0.2 þá virkaði það ekki því að það var `__swig_getmethods__` og `_swig_property` þessar línur eru sammt ekki mikilvægar svo það var hægt að taka það út ég tók í burtu. Sjáðu **leap-modified** í code/ á línu 830, 885, 1317.
 
---
# Myndbönd #


---
# Kóði #
 
* [Adafruit Matrix library](https://github.com/hzeller/rpi-rgb-led-matrix)
 
* [LMC Python 3](https://github.com/BlackLight/leap-sdk-python3)
---
