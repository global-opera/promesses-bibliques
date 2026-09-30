# -*- coding: utf-8 -*-
"""La page francaise est le modele. On n'y touche pas, sauf le texte biblique.

La page portugaise en est la traduction exacte : meme balisage, meme feuille de
style, meme script, memes sections, memes themes, memes references. Seuls
changent les mots et la version biblique.

  francais  : Louis Segond 1910 (domaine public)
  portugais : Biblia Livre (CC BY 3.0 BR)
"""
import io
import os
import re

import promesses_data as P

ICI = os.path.dirname(os.path.abspath(__file__))
MODELE = os.path.join(ICI, 'fr_original.html')     # la page francaise d'origine
SORTIE_FR = r'C:\Users\Stéphane CASSANI\Depots\promesses-bibliques\index.html'
SORTIE_PT = r'C:\Users\Stéphane CASSANI\Depots\promessas-biblicas\index.html'

# ------------------------------------------------- ce qui change d'une langue a l'autre

# Les sept sections et les trente-cinq themes portugais viennent de la version
# portugaise precedente : ce sont les traductions de Stephane, reprises telles quelles.
SECTIONS_PT = [
    'Se\u00e7\u00e3o 1: Salva\u00e7\u00e3o e Relacionamento com Deus',
    'Se\u00e7\u00e3o 2: Prote\u00e7\u00e3o e Provis\u00e3o',
    'Se\u00e7\u00e3o 3: For\u00e7a e Vit\u00f3ria',
    'Se\u00e7\u00e3o 4: Palavra e Sabedoria',
    'Se\u00e7\u00e3o 5: Vida Pr\u00e1tica e Fam\u00edlia',
    'Se\u00e7\u00e3o 6: Paz e Perseveran\u00e7a',
    'Se\u00e7\u00e3o 7: Volta de Cristo e Eternidade',
]

THEMES_PT = [
    'Salva\u00e7\u00e3o e Reden\u00e7\u00e3o', 'Amor de Deus', 'Esp\u00edrito Santo', 'Ora\u00e7\u00e3o',
    'Alegria', 'Prote\u00e7\u00e3o', 'Ref\u00fagio', 'Provis\u00e3o', 'Prosperidade', 'For\u00e7a',
    'Vit\u00f3ria', 'Batalha espiritual', 'Ansiedade e medo', 'Tristeza e luto',
    'Esperan\u00e7a', 'Palavra de Deus', 'Sabedoria', 'Dire\u00e7\u00e3o', 'Obedi\u00eancia',
    'Conhecimento', 'Fam\u00edlia', 'Filhos', 'Casamento', 'Trabalho', 'Cura', 'Paz',
    'Perd\u00e3o', 'Perseveran\u00e7a', 'Santidade', 'Paci\u00eancia', 'Volta de Cristo',
    'Novos c\u00e9us e terra', 'Ressurrei\u00e7\u00e3o', 'Fim do sofrimento', 'Morada eterna',
]

# Sous-titres portugais : mes traductions des sous-titres francais. A RELIRE.
SOUS_TITRES_PT = [
    'Vida eterna pela f\u00e9', 'Amor incondicional do Pai', 'Presen\u00e7a e poder divino',
    'Comunica\u00e7\u00e3o com Deus', 'Alegria do Senhor', 'Deus como escudo',
    'Abrigo na tempestade', 'Necessidades di\u00e1rias supridas', 'B\u00ean\u00e7\u00e3os materiais',
    'For\u00e7a na fraqueza', 'Triunfo sobre a adversidade', 'Armas espirituais',
    'Paz na ang\u00fastia', 'Consolo divino', 'Espera confiante', 'Luz e verdade',
    'Entendimento divino', 'Dire\u00e7\u00e3o nas escolhas', 'B\u00ean\u00e7\u00e3os da obedi\u00eancia',
    'Revela\u00e7\u00e3o divina', 'B\u00ean\u00e7\u00e3o familiar', 'Heran\u00e7a do Senhor',
    'Uni\u00e3o aben\u00e7oada', 'Fruto do trabalho', 'Sa\u00fade e restaura\u00e7\u00e3o',
    'Tranquilidade da alma', 'Miseric\u00f3rdia divina', 'Correr at\u00e9 o fim',
    'Vida consagrada', 'Esperar em Deus', 'Segunda vinda gloriosa',
    'Cria\u00e7\u00e3o renovada', 'Corpo glorificado', 'Sem dor nem l\u00e1grimas',
    'Casa do Pai',
]

