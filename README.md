# Installation:
```bash
git clone https://github.com/fives03/Etech_projekt
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate # für linux/mac systeme
```
```bash
venv\Scripts\Activate.ps1 # für windows systeme
```

```bash
pip install -r requirements.txt
```

> tkinter muss extra und global installiert werden, für ubuntu:
```bash
sudo apt-get install python3-tk
```

# Start:
```bash
python3 wave_simulation.py
```



In meinem Projekt habe ich die aus der Vorlesung bekannten Reflektionen von Spannungswellen auf
parallelen Reitern betrachtet. Ziel war es die Spannung am Anfang und am Ende des Leiters zu
plotten und mit verschiedenen Wiederständen zu berechnen. Dabei ist es möglich einen
Reflektionswiederstand und einen Spannungsquellenwiederstand einzustellen. Ich habe zunächst
damit gestartet die Berechnungen vorzunehmen und diese in Funktionen zu verpacken. Dannach
habe ich mich mit dem Plotten der Daten beschäftigt und eine Input GUI gebaut.
