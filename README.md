# Projektübersicht - photobox
![](https://img.shields.io/badge/Status-In_Entwicklung-orange)

Willkommen. In dieser Repository geht es um eine Fotobox mit einer Website.
Wir haben diese auf einem Raspberry Pi 3b+ gehostet, aber andere Modelle gehen hier sicherlich auch.
Unsere Kamera ist hier eine GoPro HERO 4, welche ein WLAN-Netz eröffnet, indem sich der Raspberry Pi einloggen kann.
Der Raspberry Pi ist per LAN-Kabel mit einem Router verbunden, da alle gemachten Bilder auf einem online gehosteten Server hochgeladen werden.
Von dort aus kann ein QR-Code erstellt werden, sodass man die Bilder direkt an der Fotobox über einen QR-Code online erreichen kann.
Die alternative zum QR-Code ist die Sendung über eine E-Mail, hier wird das Foto einmal als Anhang, und zusätzlich der Link zur Website gesendet.

:handshake:	Eine Zusammenarbeit zwischen [@JonnyTutorials](https://github.com/jonnytutorials) und [@EasyTecRepository](https://github.com/easytecrepository)

## Was wird benötigt?
- Raspberry Pi (3b+)[^1]
- GoPro (HERO 4)[^1]
[^1]: Andere Modelle wurden nicht getestet, können aber auch funktionieren

## Wie wird es installiert?

Schaue dir doch dieses YouTube Video an, hier wird alles erklärt. :point_right:
**[Erklärvideo auf YouTube](https://youtube.com/EasyTec100)**

### Online Webspace (Download-Server)
WICHTIG: Der Download Server muss nach außen freigegeben sein! Zudem wird ein gültiges SSL-Zertifikat und bestenfalls eine Domain benötigt!
1. Abhängigkeiten installieren `sudo apt-get install python3 python3-pip git screen`
2. Dateien für den File Host Server herunterladen`git clone https://github.com/EasyTecRepository/photobox.git`
3. Ordner "file-host-api" öffnen `cd photobox/download-server`
4. Abhängigkeiten installieren `pip3 install -r requirements.txt`
5. Konfiguration anpassen `nano config.json`

Variable | Beschreibung
:------:|-------------
photo_dir|Verzeichnis, in dem die Fotos 
qr_dir|Verzeichnis, in dem die QR-Codes gespeichert werden
token_hash|Das Kommunikationspasswort zwischen der Lokalen API Schnittstelle und dem Download Server. Erstelle ein Passwort und Trage es [hier](https://coding.tools/sha256) ein. Das gehashte Passwort kannst du nun in die Konfiguration eintragen. Das ungehashte bitte für später bereithalten ;)
host|IP oder Domain deines Servers
ssl-> key|Pfad zum Key deines SSL-Zertifikates
ssl-> cert|Pfad zum Zertifikat deines SSL-Zertifikates

6. App starten `screen -dmS download-server python3 main.py`

### Website (Lokal auf Raspberry Pi)
1. Abhängigkeiten installieren `sudo apt-get install python3 python3-pip git screen npm node`
2. Dateien für lokale Schnittstelle herunterladen `git clone https://github.com/EasyTecRepository/photobox.git`
3. Ordner "file-host-api" öffnen `cd photobox/local/backend`
4. **Kommt noch ;)** ...


## Quellenangabe der verwendeten Icons

> autor: [paonkz](https://www.flaticon.com/authors/paonkz) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/qr-code-scan_8618309?term=qr-code&page=1&position=4&origin=tag&related_id=8618309)

> autor: [freepik](https://www.flaticon.com/authors/freepik) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/mail_646094?term=mail&page=1&position=2&origin=tag&related_id=646094)
