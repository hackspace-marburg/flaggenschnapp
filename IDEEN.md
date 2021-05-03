tl;dr: alles nicht komplett, zerstückelt, keine Garantie auf brennde Compiler und amoklaufende Toaster. Lose Ideensammlung für potentielle Rätsel.

# riddle
Programmierrätsel 

# Ideen:

## leicht
* ROT13-alike
* files mit irreführender Endung, zb ein `*.zip` als `*.tar` benennen
* pgp encryption
* mit Polynomen Bilder zeichnen
* dictionary / brute force Passwordattacken 
* Texte mittels Wort/Buchstabenhäufigkeit zurückrechnen
* Polynom/Primfaktorisierung
* Code in exotischen Programmiersprachen wie [Ook!](https://de.wikipedia.org/wiki/Ook!) oder [Brainfuck](https://de.wikipedia.org/wiki/Brainfuck)
* nummernfolgen fortsetzen
* google maps Koordinaten
* QR-Codes / Prüfsummen
* sodoku bruteforce
* Wegsuche im Graphen, besuchte Knoten ergeben Codewort
* text encoded Maze, auf kürzestem Pfad liegen Buchstaben, die ein Codewort ergeben 
* pyfiglet
* SSH Server mit nicht standard port + ssh key login

## schwer
* RC4-alike
* asymmetrische Krypto
* Manipulation von Binaries, zb Sprungadressen / Checksummen manipulieren
* Verschlüsselungsalgorithmen erraten
* einen präparierten Webserver (zb im VPN) "hacken", wie bei diesen "hack the box" games
* Programme, die in einer naiven Implementation Ewigkeiten laufen, mit einem Trick aber nur sehr kurz
* Steganographie
* defekte QR-Codes / Prüfsummen
* Hinweise in docker containern / virtuellen Maschinen verstecken


## diskutabel
* physische Hinweise, wie zb an `$ORT` Bilder aufzuhängen

## nützliche Links


## version2

* fünfteiliges Rätsel
* verschlüsselt string "sende eine Mail an X mit Betreff Y"
** Absender der ersten Mail gewinnt
* Summe aller Teilantworten ergibt pgp key

* Bei jedem Rätsel purzelt der Endpunkt des nächsten Rätsels raus, dazu ein fünftel des Endkeys
* alle Endpunkte sind von Anfang an da, die usernamen/Passwörter werden im transmitter o.ä. bekanntgegeben


# Teil 0
* user soll mailaddresse in api registrieren
* bekommt dafür zwei Dinge:
** Cyphertext, dieser kann erst ganz am Ende mit PGP key entschlüsselt werden, verschlüsselt mit unique PGP key für user
** Addresse Endpunkt Teil 1

# Teil 1
* login mit username + passwort. Passwort für alle gleich, username = registrierte Mailaddresse
* liefert ROT13 cyphertext
  * api endpunkt für Teil2



# Teil 2
# Teil 3
# Teil 4
# Teil 5


