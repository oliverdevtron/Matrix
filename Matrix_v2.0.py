# Ein textbasiertes Adventure-Spiel im Stil der 80er/90er Jahre, inspiriert von "The Matrix"
# von den Anfängen der Computer- und Hackerkultur.
import time
import textwrap
import random
import sys
import os

# --- Konstanten ---
WIDTH = 70  # Breite für Textumbruch

# --- Hilfsfunktionen ---
def clear_screen():
  """Löscht den Bildschirm (funktioniert auf den meisten Systemen)."""
  os.system('cls' if os.name == 'nt' else 'clear')

def wrap_text(text):
  """Bricht Text für die Konsolenausgabe um."""
  return "\n".join(textwrap.wrap(text, WIDTH))

def print_slow(text, delay=0.03):
  """Gibt Text langsam aus, Zeichen für Zeichen."""
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(delay)
  print() # Zeilenumbruch am Ende

def print_c64_header():
  """Zeigt den C64-Startbildschirm."""
  clear_screen()
  print_slow("    **** C=64 ZEITMASCHINE ****")
  print_slow(" 64K RAM SYSTEM 38911 BASIC BYTES FREE")
  print()
  print_slow("READY.")
  time.sleep(1)
  # Simuliert Laden
  print_slow("LOAD\"*\",8,1")
  time.sleep(0.5)
  print_slow("SEARCHING FOR *")
  time.sleep(1.5)
  print_slow("LOADING...")
  time.sleep(2)
  print_slow("READY.")
  print_slow("RUN")
  print("-" * WIDTH)
  time.sleep(1.5)
  clear_screen()

def get_player_input():
  """Fragt den Spieler nach Eingabe und bereinigt sie."""
  command = input("\nWAS TUN?> ").strip().upper()
  return command

# --- Spielwelt Daten ---

locations = {
    'APARTMENT': {
        'name': 'DEIN APARTMENT',
        'description': ("EIN SCHLICHTER RAUM MIT EINEM ALTEN BETT, EINEM UEBERLADENEN SCHREIBTISCH "
                        "UND DEINEM TREUEN HEIMCOMPUTER. DAS FENSTER ZEIGT EINE REGENERISCHE STRASSE. "
                        "AUF DEM SCHREIBTISCH LIEGT EIN ZETTEL."),
        'items': ['ZETTEL'],
        'interactables': ['COMPUTER', 'FENSTER', 'BETT'],
        'exits': {'RAUS': 'STRASSE'},
        'details': {
            'COMPUTER': "DEIN ALTER HEIMCOMPUTER. EIN TURBO-XT Klon. BEREIT FUER BEFEHLE.",
            'FENSTER': "DU SCHAUST HINAUS AUF DIE NASSE STRASSE. DIE STADT SCHLAEFT NIE.",
            'BETT': "EIN EINFACHES BETT. NICHT SEHR BEQUEM.",
            'ZETTEL': "EIN VERGILBTER ZETTEL MIT EINER HANDGESCHRIEBENEN NOTIZ."
        },
        'first_visit': True
    },
    'STRASSE': {
        'name': 'STRASSE VOR DEM HAUS',
        'description': ("DU STEHST AUF DEM NASSEN GEHSTEIG. DER REGEN HAT AUFGEHOERT. LINKS IST EINE TELEFONZELLE, "
                        "RECHTS GEHT ES ZUM 'CYBER CAFE'. HINTER DIR IST DEIN APARTMENTHAUS."),
        'items': [],
        'interactables': ['TELEFONZELLE'],
        'exits': {'CAFE': 'CAFE', 'ZURUECK': 'APARTMENT', 'TELEFONZELLE': 'TELEFONZELLE_INNERES'},
        'details': {
            'TELEFONZELLE': "EINE VERWITTERTE, ALTMODISCHE TELEFONZELLE. SIEHT FUNKTIONSFAEHIG AUS.",
        }
    },
    'CAFE': {
        'name': 'CYBER CAFE',
        'description': ("DAS 'CYBER CAFE' IST DUNKEL UND RIECHT NACH ALTEM KAFFEE UND OZON VON DEN MONITOREN. "
                        "EIN PAAR GESTALTEN SITZEN AN TERMINALS. HINTER DER THEKE STEHT EIN MANN MIT SPIEGELNDER SONNENBRILLE, "
                        "AUCH NACHTS. DU KANNST ZURUECK AUF DIE STRASSE."),
        'items': [],
        'interactables': ['MANN', 'TERMINAL', 'GESTALTEN'], # GESTALTEN hinzugefügt
        'exits': {'RAUS': 'STRASSE'},
        'details': {
             'MANN': "DER MANN POLIERT SEINE SONNENBRILLE. ER MUSTERT DICH KUEHL. 'WAS WILLST DU, NEULING?'",
             'TERMINAL': "EIN OEFFENTLICHES TERMINAL. KOSTET 1 MARK PRO MINUTE.",
             'GESTALTEN': "SIE SCHEINEN VERTIEFT IN IHRE ARBEIT ZU SEIN. EINER HAT EIN SILBERNES IMPLANTAT AM HALS." # Kleine Überraschung/Andeutung
        },
        'npcs': ['MANN']
    },
    'TELEFONZELLE_INNERES': {
        'name': 'IN DER TELEFONZELLE',
        'description': ("ES IST ENG HIER DRIN. DAS TELEFON SIEHT ALT AUS, ABER EIN LICHT LEUCHTET. "
                       "DER HOERER LIEGT NEBEN DEM APPARAT. DU KANNST WIEDER RAUS."),
        'items': [],
        'interactables': ['TELEFON', 'HOERER'],
        'exits': {'RAUS': 'STRASSE'},
        'details': {
            'TELEFON': "EIN ALTES WAEHLSCHEIBENTELEFON. EINE GRUENE LED LEUCHTET NEBEN DEM MUENZSCHLITZ.",
            'HOERER': "DER SCHWARZE HOERER AUS BAKELIT. ER IST NICHT AUFGELEGT."
        }
    },
     'SERVER_FARM_EINGANG': {
        'name': 'VOR DER SERVER-FARM',
        'description': "DU STEHST VOR EINEM UNANSEHNLICHEN GEBAEUDE OHNE FENSTER. EINE SCHWERE METALLTUER IST DER EINZIGE EINGANG. NEBEN DER TUER IST EIN KARTENLESER UND EIN NUMPAD.",
        'items': [],
        'interactables': ['TUER', 'KARTENLESER', 'NUMPAD'],
        'exits': {'ZURUECK': 'STRASSE'}, # Annahme: Man kommt von der Strasse hierher (muss noch eingebaut werden, z.B. neue Straße oder Gasse)
        'details': {
            'TUER': "EINE SCHWERE, VERSTAERKTE STAHLTUER. KEIN GRIFF VON AUSSEN.",
            'KARTENLESER': "EIN STANDARD-MAGNETSTREIFENLESER.",
            'NUMPAD': "EIN NUMPAD ZUR CODE-EINGABE."
        }
    },
    'KANINCHENBAU_FORUM': {
        'name': 'DAS "KANINCHENBAU" FORUM',
        'description': "DU BIST IM VERSTECKTEN ONLINE-FORUM 'KANINCHENBAU'. TEXT ZEILEN FLIMMERN UEBER DEN SCHIRM. ES GIBT BEREICHE FUER 'NACHRICHTEN', 'GERUECHTE' UND EINEN PRIVATEN BEREICH DER 'ORACLE'.",
        'items': [],
        'interactables': ['NACHRICHTEN', 'GERUECHTE', 'ORACLE'],
        'exits': {'LOGOUT': 'APARTMENT'}, # Zurück zum Computer im Apartment
        'details': {
            'NACHRICHTEN': "'SYSTEM SCAN LAEUFT...', 'NEUE FIREWALL REGELN AKTIV...', 'ACHTUNG: AGENTEN-AKTIVITAET HOCH'",
            'GERUECHTE': "'HABE EINEN GLITCH GESEHEN...', 'WER IST MORPHEUS?', 'DIE MATRIX HAT DICH...'",
            'ORACLE': "ZUGANG GESPERRT. BENOETIGT AUTHENTIFIZIERUNG."
        },
        'requires_computer': True # Man kann nur vom Computer hierher
    }
    # Weitere Orte können hier hinzugefügt werden
    # Beispiel: Eine Gasse, die zur Serverfarm führt
    # 'GASSE': { ... }
    # Dann 'STRASSE': { ... 'exits': {'CAFE': 'CAFE', 'ZURUECK': 'APARTMENT', 'TELEFONZELLE': 'TELEFONZELLE_INNERES', 'GASSE': 'GASSE'}, ...}
    # Und 'SERVER_FARM_EINGANG': { ... 'exits': {'ZURUECK': 'GASSE'}, ...}
}

