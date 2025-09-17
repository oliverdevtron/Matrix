# Matrix Text-Adventure

Ein textbasiertes Adventure-Spiel inspiriert von "The Matrix" und der Hacker-Kultur der 80er/90er Jahre.

## Beschreibung

Dieses Spiel versetzt den Spieler in die Rolle eines Hackers im Jahr 1999, der mysteriöse Anomalien in digitalen Systemen entdeckt. Durch die Erkundung einer düsteren Cyberpunk-Welt, das Lösen von Rätseln und das Bestehen von Hacking-Minispielen deckt der Spieler nach und nach die Wahrheit über die "Matrix" auf.

## Features

- Klassisches textbasiertes Adventure-Gameplay
- Immersive Cyberpunk-Atmosphäre mit Retro-Computing-Elementen
- Interaktive Hacking-Minispiele
- Dynamisches Alert-Level-System für zusätzliche Spannung
- Mehrere Orte zum Erkunden und NPCs zum Interagieren
- Rätsel und verschlüsselte Nachrichten

## Installation

1. Stellen Sie sicher, dass Python 3.6 oder höher installiert ist
2. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/oliverdevtron/Matrix.git
   cd Matrix
   ```

## Spielstart

```bash
python3 Matrix_v2.0.py
```

## Spielanleitung

### Grundlegende Befehle

- `GEHE [RICHTUNG]` oder `G [RICHTUNG]` - Bewegt sich zu einem anderen Ort
- `NIMM [GEGENSTAND]` oder `N [GEGENSTAND]` - Nimmt einen Gegenstand auf
- `SCHAU` oder `L` - Betrachtet die Umgebung
- `SCHAU [OBJEKT]` - Betrachtet ein bestimmtes Objekt genauer
- `BENUTZE [GEGENSTAND/OBJEKT]` oder `U [GEGENSTAND/OBJEKT]` - Benutzt einen Gegenstand oder interagiert mit einem Objekt
- `INVENTAR` oder `I` - Zeigt das Inventar an
- `HILFE` oder `?` - Zeigt alle verfügbaren Befehle an

### Erweiterte Befehle

- `HACKE [ZIEL]` - Startet einen Hacking-Versuch
- `DEKRYPTIERE [WAS] MIT [SCHLÜSSEL]` - Entschlüsselt Nachrichten
- `REDE MIT [PERSON]` - Spricht mit NPCs
- `LIES [GEGENSTAND]` - Liest Texte oder Dokumente
- `CODE [NUMMER]` - Gibt Codes an Numpads ein
- `SCANNE [ZIEL]` - Führt Netzwerk-Scans durch

### Spieltipps

- Erkunden Sie alle verfügbaren Orte gründlich
- Sammeln Sie alle Gegenstände, die Sie finden können
- Achten Sie auf Hinweise in Texten und Gesprächen
- Das Alert-Level steigt bei verdächtigen Aktivitäten - seien Sie vorsichtig!
- Experimentieren Sie mit verschiedenen Befehlskombinationen

## Spielwelt

Das Spiel beginnt in Ihrem Apartment und erweitert sich auf verschiedene Orte:

- **Apartment** - Ihr Zuhause mit Computer und mysteriösen Nachrichten
- **Straße** - Die nasse Straße vor Ihrem Haus mit einer Telefonzelle
- **Cyber Cafe** - Ein düsterer Ort mit Terminals und zwielichtigen Gestalten
- **Telefonzelle** - Eine alte Telefonzelle, die wichtige Anrufe empfangen könnte
- **Kaninchenbau Forum** - Ein verstecktes Online-Forum für Hacker
- **Server-Farm** - Ein gesichertes Gebäude mit wichtigen Servern

## Technische Details

- Geschrieben in Python 3
- Keine externen Abhängigkeiten erforderlich
- Textbasierte Benutzeroberfläche
- Plattformübergreifend (Windows, macOS, Linux)

## Mitwirkende

Entwickelt von Oliver

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## Changelog

### Version 2.0
- Vollständige Implementierung des Grundspiels
- Alle Hauptorte und NPCs implementiert
- Hacking-Minispiele hinzugefügt
- Alert-Level-System implementiert
- Verschlüsselungs-/Entschlüsselungsmechaniken

