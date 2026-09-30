# -*- coding: utf-8 -*-
"""Socle commun : lire les 113 promesses francaises, resoudre chaque reference
dans la Segond 1910 (libre) et dans la Biblia Livre (libre)."""
import io
import json
import re

FR_APP = r'C:\Users\Stéphane CASSANI\Depots\promesses-bibliques\index.html'
PT_APP = r'C:\Users\Stéphane CASSANI\Depots\promessas-biblicas\index.html'
SEGOND = r'C:\Users\Stéphane CASSANI\bible-chantee\bibles\fr_bible_segond1910.json'
BLIVRE = r'C:\Users\Stéphane CASSANI\Desktop\Promesses Vitamin (B)iblique\pt\bible\BLIVRE.json'

# --------------------------------------------------------------- l'application FR


def lire_categories():
    """[(numero, titre, icone, [(reference, texte_segond21), ...]), ...]"""
    s = io.open(FR_APP, encoding='utf-8', errors='replace').read()
    debut = s.index('const promessesData')
    fin = s.index('\n};', debut)
    bloc = s[debut:fin]
    sortie = []
    for m in re.finditer(r'(\d+):\s*\{\s*title:\s*"([^"]*)",\s*icon:\s*"([^"]*)",\s*'
                         r'promises:\s*\[(.*?)\]\s*\}', bloc, re.S):
        versets = re.findall(r'reference:\s*"([^"]*)",\s*text:\s*"((?:[^"\\]|\\.)*)"',
                             m.group(4), re.S)
        versets = [(r, t.replace('\\"', '"').replace("\\'", "'")) for r, t in versets]
        sortie.append((int(m.group(1)), m.group(2), m.group(3), versets))
    return sortie


def lire_categories_pt():
    """Les titres portugais deja traduits, dans l'ordre : [(emoji, nom), ...]"""
    s = io.open(PT_APP, encoding='utf-8', errors='replace').read()
    return re.findall(r'emoji:\s*"([^"]*)",\s*nome:\s*"([^"]*)"', s)


def lire_sections_pt():
    s = io.open(PT_APP, encoding='utf-8', errors='replace').read()
    return re.findall(r'titulo:\s*"([^"]*)"', s)


# --------------------------------------------------------------- les deux bibles

def charger_segond():
    d = json.load(io.open(SEGOND, encoding='utf-8'))
    index = {}
    for v in d['verses']:
        index.setdefault(v['book_name'], {}).setdefault(v['chapter'], {})[v['verse']] = \
            v['text'].replace('¶', '').strip()
    return index


def charger_blivre():
    d = json.load(io.open(BLIVRE, encoding='utf-8'))
    index = {}
    for livre in d:
        index[livre['name']] = {
            c + 1: {v + 1: t.strip() for v, t in enumerate(versets)}
            for c, versets in enumerate(livre['chapters'])}
    return index


# nom francais de l'application -> nom dans chaque bible
# La Segond 1910 locale nomme les livres exactement comme l'application :
# « Psaume » au singulier, « Ésaïe » accentue. Seul le Cantique differe
# (son nom y est tronque a vingt caracteres).
FR_VERS_SEGOND = {
    'Cantique': 'Cantique Des Cantiqu',
    'Cantique des Cantiques': 'Cantique Des Cantiqu',
}

FR_VERS_PT = {
    'Genèse': 'Gênesis', 'Exode': 'Êxodo', 'Lévitique': 'Levítico',
    'Nombres': 'Números', 'Deutéronome': 'Deuteronômio', 'Josué': 'Josué',
    'Juges': 'Juízes', 'Ruth': 'Rute', '1 Samuel': '1 Samuel', '2 Samuel': '2 Samuel',
    '1 Rois': '1 Reis', '2 Rois': '2 Reis', '1 Chroniques': '1 Crônicas',
    '2 Chroniques': '2 Crônicas', 'Esdras': 'Esdras', 'Néhémie': 'Neemias',
    'Esther': 'Ester', 'Job': 'Jó', 'Psaume': 'Salmos', 'Psaumes': 'Salmos',
    'Proverbes': 'Provérbios', 'Ecclésiaste': 'Eclesiastes',
    'Cantique': 'Cânticos', 'Ésaïe': 'Isaías', 'Jérémie': 'Jeremias',
    'Lamentations': 'Lamentações', 'Ézéchiel': 'Ezequiel', 'Daniel': 'Daniel',
    'Osée': 'Oséias', 'Joël': 'Joel', 'Amos': 'Amós', 'Abdias': 'Obadias',
    'Jonas': 'Jonas', 'Michée': 'Miquéias', 'Nahum': 'Naum', 'Habacuc': 'Habacuque',
    'Sophonie': 'Sofonias', 'Aggée': 'Ageu', 'Zacharie': 'Zacarias',
    'Malachie': 'Malaquias', 'Matthieu': 'Mateus', 'Marc': 'Marcos', 'Luc': 'Lucas',
    'Jean': 'João', 'Actes': 'Atos', 'Romains': 'Romanos',
    '1 Corinthiens': '1 Coríntios', '2 Corinthiens': '2 Coríntios',
    'Galates': 'Gálatas', 'Éphésiens': 'Efésios', 'Philippiens': 'Filipenses',
    'Colossiens': 'Colossenses', '1 Thessaloniciens': '1 Tessalonicenses',
    '2 Thessaloniciens': '2 Tessalonicenses', '1 Timothée': '1 Timóteo',
    '2 Timothée': '2 Timóteo', 'Tite': 'Tito', 'Philémon': 'Filemom',
    'Hébreux': 'Hebreus', 'Jacques': 'Tiago', '1 Pierre': '1 Pedro',
    '2 Pierre': '2 Pedro', '1 Jean': '1 João', '2 Jean': '2 João',
    '3 Jean': '3 João', 'Jude': 'Judas', 'Apocalypse': 'Apocalipse',
}


def decouper(reference):
    """'Éphésiens 2:8-9' -> ('Éphésiens', 2, [8, 9])"""
    m = re.match(r'^((?:[123]\s)?[^\d]+?)\s+(\d+):(\d+)(?:-(\d+))?$', reference.strip())
    if not m:
        return None
    livre, chap, v1, v2 = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4)
    return livre, chap, list(range(v1, int(v2) + 1)) if v2 else [v1]


def texte(index, livre, chap, versets):
    ch = index.get(livre, {}).get(chap)
    if not ch:
        return None
    morceaux = [ch.get(v) for v in versets]
    if any(m is None for m in morceaux):
        return None
    return ' '.join(m.strip() for m in morceaux)