items = {
    'ZETTEL': {
        'name': 'ZETTEL',
        'description': "Eine Notiz mit der Aufschrift: 'PASSWORT HINWEIS: Der erste grosse Film des Regisseurs von 'Bound'. Alles klein geschrieben.'",
        'location': 'APARTMENT',
        'can_take': True
    },
    'DATEN_DISKETTE': {
        'name': 'DATEN DISKETTE',
        'description': "Eine 3.5 Zoll Diskette. Beschriftet mit 'PROTOKOLL 7'.",
        'location': None, # Startet nicht im Spiel, muss gefunden werden (z.B. nach Hack im Cafe?)
        'can_take': True
    },
    'SCHLUESSELKARTE': {
        'name': 'SCHLUESSELKARTE',
        'description': "Eine abgenutzte Magnetstreifenkarte. Sieht aus wie eine Zugangskarte.",
        'location': None, # Bekommt man vom Mann im Cafe
        'can_take': True
    }
    # Weitere Items
}

# --- Spielzustand ---

game_state = {
    'current_location': 'APARTMENT',
    'player_inventory': [],
    'alert_level': 0, # 0 = niedrig, 7 = sehr hoch (Game Over)
    'known_codeword': None, # Für die erste Nachricht
    'computer_logged_in': False,
    'decrypted_message_content': None,
    'apartment_password_cracked': False,
    'oracle_contacted': False,
    'met_cypher': False,
    'phone_ringing': False, # Überraschung: Das Telefon könnte klingeln
    'first_message_received': False,
    'server_farm_access_code': "1999", # Beispiel-Code, wird ggf. im Spiel 'entdeckt'
    'server_farm_hacked': False, # Flag für erfolgreichen Port-Scan
    'server_farm_card_used': False, # Flag für Benutzung der Karte am Leser
    'server_farm_code_correct': False, # Flag für korrekte Code-Eingabe
    'server_farm_access_granted': False, # Flag wenn Karte UND Code korrekt
    'diskette_received': False # Um zu verhindern, dass die Diskette mehrmals gegeben wird
}

# --- Parser & Befehlsverarbeitung ---
def parse_command(command):
  """Zerlegt den Befehl in Verb und Argumente."""
  parts = command.split()
  if not parts:
    return None, None
  verb = parts[0]
  args = parts[1:]
  return verb, args

def handle_command(verb, args):
  """Verarbeitet den geparsten Befehl."""
  if verb in ['GEHE', 'G', 'LAUFE']:
    handle_go(args)
  elif verb in ['NIMM', 'NEHMEN', 'N']:
    handle_take(args)
  elif verb in ['SCHAU', 'UMSCHAUEN', 'L', 'LOOK']:
    handle_look(args)
  elif verb in ['BENUTZE', 'USE', 'U']:
    handle_use(args)
  elif verb in ['INVENTAR', 'INV', 'I']:
    handle_inventory()
  elif verb in ['HILFE', 'HELP', '?']:
    handle_help()
  elif verb in ['DEKRYPTIERE', 'DECRYPT']:
    handle_decrypt(args)
  elif verb in ['HACKE', 'HACK']:
      handle_hack(args)
  elif verb in ['REDE', 'SPRECHE', 'TALK']:
      handle_talk(args)
  elif verb in ['LIES', 'LESEN', 'READ']:
        handle_read(args)
  elif verb in ['OEFFNE', 'OPEN']: # Bspw. für Türen
        handle_open(args)
  elif verb in ['DRUECKE', 'PUSH']: # Bspw. für Knöpfe
        handle_push(args)
  elif verb in ['SCANNE', 'SCAN']: # Für Hacking-Minispiel
        handle_scan(args)
  elif verb in ['CODE', 'EINGABE']: # Für Numpad
        handle_code_input(args)
  elif verb == 'QUIT' or verb == 'EXIT' or verb == 'ENDE':
      print_slow("BIS BALD IM DIGITALEN NIRVANA...")
      sys.exit()
  else:
    # Versuch, mehrteilige Verben zu erkennen (z.B. "REDE MIT")
    if len(verb) > 0 and len(args) > 0:
        combined_verb = verb + " " + args[0]
        if combined_verb == "REDE MIT":
            handle_talk(args[1:])
            return
        elif combined_verb == "ONLINE GEHEN" and game_state['computer_logged_in']: # Sonderfall für Computer
             use_computer_command('ONLINE GEHEN')
             return

    print_slow("ICH VERSTEHE '{}' NICHT.".format(verb))

# --- Befehls-Handler ---
def display_location():
  """Zeigt die Beschreibung des aktuellen Ortes an."""
  loc_id = game_state['current_location']
  location = locations[loc_id]
  print("-" * WIDTH)
  print(f"ORT: {location['name']}")
  print("-" * WIDTH)
  # Beim ersten Betreten des Apartments die Einleitung zeigen
  if loc_id == 'APARTMENT' and location.get('first_visit', False):
      print_slow(wrap_text(
          "Du sitzt in deinem spartanisch eingerichteten Apartment. Dein CRT-Monitor flackert vor dir, "
          "die Tastatur deines alten Heimcomputers knistert leise unter deinen Fingern. Draussen pulsiert "
          "die anonyme Hektik der Grossstadt im Jahr 1999. Doch deine Welt spielt sich vor allem in den "
          "digitalen Schatten ab. Du bist ein talentierter, aber (bisher) unauffaelliger Hacker."
      ))
      print_slow(wrap_text(
          "In letzter Zeit hast du merkwuerdige Anomalien in den Systemen bemerkt – Glitches, die nicht "
          "erklaerbar sind, Codesequenzen, die keinen Sinn ergeben. Es ist, als wuerde etwas unter der "
          "Oberflaeche der digitalen Welt lauern."
      ))
      location['first_visit'] = False # Nur einmal anzeigen
      time.sleep(1)
      # Die erste Nachricht auslösen
      trigger_first_message()
  else:
      print_slow(wrap_text(location['description']))

  # Zeige sichtbare Gegenstände am Ort
  visible_items = [item_name for item_name, item_data in items.items()
                   if item_data['location'] == loc_id]
  if visible_items:
    print("\nDU SIEHST HIER:")
    for item_name in visible_items:
      print(f"- {item_name}")

  # Zeige mögliche Ausgänge
  exits = location.get('exits', {})
  if exits:
    print("\nMOEGLICHE AUSGAENGE:")
    print(", ".join(exits.keys()))

def handle_go(args):
  """Bewegt den Spieler zu einem anderen Ort."""
  if not args:
    print_slow("WOHIN SOLL ES GEHEN?")
    return

  direction = args[0] # Richtung oder Zielname
  loc_id = game_state['current_location']
  location = locations[loc_id]
  exits = location.get('exits', {})

  target_loc_id = None
  # Prüfe direkte Richtungen
  if direction in exits:
    target_loc_id = exits[direction]
  else:
    # Prüfe, ob ein Zielort direkt angesprochen wurde (z.B. "GEHE CAFE")
    for exit_name, dest_id in exits.items():
        if dest_id == direction: # Wenn der ZIELORT direkt als Befehl gegeben wird
            target_loc_id = dest_id
            break
        elif exit_name == direction: # Sollte eigentlich schon oben abgedeckt sein
             target_loc_id = dest_id
             break


  if target_loc_id:
    # Prüfe, ob der Zielort spezielle Bedingungen hat
    if locations[target_loc_id].get('requires_computer', False) and not game_state['computer_logged_in']:
        print_slow("DU MUSST DAFUER DEN COMPUTER BENUTZEN.")
        return
    # Logik für die Telefonzelle leicht angepasst: Man kann immer rein, aber nur wenn sie klingelt, passiert was beim Abheben.
    # if target_loc_id == 'TELEFONZELLE_INNERES' and not game_state['phone_ringing']:
    #    print_slow("DIE TELEFONZELLE IST STUMM. WARUM SOLLTEST DU HINEINGEHEN?")
    #    return # Kleine Hürde/Logik - Entfernt, um Erkundung zu ermöglichen

    # Spezielle Prüfung für Server-Farm-Eingang (Beispiel: Muss erst freigeschaltet werden?)
    # if target_loc_id == 'SERVER_FARM_EINGANG' and not some_condition:
    #     print_slow("DU KANNST DEN WEG ZUR SERVER-FARM NOCH NICHT FINDEN.")
    #     return

    game_state['current_location'] = target_loc_id
    display_location()
    # Event: Betreten der Telefonzelle während sie klingelt (Effekt beim Abheben)
    if target_loc_id == 'TELEFONZELLE_INNERES' and game_state['phone_ringing']:
        print_slow("Das Klingeln ist hier drinnen ohrenbetaeubend!")

  else:
    print_slow(f"DU KANNST NICHT NACH '{direction}' GEHEN.")


