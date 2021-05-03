UBER Rätsel API incomming

# generelle Idee
* es wird eine Framework bereitgestellt, mit der wir capture the flag implementieren
* user registrieren sich (ub mit uuid o.ä., muss nicht Mail sein), dies dient dem Zweck, die Rätsel für jeden user unique zu rendern
* es gibt `n` Rätsel APIs, das Lösen eines Rätsels stellt den Schlüssel/URL/Hinweis für das nachfolgende Rätsel bereit

# partizipieren
* flaggenschnapp stellt nützliche Funktionen bereit
* Menschen nutzen `$boilerplate.py` (selbstverständlich ToDO), um ihre eigenen Rätsel zu implementieren
** Bonuspunkte für Testroutinen
* Patches bitte via Mail an `...TODO...`
* "sei kein Arschloch" TM

# Probleme:
* Wie können wir trotz bekanntem Code ein reverse engineering / lokales bruteforcen verhindern?

# ToDo
* [ ] API verschlanken
* [ ] API dokumentieren
* [ ] example(s) (TM) bauen
* [ ] example test bauen
* [ ] boilerplate.py bauen
* [ ] mailaddresse klicken

# Bonuspunkte
* [ ] ratelimiting
* [ ] prometheus exporter (gather all the metrics!!1!)
* [ ] sinnvolles logging
