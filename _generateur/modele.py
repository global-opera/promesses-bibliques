# -*- coding: utf-8 -*-
"""Le modele complet de l'application : 7 sections, 35 categories, 113 versets.
Lu dans la version francaise, qui fait reference."""
import io
import re

import promesses_data as P


def lire_modele():
    s = io.open(P.FR_APP, encoding='utf-8', errors='replace').read()
    corps = s[s.index('<div id="mainView">'):]

    # Les cartes contiennent des <div> imbriques : on ne peut pas decouper la
    # grille par expression reguliere. On repere donc sections et cartes par
    # leur POSITION, et chaque carte revient a la derniere section au-dessus.
    sections = []
    for m in re.finditer(r'<span class="section-icon">([^<]*)</span>\s*'
                         r'<h2 class="section-title">([^<]*)</h2>', corps, re.S):
        sections.append(dict(pos=m.start(), icone=m.group(1).strip(),
                             titre=m.group(2).strip(), cartes=[]))

    for m in re.finditer(r'onclick="showCategory\((\d+)\)">\s*'
                         r'<div class="category-icon">([^<]*)</div>\s*'
                         r'<div class="category-title">([^<]*)</div>\s*'
                         r'<div class="category-subtitle">([^<]*)</div>', corps, re.S):
        courante = [s for s in sections if s['pos'] < m.start()][-1]
        courante['cartes'].append(dict(num=int(m.group(1)), icone=m.group(2).strip(),
                                       titre=m.group(3).strip(),
                                       sous_titre=m.group(4).strip()))

    versets = {num: [r for r, _ in v] for num, _, _, v in P.lire_categories()}
    for sec in sections:
        for c in sec['cartes']:
            c['refs'] = versets[c['num']]
    return sections


if __name__ == '__main__':
    m = lire_modele()
    print('sections :', len(m))
    total_cartes = sum(len(s['cartes']) for s in m)
    total_refs = sum(len(c['refs']) for s in m for c in s['cartes'])
    print('categories :', total_cartes)
    print('versets    :', total_refs)
    print()
    for sec in m:
        print('%s %s' % (sec['icone'], sec['titre']))
        for c in sec['cartes']:
            print('    %2d. %s  %-28s | %-34s | %d versets'
                  % (c['num'], c['icone'], c['titre'][3:][:28], c['sous_titre'][:34],
                     len(c['refs'])))
        print()