def handle_take(args):
    """Nimmt einen Gegenstand auf."""
    if not args:
        print_slow("WAS MOECHTEST DU NEHMEN?")
        return

    item_name_arg = " ".join(args).upper() # Falls Item-Namen Leerzeichen haben
    loc_id = game_state['current_location']
    found_item_name = None

    # Finde das Item am aktuellen Ort
    for item_id, item_data in items.items():
        if item_data['location'] == loc_id and item_id == item_name_arg:
             # Spezialfall für Zettel im Apartment (wenn Passwort schon geknackt)
            if item_id == 'ZETTEL' and game_state['apartment_password_cracked']:
                 print_slow("DU HAST DIE INFO VOM ZETTEL BEREITS VERWENDET. ER IST JETZT UNWICHTIG.")
                 return

            if item_data.get('can_take', False):
                found_item_name = item_id
                break
            else:
                print_slow(f"DU KANNST '{item_name_arg}' NICHT NEHMEN.")
                return

    if found_item_name:
        game_state['player_inventory'].append(found_item_name)
        items[found_item_name]['location'] = None # Aus der Welt entfernen
        print_slow(f"DU NIMMST: {found_item_name}")
        increase_alert_level(1) # Kleinigkeit aufheben ist minimal verdächtig
    else:
        print_slow(f"HIER GIBT ES KEIN '{item_name_arg}'.")

def handle_look(args):
  """Schaut sich den Ort oder einen Gegenstand genauer an."""
  loc_id = game_state['current_location']
  location = locations[loc_id]

  if not args:
    # Einfach nur 'SCHAU' -> Zeige die Ortsbeschreibung erneut detaillierter
    display_location()
    # Zeige Details zu Interactables
    if location.get('interactables'):
      print("\nINTERESSANTE DINGE HIER:")
      for thing in location['interactables']:
          # Prüfen ob das Ding noch 'da' ist (z.B. wenn es ein NPC ist, der weggehen könnte)
          is_npc = thing in location.get('npcs', [])
          is_item = thing in items and items[thing]['location'] == loc_id

          # Wenn es ein NPC ist oder KEIN Item (also ein festes Merkmal des Raums) oder ein Item AM ORT ist
          if is_npc or not is_item or (is_item and items[thing]['location'] == loc_id) :
              print(f"- {thing}")
              if thing in location.get('details', {}):
                   # Kurze Beschreibung in Klammern anzeigen
                   detail_text = location['details'][thing]
                   # Optional: Kürzen, wenn zu lang für eine Klammeranzeige
                   if len(detail_text) > 50:
                       detail_text = detail_text[:47] + "..."
                   print(f"  ({detail_text})")


  else:
    target_name = " ".join(args).upper()

    # Ist es ein Detail im Raum (Interactable oder NPC)?
    if target_name in location.get('details', {}):
      print_slow(wrap_text(location['details'][target_name]))
    # Ist es ein Gegenstand im Inventar?
    elif target_name in game_state['player_inventory']:
      print_slow(wrap_text(items[target_name]['description']))
    # Ist es ein Gegenstand am Ort?
    elif target_name in items and items[target_name]['location'] == loc_id:
         print_slow(wrap_text(items[target_name]['description']))
         # Spezieller Text für den Zettel, wenn man ihn anschaut
         if target_name == 'ZETTEL' and not game_state['apartment_password_cracked']:
              # Die Standardbeschreibung reicht hier, da sie den Hinweis enthält
              pass
         elif target_name == 'ZETTEL' and game_state['apartment_password_cracked']:
             print_slow("Die Schrift ist verwischt und kaum noch lesbar.")

    else:
      print_slow(f"DU SIEHST NICHTS BESONDERES AN '{target_name}'.")


def handle_read(args):
    """Liest einen Gegenstand."""
    if not args:
        print_slow("WAS MOECHTEST DU LESEN?")
        return

    item_name_arg = " ".join(args).upper()
    loc_id = game_state['current_location']

    # Ist es der Zettel am Ort?
    if item_name_arg == 'ZETTEL' and items['ZETTEL']['location'] == loc_id:
        if game_state['apartment_password_cracked']:
             print_slow("DU HAST DIE INFO VOM ZETTEL BEREITS VERWENDET. Die Schrift ist verwischt.")
        else:
            print_slow(f"DU LIEST DEN {item_name_arg}:")
            print_slow(wrap_text(items['ZETTEL']['description']))
        return
    # Ist es der Zettel im Inventar?
    elif item_name_arg == 'ZETTEL' and 'ZETTEL' in game_state['player_inventory']:
        if game_state['apartment_password_cracked']:
             print_slow("DU HAST DIE INFO VOM ZETTEL BEREITS VERWENDET. Die Schrift ist verwischt.")
        else:
            print_slow(f"DU LIEST DEN {item_name_arg} AUS DEINEM INVENTAR:")
            print_slow(wrap_text(items['ZETTEL']['description']))
        return
    # Ist es ein anderer lesbarer Gegenstand im Inventar?
    elif item_name_arg in game_state['player_inventory'] and item_name_arg in items:
         # Hier könnte man spezifische Logik für andere lesbare Items einfügen
         if item_name_arg == 'DATEN_DISKETTE':
              print_slow("DU KANNST EINE DISKETTE NICHT EINFACH SO LESEN. DU BRAUCHST EINEN COMPUTER. (BENUTZE COMPUTER, DANN LIES DISKETTE)")
         else:
            # Generische Lese-Aktion für andere Items, falls vorhanden
            if 'read_text' in items[item_name_arg]: # Wenn ein spezieller Lesetext definiert ist
                 print_slow(f"DU LIEST {item_name_arg}:")
                 print_slow(wrap_text(items[item_name_arg]['read_text']))
            else: # Ansonsten nur die Beschreibung anzeigen
                 print_slow(f"DU SCHAUST DIR {item_name_arg} AN:")
                 print_slow(wrap_text(items[item_name_arg]['description']))
         return
    # Ist es ein lesbares Objekt am Ort (z.B. Schild)?
    elif item_name_arg in locations[loc_id].get('details', {}):
        # Prüfen, ob es als 'lesbar' markiert ist oder einfach nur Text anzeigen
        print_slow(f"DU LIEST {item_name_arg}:")
        print_slow(wrap_text(locations[loc_id]['details'][item_name_arg]))
        return

    else:
        print_slow(f"DU KANNST '{item_name_arg}' NICHT LESEN ODER HAST ES NICHT.")


def handle_use(args):
  """Benutzt einen Gegenstand oder ein Objekt."""
  if not args:
    print_slow("WAS MOECHTEST DU BENUTZEN?")
    return

  target_name = args[0].upper()
  loc_id = game_state['current_location']
  location = locations[loc_id]

  # Fall 1: Benutze Computer
  if target_name == 'COMPUTER' and loc_id == 'APARTMENT':
    use_computer()
  # Fall 2: Benutze Telefon in der Zelle
  elif target_name == 'TELEFON' and loc_id == 'TELEFONZELLE_INNERES':
      use_phone()
  # Fall 3: Benutze Hoerer in der Zelle
  elif target_name == 'HOERER' and loc_id == 'TELEFONZELLE_INNERES':
      use_phone_receiver()
  # Fall 4: Benutze Gegenstand mit Objekt (z.B. BENUTZE KARTE MIT LESER)
  elif len(args) >= 3 and args[1].upper() in ['MIT', 'AN', 'AUF']: # Flexibler
      item_to_use = args[0].upper()
      target_object = " ".join(args[2:]).upper() # Rest ist das Objekt

      # Ist der Gegenstand im Inventar?
      if item_to_use not in game_state['player_inventory']:
          print_slow(f"DU HAST '{item_to_use}' NICHT.")
          return

      # Spezifische Interaktionen
      # Schlüsselkarte mit Kartenleser
      if item_to_use == 'SCHLUESSELKARTE' and target_object == 'KARTENLESER' and loc_id == 'SERVER_FARM_EINGANG':
          print_slow("DU ZIEHST DIE SCHLUESSELKARTE DURCH DEN LESER...")
          time.sleep(1)
          # Hier eine Erfolgschance einbauen oder es einfach funktionieren lassen
          print_slow("...EIN GRUENES LICHT BLINKT KURZ AUF. KARTE AKZEPTIERT.")
          game_state['server_farm_card_used'] = True
          increase_alert_level(1)
          # Prüfen, ob auch Code schon korrekt war
          if game_state.get('server_farm_code_correct', False):
               game_state['server_farm_access_granted'] = True
               print_slow("EIN KLICKEN IST ZU HOEREN. DIE TUER SCHEINT ENTSPERRT ZU SEIN. (VERSUCHE 'OEFFNE TUER')")
          else:
               print_slow("DIE KARTE WURDE AKZEPTIERT, ABER DIE TUER BLEIBT ZU. FEHLT NOCH DER CODE?")

      # Diskette mit Computer
      elif item_to_use == 'DATEN_DISKETTE' and target_object == 'COMPUTER' and loc_id == 'APARTMENT':
          if game_state['computer_logged_in']:
              print_slow("DU SCHIEBST DIE DISKETTE 'PROTOKOLL 7' IN DAS LAUFWERK.")
              # Hinweis, wie man sie liest (innerhalb der Computer-Interaktion)
              print_slow("(IM COMPUTER-MODUS KANNST DU JETZT 'LIES DISKETTE' EINGEBEN.)")
              increase_alert_level(1) # Zugriff auf unbekannte Daten
          else:
              print_slow("DU MUSST ZUERST DEN COMPUTER STARTEN/BENUTZEN (BENUTZE COMPUTER).")
      else:
          print_slow(f"DU KANNST '{item_to_use}' NICHT MIT '{target_object}' BENUTZEN.")

  # Fall 5: Benutze einfaches Interactable am Ort
  elif target_name in location.get('interactables', []):
       # Generische Nachricht oder spezifische Aktionen hier hinzufügen
       if target_name == 'TERMINAL' and loc_id == 'CAFE':
           print_slow("DU SETZT DICH AN DAS OEFFENTLICHE TERMINAL. ES RIECHT NACH STAUB UND NIKOTIN.")
           print_slow("ES VERLANGT NACH EINER ANMELDUNG ODER MUENZEN...")
           print_slow("(VIELLEICHT KANNST DU ES HACKEN? 'HACKE TERMINAL')")
           increase_alert_level(1)
       elif target_name == 'NUMPAD' and loc_id == 'SERVER_FARM_EINGANG':
            print_slow("DAS NUMPAD IST BEREIT FUER EINE EINGABE. (BENUTZE 'CODE [NUMMER]')")
       elif target_name == 'KARTENLESER' and loc_id == 'SERVER_FARM_EINGANG':
            print_slow("DER KARTENLESER WARTET AUF EINE KARTE. (BENUTZE 'SCHLUESSELKARTE MIT KARTENLESER')")
       elif target_name == 'FENSTER' and loc_id == 'APARTMENT':
            print_slow(wrap_text(location['details']['FENSTER'])) # Zeige einfach die Beschreibung
       elif target_name == 'BETT' and loc_id == 'APARTMENT':
             print_slow("DU SETZT DICH AUFS BETT. ES IST NICHT SEHR BEQUEM. AUSRUHEN?")
             # Hier könnte man eine 'warte' Funktion einbauen
       elif target_name == 'TELEFONZELLE' and loc_id == 'STRASSE':
           print_slow("DU RÜTTELST AN DER TÜR DER TELEFONZELLE. DU KÖNNTEST HINEINGEHEN ('GEHE TELEFONZELLE').")
       else:
           print_slow(f"DU VERSUCHST '{target_name}' ZU BENUTZEN, ABER NICHTS SINNVOLLES PASSIERT.")
  else:
    print_slow(f"DU KANNST '{target_name}' HIER NICHT BENUTZEN.")

