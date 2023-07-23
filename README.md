# Projektübersicht - photobox
Willkommen. In dieser Repository geht es um eine Fotobox mit einer Website.
Wir haben diese auf einem Raspberry Pi 3b+ gehostet, aber andere Modelle gehen hier sicherlich auch.
Unsere Kamera ist hier eine GoPro HERO 4, welche ein WLAN-Netz eröffnet, indem sich der Raspberry Pi einloggen kann.
Der Raspberry Pi ist per LAN-Kabel mit einem Router verbunden, da alle gemachten Bilder auf einem online gehosteten Server hochgeladen werden.
Von dort aus kann ein QR-Code erstellt werden, sodass man die Bilder direkt an der Fotobox über einen QR-Code online erreichen kann.
Die alternative zum QR-Code ist die Sendung über eine E-Mail, hier wird das Foto einmal als Anhang, und zusätzlich der Link zur Website gesendet.

:handshake:	Eine Zusammenarbeit zwischen [@JonnyTutorials](https://github.com/jonnytutorials) und [@EasyTecRepository](https://github.com/easytecrepository)

## Was wird benötigt?
- Raspberry Pi (3b+)[^1]
- GoPro (HERO 4[^1]
[^1]: Andere Modelle wurden nicht getestet, können aber auch funktionieren

## Wie wird es installiert?

Schaue dir doch dieses YouTube Video an, hier wird alles erklärt. :point_right:
**[Erklärvideo auf YouTube](https://youtube.com/EasyTec100)**

### Online Webspace (Download-Server)
1. Dateien von GitHub herunterladen (https://github.com/EasyTecRepository/photobox/archive/refs/heads/main.zip)
2. Ordner "file-host-api" entpacken
3. Python3 installieren `sudo apt-get install python3 python3-pip`
4. Abhängigkeiten installieren `pip install -r requirements.txt`
5. 

### Website (Lokal auf Raspberry Pi)
1. Dateien von GitHub herunterladen `git clone https://github.com/EasyTecRepository/photobox.git`
2. 


## Quellenangabe der verwendeten Icons

> autor: [paonkz](https://www.flaticon.com/authors/paonkz) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/qr-code-scan_8618309?term=qr-code&page=1&position=4&origin=tag&related_id=8618309)

> autor: [freepik](https://www.flaticon.com/authors/freepik) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/mail_646094?term=mail&page=1&position=2&origin=tag&related_id=646094)