# Les autres mots de l'interface : (francais d'origine, francais corrige, portugais)
INTERFACE = [
    ('<html lang="fr">', '<html lang="fr">', '<html lang="pt-BR">'),
    ('<title>\u271d\ufe0f Promesses de Dieu</title>',
     '<title>\u271d\ufe0f Promesses de Dieu</title>',
     '<title>\u271d\ufe0f Promessas de Deus</title>'),
    ('<h1>\u271d\ufe0f Promesses de Dieu</h1>',
     '<h1>\u271d\ufe0f Promesses de Dieu</h1>',
     '<h1>\u271d\ufe0f Promessas de Deus</h1>'),
    ('D\u00e9couvrez les promesses divines pour chaque situation de votre vie',
     'D\u00e9couvrez les promesses divines pour chaque situation de votre vie',
     'Descubra as promessas divinas para cada situa\u00e7\u00e3o da sua vida'),
    ('\u2190 Retour aux cat\u00e9gories',
     '\u2190 Retour aux cat\u00e9gories',
     '\u2190 Voltar \u00e0s categorias'),
    ('Application biblique interactive avec 35 cat\u00e9gories et 130+ versets '
     'des promesses de Dieu.',
     'Application biblique interactive avec 35 cat\u00e9gories et 113 versets '
     'des promesses de Dieu.',
     'Aplicativo b\u00edblico interativo com 35 categorias e 113 vers\u00edculos '
     'das promessas de Deus.'),
    ('35 cat\u00e9gories \u2022 130+ versets bibliques',
     '35 cat\u00e9gories \u2022 113 versets bibliques',
     '35 categorias \u2022 113 vers\u00edculos b\u00edblicos'),
    ('Version fran\u00e7aise Segond 21',
     'Version fran\u00e7aise \u2014 Louis Segond 1910, domaine public',
     'Vers\u00e3o em portugu\u00eas \u2014 B\u00edblia Livre, CC BY 3.0 BR'),
    ('Un outil de', 'Un outil de', 'Uma ferramenta da'),
]


# ------------------------------------------------------------------- la fabrication

def texte_biblique(ref, index, correspondance):
    livre, chap, versets = P.decouper(ref)
    t = P.texte(index, correspondance(livre), chap, versets)
    if t is None:
        raise SystemExit('Verset introuvable : %s' % ref)
    return t


def echapper(t):
    """Le texte part dans une chaine JavaScript entre guillemets doubles."""
    return t.replace('\\', '\\\\').replace('"', '\\"')


def construire(source, langue, index, correspondance, sortie,
               sections=None, themes=None, sous_titres=None):
    s = source

    # 1. les donnees : titre du theme, reference, texte biblique
    def refaire_theme(m):
        numero = int(m.group(1))
        titre = m.group(2)
        if themes:
            titre = '%d. %s' % (numero, themes[numero - 1])
        return '%s: {\n        title: "%s",' % (m.group(1), titre)

    s = re.sub(r'(\d+): \{\n        title: "([^"]*)",', refaire_theme, s)

    compteur = [0]

    def refaire_verset(m):
        ref = m.group(1)
        t = texte_biblique(ref, index, correspondance)
        if langue == 'pt':
            livre = P.decouper(ref)[0]
            ref = P.FR_VERS_PT[livre] + ref[len(livre):]
        compteur[0] += 1
        return 'reference: "%s",\n                text: "%s"' % (ref, echapper(t))

    s = re.sub(r'reference: "([^"]*)",\s*\n\s*text: "(?:[^"\\]|\\.)*"',
               refaire_verset, s)

    # 2. les titres de sections et les cartes
    if sections:
        for i, titre in enumerate(sections):
            vieux = re.search(r'<h2 class="section-title">Section %d[^<]*</h2>' % (i + 1), s)
            assert vieux, 'section %d introuvable' % (i + 1)
            s = s.replace(vieux.group(0), '<h2 class="section-title">%s</h2>' % titre)

    if themes:
        for i, titre in enumerate(themes):
            vieux = re.search(
                r'<div class="category-title">%d\. [^<]*</div>' % (i + 1), s)
            assert vieux, 'carte %d introuvable' % (i + 1)
            s = s.replace(vieux.group(0),
                          '<div class="category-title">%d. %s</div>' % (i + 1, titre))

    if sous_titres:
        cartes = re.findall(r'<div class="category-subtitle">([^<]*)</div>', s)
        assert len(cartes) == 35, len(cartes)
        for vieux, neuf in zip(cartes, sous_titres):
            s = s.replace('<div class="category-subtitle">%s</div>' % vieux,
                          '<div class="category-subtitle">%s</div>' % neuf, 1)

    # 3. les mots de l'interface
    # Certaines chaines apparaissent plusieurs fois : le bouton de retour figure
    # en haut et en bas du detail, la mention de version a trois endroits.
    colonne = 1 if langue == 'fr' else 2
    for entree in INTERFACE:
        vieux, neuf = entree[0], entree[colonne]
        assert s.count(vieux) >= 1, (langue, vieux[:50])
        s = s.replace(vieux, neuf)

    io.open(sortie, 'w', encoding='utf-8', newline='\n').write(s)
    print('ecrit : %s  (%d versets, %d o)' % (sortie, compteur[0], os.path.getsize(sortie)))


if __name__ == '__main__':
    source = io.open(MODELE, encoding='utf-8').read()
    assert source.count('reference: "') == 113, source.count('reference: "')

    construire(source, 'fr', P.charger_segond(),
               lambda l: P.FR_VERS_SEGOND.get(l, l), SORTIE_FR)
    construire(source, 'pt', P.charger_blivre(), lambda l: P.FR_VERS_PT[l], SORTIE_PT,
               sections=SECTIONS_PT, themes=THEMES_PT, sous_titres=SOUS_TITRES_PT)