def handle_inventory():
  """Zeigt das Inventar des Spielers an."""
  if not game_state['player_inventory']:
    print_slow("DU TRAEGST NICHTS BEI DIR.")
  else:
    print_slow("DU TRAEGST:")
    for item_name in game_state['player_inventory']:
      print(f"- {item_name}")

def handle_help():
  """Zeigt eine Liste möglicher Befehle."""
  print_slow("MOEGLICHE BEFEHLE SIND:")
  print_slow("- GEHE [RICHTUNG/ORT] (ODER G)")
  print_slow("- NIMM [GEGENSTAND] (ODER N)")
  print_slow("- SCHAU (UMSCHAUEN) [OBJEKT/RICHTUNG] (ODER L)")
  print_slow("- LIES [GEGENSTAND]")
  print_slow("- BENUTZE [GEGENSTAND/OBJEKT] (ODER U)")
  print_slow("- BENUTZE [GEGENSTAND] MIT/AN/AUF [OBJEKT]")
  print_slow("- INVENTAR (ODER I)")
  print_slow("- HACKE [ZIEL]")
  print_slow("- DEKRYPTIERE [WAS] MIT [SCHLUESSEL]")
  print_slow("- REDE MIT [PERSON]")
  print_slow("- SCANNE [ZIEL/PORTS]")
  print_slow("- CODE [NUMMER] (Fuer Numpads)")
  print_slow("- OEFFNE [TUER/OBJEKT]")
  # print_slow("- DRUECKE [KNOPF]") # Momentan nicht verwendet
  print_slow("- HILFE (?)")
  print_slow("- QUIT (ODER EXIT, ENDE)")

def handle_decrypt(args):
    """Versucht, etwas zu dekryptieren."""
    # Beispiel: DEKRYPTIERE NACHRICHT MIT REDPILL
    if len(args) < 3 or args[1].upper() != 'MIT':
        print_slow("BENUTZE: DEKRYPTIERE [WAS] MIT [SCHLUESSEL]")
        return

    target = args[0].upper()
    key = " ".join(args[2:]).upper() # Schlüssel kann mehrere Worte sein

    # Szenario 1: Erste Nachricht dekryptieren
    if target == 'NACHRICHT' and game_state['current_location'] == 'APARTMENT' and game_state['first_message_received'] and not game_state['decrypted_message_content']:
        # Das Codewort/Schlüssel (Groß-/Kleinschreibung ignorieren beim Vergleich)
        correct_key = 'REDPiLL'.upper() # Im Code immer Großbuchstaben verwenden für Konsistenz
        if key == correct_key:
            game_state['known_codeword'] = 'REDPiLL' # Spieler kennt das Wort (in Originalschreibweise speichern?)
            game_state['decrypted_message_content'] = "FOLGE DEM WEISSEN KANINCHEN."
            print_slow("DEKRYPTION ERFOLGREICH!")
            print_slow(f"NACHRICHT ENTSCHLUESSELT: '{game_state['decrypted_message_content']}'")
            print_slow("WAS BEDEUTET DAS NUR? VIELLEICHT EIN HINWEIS AUF EIN ONLINE FORUM?")
            increase_alert_level(1)
            # Möglicher Hinweis: Der Computer könnte jetzt für 'ONLINE GEHEN' genutzt werden
            print_slow("(VIELLEICHT KANNST DU JETZT MIT DEM COMPUTER 'ONLINE GEHEN'?)")
        else:
            print_slow("FALSCHER SCHLUESSEL. DEKRYPTION FEHLGESCHLAGEN.")
            increase_alert_level(1) # Versuch macht verdächtig
    # Hier könnten weitere Dekryptier-Rätsel eingefügt werden
    # elif target == 'PROTOKOLL 7' and 'DATEN_DISKETTE' in game_state['player_inventory'] and key == 'MORPHEUS':
    #    ... (Vielleicht muss die Diskette erst dekryptiert werden?)
    else:
        if target == 'NACHRICHT' and game_state['decrypted_message_content']:
             print_slow("DU HAST DIESE NACHRICHT BEREITS DEKRYPTIERT.")
        else:
             print_slow(f"ES GIBT HIER KEIN '{target}' ZUM DEKRYPTIEREN, DU HAST ES NICHT, ODER DER SCHLUESSEL IST FALSCH.")


def handle_hack(args):
    """Startet einen Hacking-Versuch."""
    if not args:
        print_slow("WAS MOECHTEST DU HACKEN?")
        return

    target = " ".join(args).upper()
    loc_id = game_state['current_location']

    # Szenario 1: Computer-Passwort im Apartment knacken (wird jetzt über 'BENUTZE COMPUTER' ausgelöst)
    # if target == 'COMPUTER' and loc_id == 'APARTMENT' and not game_state['apartment_password_cracked']:
    #    crack_apartment_password()

    # Szenario 2: Server-Farm Zugang (Port Scan Minispiel)
    if target in ['SERVER', 'SERVER-FARM', 'SERVERFARM', 'PORTS'] and loc_id == 'SERVER_FARM_EINGANG':
         # Hier könnte das Port-Scanning Minispiel starten
         start_port_scan_minigame()
    # Szenario 3: Terminal im Cafe
    elif target == 'TERMINAL' and loc_id == 'CAFE':
        print_slow("DU VERSUCHST, DIE ANMELDUNG DES TERMINALS ZU UMGEHEN...")
        time.sleep(1.5)
        if random.randint(1, 3) == 1: # Einfache Zufallschance
            print_slow("ERFOLG! DU HAST EINE TEMPORAERE SITZUNG ERLANGT.")
            print_slow("DU FINDEST EINE HERUM LIEGENDE DATEI 'TRANSFER.LOG'.")
            time.sleep(1)
            # Belohnung: Finde die Daten-Diskette
            if not game_state.get('diskette_received', False):
                print_slow("IN DEN LOGS WIRD EINE VERSCHOBENE 'PROTOKOLL 7' DATEI ERWÄHNT. JEMAND HAT EINE KOPIE AUF EINER DISKETTE ZURÜCKGELASSEN!")
                # Die Diskette erscheint jetzt im Cafe
                items['DATEN_DISKETTE']['location'] = 'CAFE'
                game_state['diskette_received'] = True
                print_slow("DU SIEHST HIER JETZT: DATEN DISKETTE")
                increase_alert_level(3)
            else:
                print_slow("DU DURCHSUCHST DIE LOGS, FINDEST ABER NICHTS NEUES VON INTERESSE.")
                increase_alert_level(1)
        else:
            print_slow("FEHLGESCHLAGEN! DAS SYSTEM HAT DEINEN VERSUCH REGISTRIERT.")
            increase_alert_level(4)
            check_alert_level()
    elif target == 'COMPUTER' and loc_id == 'APARTMENT':
         print_slow("DU MUSST DEN COMPUTER ZUERST BENUTZEN ('BENUTZE COMPUTER'), UM ZU VERSUCHEN, DICH EINZULOGGEN.")
    else:
        print_slow(f"DU KANNST '{target}' HIER NICHT HACKEN.")


