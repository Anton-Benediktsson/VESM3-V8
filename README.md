# VESM3-Vorönn-2022-Pong
Lokaverkefni í Verksmiðju 3
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
