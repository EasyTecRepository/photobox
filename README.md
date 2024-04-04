# Projektübersicht - photobox
![](https://img.shields.io/badge/Status-Abgeschlossen-green)
![](https://img.shields.io/badge/Test-Ausstehend-orange)

Willkommen. In dieser Repository geht es um eine Fotobox mit einer Website.
Wir haben diese auf einem Raspberry Pi 3b+ gehostet, aber andere Modelle gehen hier sicherlich auch.
Unsere Kamera ist hier eine GoPro HERO 4, welche ein WLAN-Netz eröffnet, indem sich der Raspberry Pi einloggen kann.
Der Raspberry Pi ist per LAN-Kabel mit einem Router verbunden, da alle gemachten Bilder auf einem online gehosteten Server hochgeladen werden.
Von dort aus kann ein QR-Code erstellt werden, sodass man die Bilder direkt an der Fotobox über einen QR-Code online erreichen kann.
Die alternative zum QR-Code ist die Sendung über eine E-Mail, hier wird das Foto einmal als Anhang, und zusätzlich der Link zur Website gesendet.

:handshake:	Eine Zusammenarbeit zwischen [@JonnyTutorials](https://github.com/jonnytutorials) und [@EasyTecRepository](https://github.com/easytecrepository)

> [!WARNING]
> Beachte: Alle Fotos die über die Weboberfläche übertragen werden sind im Netzwerk unverschlüsselt!
> Unbefugte könnten diese Fotos im Netzwerk leicht abfangen.

> [!NOTE]
> Beachte: Die WLAN-Karte des Pi's wird benötigt um sich mit der GoPro zu verbinden.
> Zudem wird eine LAN-Verbindung benötigt, um die Oberfläche bereitzustellen.

## Was wird an Hardware benötigt?
- Raspberry Pi (3b+)[^1] (mit WLAN-Modul)
- GoPro (HERO 4)[^1]
- Bildschirm o.ä. zum anzeigen der Website
[^1]: Andere Modelle wurden nicht getestet, können aber auch funktionieren

## Wie wird es installiert?

Schaue dir doch dieses YouTube Video an, hier wird alles erklärt. :point_right:
**[Erklärvideo auf YouTube](https://youtube.com/EasyTec100)**

### Online Webspace (Download-Server)
WICHTIG: Der Download Server muss nach außen freigegeben sein! Zudem sollte eine gültige Domain vorhanden sein.
1. Abhängigkeiten installieren `sudo apt-get install python3 python3-pip git screen`
2. Dateien für den File Host Server herunterladen `git clone https://github.com/EasyTecRepository/photobox.git`
3. Ordner "download-server" öffnen `cd photobox/download-server`
4. Abhängigkeiten installieren `pip3 install -r requirements.txt`
5. Konfiguration anpassen `nano config.json`
6. SSL-Zertifikat generieren `certbot certonly -m deine@email.com -d deine.domain.tld`<br>Alternativ kann das SSL-Zertifikat weggelassen werden. Dazu einfach in der `config.json` `ssl-> enabled` auf `false` setzen. **Wird nicht empfohlen und birgt ein Sicherheitsrisiko!**


Variable | Beschreibung | Typ
:------:|-------------|:-----:
photo_dir|Verzeichnis, in dem die Fotos gespeichert werden|Pfad[string]
qr_dir|Verzeichnis, in dem die QR-Codes gespeichert werden|Pfad[string]
port|Port für den Download-Server|Port[intiger]
token_hash|Das Kommunikationspasswort zwischen der Lokalen API Schnittstelle und dem Download Server. Erstelle ein Passwort und Trage es [hier](https://coding.tools/sha256) ein. Das gehashte Passwort kannst du nun in die Konfiguration eintragen. Das ungehashte bitte für später bereithalten ;)|sha256 Hash[string]
host|IP oder Domain deines Servers|Domain/IP[string]
public_url|Öffentliche URL deines Servers|http(s)://Domain/IP[string]
ssl-> enabled|Schaltet das Bentuzen des SSL-Zertifikates ein und aus.|true/false[boolean]
ssl-> key|Pfad zum Key deines SSL-Zertifikates|Pfad[string]
ssl-> cert|Pfad zum Zertifikat deines SSL-Zertifikates|Pfad[string]

7. App starten `screen -dmS download-server python3 main.py`


### Backend (Lokal auf Raspberry Pi)
1. Abhängigkeiten installieren `sudo apt-get install python3 python3-pip git screen npm node apache2`
2. Dateien für lokale Schnittstelle herunterladen `git clone https://github.com/EasyTecRepository/photobox.git`
3. Ordner "backend" öffnen `cd photobox/local/backend`
4. Abhängigkeiten installieren `pip3 install -r requirements.txt`
5. Konfiguration anpassen `nano settings.py`

Variable | Beschreibung | Typ
:------:|-------------|:-----:
photos_path|Verzeichnis, in dem die Fotos gespeichert werden|Pfad[string]
api_port|Port auf dem das Lokale API erreichbar ist|Port[intiger]
FileHost-> url|URL zum bereits konfiguriertem Download-Server|http(s)://Host:Port[string]
FileHost-> key|Ungehashtes Kommunikationspasswort, das vorhin vergeben wurde|Passwort[string]
Mail-> smtp_server|Serveradresse zum SMTP-Server deines Anbieters|Host[string]
Mail-> smtp_port|Port zum SMTP-Server deines Anbieters|Port[intiger]
Mail-> smtp_mail|E-Mail Adresse deines Mail Accounts|E-Mail-Adresse[string]
Mail-> smtp_passwd|Passwort des Mail Accounts|Passwort[string]

6. App starten `screen -dmS backend python3 main.py`
7. Verzeichnis verlassen `cd ..`

### Website (Lokal auf Raspberry Pi)
1. Ordner "web" öffnen `cd photobox/local/web`
2. Module installieren `npm i`
3. Konfiguration anpassen `nano src/config.json`

Variable | Beschreibung | Typ
:------:|-------------|:-----:
api_endpoint|Url für das Lokale API|http://{Lokale IP deines Raspberry PIs}:{Port der in der settings.py vergeben wurde}[string]

4. Website kompilieren `npm run build`
5. Website ins Webserver-Verzeichnis verschieben und Zugriffsrechte anpassen `mkdir /var/www/html/photobox && cp -R build/ /var/www/html/photobox && chown -R www-data:www-data /var/www/html/photobox/`
6. Webserver starten `sudo systemctl start apache2`

**Glückwunsch! Deine Photobox ist nun unter `http://{Lokale IP deines Raspberry PIs}/photobox/` erreichbar.**

## Quellenangabe der verwendeten Icons

> autor: [paonkz](https://www.flaticon.com/authors/paonkz) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/qr-code-scan_8618309?term=qr-code&page=1&position=4&origin=tag&related_id=8618309)

> autor: [freepik](https://www.flaticon.com/authors/freepik) - 
> [bild](https://www.flaticon.com/de/kostenloses-icon/mail_646094?term=mail&page=1&position=2&origin=tag&related_id=646094)