def handle_talk(args):
    """Initiert ein Gespräch mit einem NPC."""
    if not args:
        print_slow("MIT WEM MOECHTEST DU SPRECHEN? (BENUTZE 'REDE MIT [NAME]')")
        return

    npc_name = " ".join(args).upper()
    loc_id = game_state['current_location']
    location = locations[loc_id]

    if npc_name in location.get('npcs', []):
        # Spezifische Dialoge
        if npc_name == 'MANN' and loc_id == 'CAFE':
            talk_to_cypher_like_npc(npc_name)
        # Hier könnten weitere NPCs eingefügt werden
        # elif npc_name == 'ORACLE' and loc_id == 'KANINCHENBAU_FORUM':
        #    talk_to_oracle()
        else:
             # Generischer Fall für andere NPCs ohne spezifischen Dialog
             npc_detail = location.get('details', {}).get(npc_name, f"{npc_name} scheint beschaeftigt.")
             print_slow(wrap_text(npc_detail))
             print_slow(f"{npc_name} IGNORIERT DICH WEITGEHEND.")
    else:
        print_slow(f"HIER IST NIEMAND MIT DEM NAMEN '{npc_name}'.")

def handle_open(args):
    """Versucht etwas zu öffnen."""
    if not args:
        print_slow("WAS MOECHTEST DU OEFFNEN?")
        return

    target_name = " ".join(args).upper()
    loc_id = game_state['current_location']
    location = locations[loc_id]

    # Beispiel: Öffne Tür zur Serverfarm
    if target_name == 'TUER' and loc_id == 'SERVER_FARM_EINGANG':
        if game_state.get('server_farm_access_granted', False):
             print_slow("DIE SCHWERE STAHLTUER SCHWINGT MIT EINEM LEISEN SUMMEN AUF.")
             # Hier den Spieler in die Serverfarm bewegen (neuen Ort definieren!)
             # game_state['current_location'] = 'SERVER_FARM_INNERES'
             # display_location()
             print_slow("(DEBUG: Zugang zur Serverfarm gewaehrt, aber der Ort 'SERVER_FARM_INNERES' ist noch nicht implementiert.)")
             # Man könnte hier ein Flag setzen, dass die Tür offen ist.
             locations['SERVER_FARM_EINGANG']['details']['TUER'] = "Die schwere Stahltür steht einen Spalt offen."
             # Optional: Ausgang hinzufügen, wenn offen?
             # locations['SERVER_FARM_EINGANG']['exits']['REIN'] = 'SERVER_FARM_INNERES'

        elif game_state.get('server_farm_card_used', False) and game_state.get('server_farm_code_correct', False):
             # Sollte eigentlich durch server_farm_access_granted abgedeckt sein, aber als Fallback
             print_slow("DIE TUER KLICKT, SCHEINT ABER NOCH VERKLEMMT. VERSUCH ES NOCHMAL?")
             game_state['server_farm_access_granted'] = True # Setzen wir es hier sicherheitshalber
        elif game_state.get('server_farm_card_used', False):
             print_slow("DIE TUER BLEIBT VERSCHLOSSEN. DER KARTENLESER LEUCHTETE, ABER ES FEHLT WOHL NOCH DER CODE.")
        elif game_state.get('server_farm_code_correct', False):
             print_slow("DIE TUER BLEIBT VERSCHLOSSEN. DAS NUMPAD LEUCHTETE, ABER ES FEHLT WOHL NOCH DIE KARTE.")
        else:
             print_slow("DIE TUER IST FEST VERSCHLOSSEN. SIE BENOETIGT WOHL EINE SCHLUESSELKARTE UND EINEN CODE.")
    # Beispiel: Tür der Telefonzelle (eigentlich unnötig, da 'GEHE TELEFONZELLE' funktioniert)
    elif target_name == 'TELEFONZELLE' and loc_id == 'STRASSE':
         print_slow("Du öffnest die Tür zur Telefonzelle und gehst hinein.")
         handle_go(['TELEFONZELLE']) # Nutze die GEHE Funktion
    else:
         print_slow(f"DU KANNST '{target_name}' NICHT OEFFNEN.")

def handle_push(args):
    """Drückt etwas."""
    if not args:
        print_slow("WAS MOECHTEST DU DRUECKEN?")
        return
    target_name = " ".join(args).upper()
    loc_id = game_state['current_location']
    # Hier Logik für Knöpfe etc.
    if target_name == 'KNOPF' and loc_id == 'TELEFONZELLE_INNERES': # Beispiel
        print_slow("DU DRUECKST EINEN KLEINEN, UNBESCHRIFTETEN KNOPF NEBEN DEM MUENZSCHLITZ.")
        print_slow("NICHTS SCHEINT ZU PASSIEREN.")
    else:
        print_slow(f"DU KANNST '{target_name}' NICHT DRUECKEN ODER ES GIBT HIER NICHTS ZU DRUECKEN.")

def handle_scan(args):
     """Startet einen Scan."""
     if not args:
        print_slow("WAS MOECHTEST DU SCANNEN? (Z.B. SCANNE PORTS)")
        return

     target = " ".join(args).upper()
     loc_id = game_state['current_location']

     if target == 'PORTS' and loc_id == 'SERVER_FARM_EINGANG':
          # Direkter Aufruf des Port-Scans auch möglich
          start_port_scan_minigame()
     elif target == 'PORTS' and game_state['computer_logged_in'] and loc_id == 'APARTMENT':
         print_slow("DU STARTETST EINEN NETZWERK-SCAN VON DEINEM COMPUTER AUS...")
         # Hier könnte man Infos über erreichbare Systeme geben
         print_slow("SCAN ERGEBNISSE: Lokales Netzwerk (HEIMBASIS), Oeffentliches Terminal (CYBER CAFE), Unbekannte Adresse (SERVER-FARM IP)")
         increase_alert_level(1)
     else:
          print_slow(f"HIER GIBT ES NICHTS SINNVOLLES ZU SCANNEN MIT '{target}'.")

def handle_code_input(args):
    """Verarbeitet Code-Eingabe am Numpad."""
    if not args:
        print_slow("WELCHEN CODE MOECHTEST DU EINGEBEN? (BENUTZE 'CODE [NUMMER]')")
        return

    code = args[0]
    loc_id = game_state['current_location']

    # Nur am Server-Farm Eingang gibt es ein relevantes Numpad
    if loc_id == 'SERVER_FARM_EINGANG':
        numpad_interactable = 'NUMPAD' in locations[loc_id].get('interactables', [])
        if not numpad_interactable:
             print_slow("HIER GIBT ES KEIN NUMPAD.")
             return

        print_slow(f"DU GIBST DEN CODE '{code}' AM NUMPAD EIN...")
        time.sleep(1.5)
        # Prüfe, ob der Spieler den Code überhaupt kennen kann (z.B. nach erfolgreichem Port-Scan)
        if not game_state.get('server_farm_hacked', False):
            print_slow("DU HAST KEINE AHNUNG, WELCHEN CODE DU EINGEBEN SOLLST.")
            increase_alert_level(1)
            return

        # Vergleiche mit dem korrekten Code
        if code == game_state['server_farm_access_code']:
            print_slow("EIN GRUENES LICHT LEUCHTET AM NUMPAD. CODE AKZEPTIERT.")
            game_state['server_farm_code_correct'] = True
            increase_alert_level(1)
            # Prüfen, ob auch Karte schon benutzt wurde
            if game_state.get('server_farm_card_used', False):
                 game_state['server_farm_access_granted'] = True
                 print_slow("EIN KLICKEN IST ZU HOEREN. DIE TUER SCHEINT ENTSPERRT ZU SEIN. (VERSUCHE 'OEFFNE TUER')")
            else:
                 print_slow("DAS NUMPAD LEUCHTET GRUEN, ABER DIE TUER BLEIBT ZU. FEHLT NOCH DIE SCHLUESSELKARTE?")
        else:
            print_slow("FALSCHER CODE. EIN ROTES LICHT BLINKT WARNEND.")
            increase_alert_level(3)
            check_alert_level()
            game_state['server_farm_code_correct'] = False
    else:
        print_slow("HIER GIBT ES KEIN NUMPAD, UM EINEN CODE EINZUGEBEN.")

# --- NPCs und Dialoge ---
def talk_to_cypher_like_npc(npc_name):
    """Dialog mit dem Mann im Cafe (Cypher-Anspielung)."""
    loc_id = game_state['current_location']
    if loc_id != 'CAFE': return # Nur im Cafe

    if not game_state['met_cypher']:
        print_slow(f"'NA?', sagt {npc_name}, ohne dich anzusehen. 'NEU HIER IM SCHATTEN?'")
        time.sleep(1)
        print_slow("'SEI VORSICHTIG, WEM DU TRAUST. NICHTS IST, WIE ES SCHEINT.'")
        time.sleep(1)
        print_slow("'MANCHE SUCHEN DIE WAHRHEIT, ANDERE NUR DEN AUSWEG.'")
        game_state['met_cypher'] = True
        increase_alert_level(1) # Gespräch mit zwielichtiger Gestalt

        # Schenkt dem Spieler die Schlüsselkarte, wenn er sie noch nicht hat
        # Und wenn sie nicht schon im Cafe liegt (z.B. von früherem Versuch)
        if 'SCHLUESSELKARTE' not in game_state['player_inventory'] and items['SCHLUESSELKARTE']['location'] is None:
            time.sleep(1.5)
            print_slow(f"{npc_name} schiebt dir unauffaellig etwas ueber die Theke.")
            print_slow("'VIELLEICHT HILFT DIR DAS BEI EINER VERSCHLOSSENEN TUER IRGENDWO IN DER STADT. ABER FRAG NICHT, WOher ICH ES HABE.'")
            # Schlüsselkarte erscheint im Cafe zum Aufheben
            items['SCHLUESSELKARTE']['location'] = game_state['current_location']
            print_slow("\nDU SIEHST HIER JETZT: SCHLUESSELKARTE")
    else:
        # Wiederholungsdialog
         responses = [
             f"{npc_name} poliert weiter seine Brille. 'IMMER NOCH HIER? Suchst du was bestimmtes?'",
             f"{npc_name} zuckt mit den Schultern. 'FRAGEN UEBER FRAGEN... FINDE DEINE EIGENEN ANTWORTEN. Oder frag jemand anderen.'",
             f"{npc_name} murmelt: 'Ignoranz ist manchmal ein Segen... aber selten profitabel.'",
             f"{npc_name} schaut kurz auf. 'Pass auf die Agenten auf. Sie sind ueberall.'"
         ]
         print_slow(random.choice(responses))

# --- Minispiele und Rätsel ---
def trigger_first_message():
    """Zeigt die initiale verschlüsselte Nachricht an."""
    if not game_state['first_message_received']:
        print("\n" + "="*WIDTH)
        print_slow("PLOETZLICH BLINKT EIN FENSTER AUF DEINEM COMPUTERBILDSCHIRM AUF.")
        time.sleep(1)
        print_slow(" EINGEHENDE NACHRICHT:")
        print_slow(" QUELLE: UNBEKANNT")
        print_slow(" VERSCHLUESSELUNG: STANDARD ROT13 (DEBUG: Eigentlich REDPiLL)") # Hinweis für Spieler/Tester
        print_slow(" NACHRICHT: 'SBYTR QHZ JRVFFRA XNAVAPURA.' (ROT13)") # Verschlüsselte Nachricht direkt anzeigen
        print("="*WIDTH + "\n")
        print_slow("(DU KOENNTEST VERSUCHEN: DEKRYPTIERE NACHRICHT MIT REDPiLL)") # Klarer Hinweis
        game_state['first_message_received'] = True

def crack_apartment_password():
    """Passwort-Knack-Minispiel für den Computer."""
    print_slow("DU VERSUCHST, DICH AM COMPUTER EINZULOGGEN.")
    print_slow("PASSWORT GESCHUETZT. SYSTEM: 'HEIMBASIS'.")

    # Hinweis holen (wenn Zettel vorhanden oder gelesen wurde)
    hint = ""
    zettel_readable = ('ZETTEL' in game_state['player_inventory'] or items['ZETTEL']['location'] == 'APARTMENT') and not game_state['apartment_password_cracked']
    if zettel_readable:
        hint = " (HINWEIS AUF DEM ZETTEL VERFUEGBAR - 'LIES ZETTEL')"
    elif game_state['apartment_password_cracked']:
         hint = " (PASSWORT BEREITS GEKNACKT)" # Sollte nicht passieren, wenn schon eingeloggt
    else:
        hint = " (DU HAST KEINEN HINWEIS)"

    attempts = 3
    while attempts > 0:
        # Passwortabfrage (Kleinschreibung erzwingen für einfachere Eingabe)
        password_guess = input(f"PASSWORT EINGEBEN{hint}: ").strip().lower()

        # Das korrekte Passwort (Matrix, erster Film der Wachowskis nach Bound)
        correct_password = "matrix"

        if password_guess == correct_password:
            print_slow("ZUGRIFF GEWAEHRT. WILLKOMMEN ZURUECK.")
            game_state['computer_logged_in'] = True
            game_state['apartment_password_cracked'] = True
            increase_alert_level(1) # Erfolgreicher Login ist ok
             # Optional: Zettel "unwichtig" machen
            if 'ZETTEL' in game_state['player_inventory'] or items['ZETTEL']['location'] == 'APARTMENT':
                print_slow("(Der Zettel mit dem Hinweis scheint nun ueberfluessig.)")
                items['ZETTEL']['description'] = "Ein zerknuellter Zettel. Die Schrift ist kaum noch lesbar."
                items['ZETTEL']['read_text'] = "Die Schrift auf dem Zettel ist verwischt und kaum noch lesbar." # Eigener Lesetext
            return True # Erfolg signalisieren
        else:
            attempts -= 1
            print_slow(f"PASSWORT FALSCH. VERBLEIBENDE VERSUCHE: {attempts}")
            increase_alert_level(2) # Fehlversuch ist schlecht
            check_alert_level() # Sofort prüfen, ob das Konsequenzen hat
            if attempts == 0:
                print_slow("ZU VIELE FEHLVERSUCHE. SYSTEM TEMPORAER GESPERRT.")
                # Hier könnte eine Wartezeit oder ein anderer Nachteil eingebaut werden
                # Z.B. Computer für eine Weile unbenutzbar machen
                return False # Misserfolg signalisieren

    return False # Falls Schleife endet (sollte nicht passieren)

def use_computer():
    """Interaktion mit dem Computer im Apartment."""
    # Wenn noch nicht eingeloggt, Passwort knacken versuchen
    if not game_state['computer_logged_in']:
        if not crack_apartment_password():
            return # Abbruch, wenn Passwort-Knacken fehlschlägt

    # Ab hier ist der Spieler eingeloggt
    print_slow("\n--- COMPUTER INTERFACE ---")
    print_slow("SYSTEM 'HEIMBASIS' BEREIT.")
    print_slow("MOEGLICHE AKTIONEN: ONLINE GEHEN, LIES DISKETTE, SCANNE NETZWERK, LOGOUT")

    in_computer_mode = True
    while in_computer_mode:
        comp_cmd = input("COMPUTER> ").strip().upper()
        use_computer_command(comp_cmd)
        # Prüfen, ob der Befehl den Modus beendet hat (z.B. Logout oder Wechsel ins Forum)
        if game_state['current_location'] != 'APARTMENT' or not game_state['computer_logged_in']:
            in_computer_mode = False
            if game_state['current_location'] == 'APARTMENT': # Wenn nur ausgeloggt wurde
                 print_slow("--- COMPUTER INTERFACE GESCHLOSSEN ---")


def use_computer_command(comp_cmd):
     """Verarbeitet Befehle innerhalb des Computer-Modus."""
     if comp_cmd == 'ONLINE GEHEN' or comp_cmd == 'ONLINE':
         # Prüfen ob die erste Nachricht entschlüsselt wurde als Voraussetzung
         if game_state['decrypted_message_content'] == "FOLGE DEM WEISSEN KANINCHEN.":
             print_slow("DU VERBINDEST DICH MIT DEM NETZWERK...")
             time.sleep(1.5)
             print_slow("SUCHE NACH DEM 'KANINCHENBAU' FORUM...")
             time.sleep(2)
             print_slow("VERBINDUNG HERGESTELLT.")
             game_state['current_location'] = 'KANINCHENBAU_FORUM'
             display_location()
             # Verlässt implizit den Computer-Modus durch Ortswechsel
         else:
             print_slow("DU WEISST NICHT, WONACH DU SUCHEN SOLLST... DU BRAUCHST EINEN HINWEIS ODER EIN ZIEL.")
             print_slow("(Hast du schon die erste Nachricht auf dem Bildschirm dekryptiert?)")

     elif comp_cmd == 'LIES DISKETTE':
         if 'DATEN_DISKETTE' in game_state['player_inventory']:
             print_slow("Lese Diskette 'PROTOKOLL 7'...")
             time.sleep(2)
             # Hier den Inhalt der Diskette enthüllen
             disk_content = ("INHALT: Verschluesselte Uebertragungslogs. Zeitstempel stimmen mit den 'Glitches' ueberein. Eine Signatur: 'Morpheus'. Eine Koordinatenangabe zu einer oeffentlichen Telefonzelle auf der STRASSE VOR DEM HAUS.")
             print_slow(wrap_text(disk_content))
             # Telefonzelle wird zum Ziel / wichtiger
             print_slow("\n(Die TELEFONZELLE auf der STRASSE erscheint nun sehr wichtig. Koennte sie der naechste Schritt sein?)")
             increase_alert_level(2)
             # Flag setzen, damit das Telefon-Event ausgelöst werden kann
             game_state['diskette_read'] = True

         else:
             print_slow("KEINE DISKETTE IM LAUFWERK. HAST DU SIE IM INVENTAR?")

     elif comp_cmd in ['SCANNE NETZWERK', 'SCAN NETZWERK', 'NETZWERK SCAN']:
          print_slow("DU STARTETST EINEN NETZWERK-SCAN...")
          time.sleep(1.5)
          print_slow("SCAN ERGEBNISSE:")
          print_slow("- Lokales Netzwerk: HEIMBASIS (AKTUELL)")
          # Zeige andere bekannte/erreichbare Orte an
          if 'CAFE' in locations: # Wenn das Cafe bekannt ist
                print_slow("- Oeffentliches Netzwerk: CYBER CAFE TERMINAL (IP: 192.168.1.101)")
          if 'SERVER_FARM_EINGANG' in locations: # Wenn die Server Farm bekannt ist
                print_slow("- Externe Adresse: SERVER-FARM (IP: 213.45.67.89 - HOHE SICHERHEIT)")
          increase_alert_level(1)

     elif comp_cmd == 'LOGOUT':
         print_slow("DU LOGGST DICH VOM COMPUTER AUS.")
         # game_state['computer_logged_in'] = False # Spieler bleibt eingeloggt, bis er das Spiel beendet? Oder hier ausloggen?
         # Entscheidung: Ausloggen macht Sinn, um Passwort erneut eingeben zu müssen.
         game_state['computer_logged_in'] = False
         # Beendet die Computer-Schleife im aufrufenden use_computer()
     else:
         print_slow(f"UNBEKANNTER COMPUTER-BEFEHL: '{comp_cmd}'. Verfügbar: ONLINE GEHEN, LIES DISKETTE, SCANNE NETZWERK, LOGOUT")


def start_port_scan_minigame():
    """Port-Scanning Minispiel für die Server-Farm."""
    loc_id = game_state['current_location']
    if loc_id != 'SERVER_FARM_EINGANG':
        print_slow("DU MUSST VOR DER SERVER-FARM STEHEN, UM PORTS ZU SCANNEN.")
        return

    if game_state['server_farm_hacked']:
        print_slow("DU HAST BEREITS EINEN ZUGANG ZUM SYSTEM ÜBER TELNET GEFUNDEN.")
        return

    print_slow("DU STARTETST EINEN PORT SCAN AUF DIE IP DER SERVER-FARM (213.45.67.89)...")
    increase_alert_level(2) # Port Scan ist auffällig
    time.sleep(2)
    # Ports, einer davon ist der richtige (Telnet für den Hinweis)
    ports = ['21 (FTP)', '22 (SSH)', '23 (TELNET)', '80 (HTTP)', '443 (HTTPS)', '6667 (IRC)']
    random.shuffle(ports) # Mische die Reihenfolge für jeden Versuch
    print_slow("OFFENE PORTS GEFUNDEN:")
    for i, port_info in enumerate(ports):
        print(f"{i+1}: {port_info}")
        time.sleep(0.3)

    print_slow("\nEINE VERSTECKTE SYSTEMNACHRICHT WIRD ABGEFANGEN:")
    # Einfache ROT13 Verschlüsselung für den Hinweis
    # Hinweis: "DER TELNET-ZUGRIFF IST ALT, NUTZE DEN PORT, DER OFT FUER UNSICHERE VERBINDUNGEN VERWENDET WIRD."
    hint_encrypted = "QRE GRYARG-MHTEVSS VFG NYG, AHGMR QRA CBEG, QRE BSG SHRE HAFVPURER IREOVAQHATRA IREJRAQRG JVEQ."
    print_slow(f"'{hint_encrypted}' (ROT13)")

    correct_port_index = -1
    for i, port_info in enumerate(ports):
        if "23 (TELNET)" in port_info:
            correct_port_index = i + 1
            break

    if correct_port_index == -1:
        print_slow("FEHLER: KORREKTER PORT NICHT IN LISTE GEFUNDEN (DEBUGGING)")
        return

    attempts = 2
    while attempts > 0:
        try:
            choice = input(f"WELCHEN PORT VERSUCHST DU ZU VERBINDEN (1-{len(ports)})?> ")
            choice_index = int(choice)

            if not (1 <= choice_index <= len(ports)):
                 print_slow("UNGÜLTIGE AUSWAHL.")
                 continue # Neue Eingabeaufforderung

            chosen_port_info = ports[choice_index - 1]
            print_slow(f"VERSUCHE VERBINDUNG MIT PORT {chosen_port_info}...")
            time.sleep(1.5)

            if choice_index == correct_port_index:
                print_slow("VERBINDUNG UEBER PORT 23 HERGESTELLT!")
                time.sleep(1)
                print_slow(">>> TELNET-BANNER: 'UNAUTORISIERTER ZUGRIFF STRENGSTENS VERBOTEN! LOGGING AKTIV!' <<<")
                print_slow("DU BIST DRIN! DU HAST EINE MINIMALE SHELL-SITZUNG.")
                # Erfolg! Hier könnte Zugang zu Infos oder weiteren Hacks erfolgen.
                game_state['server_farm_hacked'] = True
                increase_alert_level(4) # Erfolgreicher Hack ist sehr auffällig
                check_alert_level()
                # Belohnung: Finde den Hinweis auf den Türcode
                print_slow("\nIN DEN WILLKOMMENSNACHRICHTEN DER ALTEN SHELL FINDEST DU EINEN VERGESSENEN HINWEIS:")
                print_slow("'ADMIN-NOTIZ: TUERCODE IST DAS JAHR, IN DEM DER ERSTE FILM IN DIE KINOS KAM.'") # Hinweis auf 1999 (Matrix)
                game_state['server_farm_access_code'] = "1999" # Sicherstellen, dass er jetzt 'bekannt' ist
                print_slow("(DU KANNST JETZT VERSUCHEN, DEN CODE AM NUMPAD EINZUGEBEN: 'CODE 1999')")
                return # Minispiel erfolgreich beendet
            else:
                attempts -= 1
                print_slow(f"VERBINDUNG FEHLGESCHLAGEN ODER ABGELEHNT. {attempts} VERSUCH(E) UEBRIG.")
                increase_alert_level(2)
                check_alert_level()
                if attempts == 0:
                    print_slow("SYSTEM HAT MEHRERE FEHLGESCHLAGENE VERBINDUNGSVERSUCHE REGISTRIERT! VERBINDUNG BLOCKIERT.")
                    increase_alert_level(3) # Extra Strafe
                    check_alert_level()
                    return # Minispiel gescheitert
        except ValueError:
            print_slow("UNGÜLTIGE EINGABE. BITTE EINE ZAHL EINGEBEN.")
        except IndexError:
             print_slow("UNGÜLTIGE AUSWAHL. BITTE EINE ZAHL ZWISCHEN 1 UND {len(ports)} EINGEBEN.")


    print_slow("DER PORT SCAN UND VERBINDUNGSVERSUCH WAR NICHT ERFOLGREICH.")


def use_phone():
    """Benutzt das Telefon in der Zelle."""
    if game_state['current_location'] != 'TELEFONZELLE_INNERES':
        print_slow("DU BIST NICHT IN EINER TELEFONZELLE.")
        return

    if game_state['phone_ringing']:
         print_slow("DAS TELEFON KLINGELT LAUT! NIMM LIEBER DEN HOERER AB ('BENUTZE HOERER').")
    else:
         print_slow("DU NIMMST DEN HOERER AB. ES IST EIN WAEHLTON ZU HOEREN.")
         print_slow("DU HAST KEINE NUMMER ZUM WAEHLEN IM KOPF UND LEGST WIEDER AUF.")
         # Hier könnte man eine Wählfunktion einbauen, wenn der Spieler Nummern kennt.
         # z.B. input("NUMMER WAEHLEN?> ") und dann prüfen.


def use_phone_receiver():
     """Nimmt den Hörer in der klingelnden Zelle ab."""
     if game_state['current_location'] != 'TELEFONZELLE_INNERES':
        print_slow("WO IST EIN HOERER?")
        return

     if game_state['phone_ringing']:
         print_slow("DU NIMMST DEN SCHWEREN, KUEHLEN BAKELIT-HOERER ANS OHR. DAS KLINGELN STOPPT SOFORT.")
         increase_alert_level(1) # Auffällige Aktion
         time.sleep(1.5)
         print_slow("Eine ruhige, tiefe, vertrauenswürdig klingende Stimme sagt: 'Hallo?'")
         time.sleep(1.5)
         # Hier könnte der Dialog mit Morpheus beginnen oder eine wichtige Info kommen
         print_slow("'Ich weiss, wonach du suchst', sagt die Stimme. 'Die Anomalien. Die Glitches in der Realitaet.'")
         time.sleep(2)
         print_slow("'Die Wahrheit ist da draussen, aber sie ist gefaehrlich.'")
         time.sleep(1.5)
         print_slow("'Du hast einen ersten Schritt gemacht. Aber sei vorsichtig. Sie beobachten dich jetzt.'")
         time.sleep(2)
         print_slow("'Es gibt andere wie uns. Suche im 'KANINCHENBAU' nach dem ORACLE. Sie erwartet dich.'")
         time.sleep(2.5)
         print_slow("KLICK.")
         print_slow("Die Verbindung bricht ab. Nur noch Stille und das leise Rauschen der Leitung.")
         game_state['phone_ringing'] = False # Klingeln hört auf
         increase_alert_level(-1) # Etwas Entspannung oder Fokus?
         # Wichtiger Story-Fortschritt markieren
         game_state['oracle_contacted'] = True # Flag, dass Morpheus kontaktiert wurde
         # Zugang zum Oracle im Forum freischalten (Beispiel)
         if 'KANINCHENBAU_FORUM' in locations:
              locations['KANINCHENBAU_FORUM']['details']['ORACLE'] = "DER PRIVATE BEREICH DES ORACLES. ZUGANG JETZT MOEGLICH."
              # Eventuell einen neuen Befehl freischalten oder Hinweis geben:
              print_slow("(Du koenntest jetzt im KANINCHENBAU Forum versuchen, das ORACLE zu kontaktieren.)")

     else:
         print_slow("DU NIMMST DEN HOERER AB. NUR EIN NORMALER WAEHLTON. DU LEGST WIEDER AUF.")


# --- Spielmechanik ---
def increase_alert_level(amount):
  """Erhöht oder verringert den Alert-Level und gibt Feedback."""
  if amount == 0:
      return

  game_state['alert_level'] += amount
  game_state['alert_level'] = max(0, game_state['alert_level']) # Nicht unter 0 fallen
  game_state['alert_level'] = min(10, game_state['alert_level']) # Obergrenze (optional)

  # Feedback basierend auf dem NEUEN Level
  level = game_state['alert_level']
  if amount > 0:
      if level <= 2:
          print_slow("(Du fuehlst dich noch relativ unbemerkt.)")
      elif level <= 4:
          print_slow("(Ein ungutes Gefühl... als ob jemand deine Aktivitaeten bemerkt.)")
      elif level <= 6:
           print_slow("[SYSTEM WARNUNG: Erhoehte Ueberwachungsaktivitaet in deinem Sektor!]")
      else: # level >= 7
           print_slow("[ALARM! HOECHSTE GEFAHRENSTUFE! DEINE POSITION IST WAHRSCHEINLICH KOMPROMITTIERT!]")
  elif amount < 0:
       print_slow("(Die digitale Anspannung laesst etwas nach.)")

  # print(f"DEBUG: Alert Level = {game_state['alert_level']}") # Zum Testen


def check_alert_level():
    """Prüft, ob der Alert-Level zu hoch ist und löst Konsequenzen aus."""
    level = game_state['alert_level']

    if level >= 8: # Game Over Schwelle
        print_slow("\n" + "!" * WIDTH)
        print_slow("!!! SYSTEM ALARM !!!")
        time.sleep(1)
        print_slow("DEINE VERBINDUNG WIRD GEKAPERT! MEHRERE EXTERNE ZUGRIFFE!")
        time.sleep(1.5)
        # Abhängig vom Ort andere Meldungen?
        current_loc = game_state['current_location']
        if current_loc == 'APARTMENT':
            print_slow("DU HOERST SIRENEN AUF DER STRASSE! SCHRITTE POLTERN IM TREPPENHAUS!")
            time.sleep(1)
            print_slow("DIE TUER ZU DEINEM APARTMENT WIRD AUFGEBROCHEN!")
        elif current_loc == 'CAFE':
            print_slow("DER MANN HINTER DER THEKE ZIEHT EINE WAFFE! DIE ANDEREN GESTALTEN STEHEN AUF!")
            time.sleep(1)
            print_slow("LICHTER ZUCKEN VOR DEM FENSTER!")
        elif current_loc == 'STRASSE' or current_loc == 'TELEFONZELLE_INNERES':
             print_slow("SCHWARZE LIMOUSINEN RASEN UM DIE ECKE! MAENNER IN SCHWARZEN ANZUEGEN SPRINGEN HERAUS!")
        else: # Generisch
             print_slow("EIN OHRENBETAEUBENDES RAUSCHEN ERFUELLT DEINE SINNE! DEINE SICHT VERSCHWIMMT!")
             time.sleep(1)
             print_slow("DU WIRST GEWALTSAM AUS DEM SYSTEM GEWORFEN!")

        time.sleep(1.5)
        print_slow("'Wir haben ihn.', hörst du eine kalte Stimme sagen.")
        time.sleep(1)
        print_slow("Alles wird schwarz...")
        print_slow("\n" + "-"*WIDTH)
        print_slow("--- VERBINDUNG PERMANENT UNTERBROCHEN ---")
        print_slow("--- SPIEL ENDE ---")
        print("!" * WIDTH)
        sys.exit()

    elif level >= 6 and random.randint(1, 3) == 1: # Zufällige niedrigere Bedrohung bei hohem Level
         print_slow("\n[SYSTEM WARNUNG: Unbekannte Prozesse analysieren deine Netzwerkverbindung intensiv... SEI EXTREM VORSICHTIG!]")
         time.sleep(1)
    elif level >= 4 and random.randint(1, 5) == 1: # Zufällige niedrigere Bedrohung bei mittlerem Level
        print_slow("\n(Ein kurzer Glitch auf deinem Monitor... oder bildest du dir das nur ein?)")
        time.sleep(0.5)


# --- Ereignisse und Überraschungen ---

def trigger_phone_event_check():
    """Prüft, ob das Telefon klingeln sollte."""
    # Bedingungen:
    # 1. Spieler hat die Diskette gelesen (weiss von der Telefonzelle)
    # 2. Spieler ist auf der Strasse (in der Nähe der Zelle)
    # 3. Telefon klingelt nicht bereits
    # 4. Morpheus/Oracle wurde noch nicht kontaktiert
    # 5. Zufällige Chance
    should_ring = (
        game_state.get('diskette_read', False) and
        game_state['current_location'] == 'STRASSE' and
        not game_state['phone_ringing'] and
        not game_state['oracle_contacted'] and
        random.randint(1, 8) == 1 # Chance 1 zu 8 pro Zug auf der Strasse
    )

    if should_ring:
         print_slow("\n*** RIIING RIIING... RIIING RIIING ***")
         time.sleep(0.8)
         print_slow("Das oeffentliche Telefon in der Zelle neben dir beginnt laut und eindringlich zu klingeln!")
         game_state['phone_ringing'] = True
         # Hinweis geben
         print_slow("(Du koenntest zur 'TELEFONZELLE' gehen und den 'HOERER' benutzen, um abzunehmen.)")
         increase_alert_level(1) # Das Klingeln könnte Aufmerksamkeit erregen

# (trigger_phone_pickup_event ist jetzt in handle_go und use_phone_receiver integriert)

# --- Hauptspiel-Schleife ---
def main():
  """Hauptfunktion des Spiels."""
  print_c64_header()
  display_location()

  while True:
    # 1. Alert Level prüfen (kann zum Spielende führen)
    check_alert_level()

    # 2. Zufällige Ereignisse prüfen (z.B. Telefon klingeln)
    # Nur prüfen, wenn der Spieler nicht gerade im Computer-Interface ist
    if game_state['current_location'] != 'KANINCHENBAU_FORUM' and not game_state['computer_logged_in']:
         trigger_phone_event_check()

    # 3. Spielereingabe holen
    command = get_player_input()
    if not command:
      continue # Leere Eingabe ignorieren

    # 4. Befehl parsen
    verb, args = parse_command(command)
    if not verb:
      continue # Ungültiger Befehl

    # 5. Befehl verarbeiten
    print("-" * WIDTH) # Trennlinie vor der Antwort
    handle_command(verb, args)

    # 6. Kleinen Moment warten (optional, für Lesbarkeit)
    # time.sleep(0.1)


if __name__ == "__main__":
  try:
      main()
  except KeyboardInterrupt:
      print_slow("\n\nSpiel durch Benutzer unterbrochen. Bis bald!")
      sys.exit()