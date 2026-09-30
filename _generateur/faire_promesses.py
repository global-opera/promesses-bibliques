# -*- coding: utf-8 -*-
"""Produit les DEUX applications « Promesses de Dieu » depuis un seul modele.

La parite entre le francais et le portugais est garantie par construction :
meme balisage, meme feuille de style, meme script. Seuls changent la langue
et la version biblique, toutes deux libres de droits :
  - francais  : Louis Segond 1910 (domaine public)
  - portugais : Biblia Livre (CC BY 3.0 BR)
"""
import io
import json
import os

import promesses_data as P
MODELE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'modele_promesses.json')

SORTIE_FR = r'C:\Users\Stéphane CASSANI\Depots\promesses-bibliques\index.html'
SORTIE_PT = r'C:\Users\Stéphane CASSANI\Depots\promessas-biblicas\index.html'

# --------------------------------------------------------- les mots de chaque langue

FR = dict(
    lang='fr',
    titre='Promesses de Dieu',
    description="Les promesses de Dieu pour chaque situation de la vie : "
                "35 themes, 113 versets, texte Louis Segond 1910.",
    tagline='Les promesses de Dieu pour chaque situation de votre vie',
    compte='7 sections · 35 themes · 113 versets',
    retour='Retour aux themes',
    haut='Haut de page',
    fermer='Fermer',
    intro_titre='Comment s\u2019en servir',
    intro="Choisissez un theme : les versets qui s\u2019y rapportent s\u2019affichent, "
          "avec leur reference. Rien a installer, rien a donner.",
    version_titre='Le texte biblique',
    version="Version <strong>Louis Segond 1910</strong>, libre de droits.",
    autres="Autres ressources : <a href=\"https://manialibris.com/ressources.html\">"
           "manialibris.com</a>",
    pied='Mania Libris',
)

PT = dict(
    lang='pt-BR',
    titre='Promessas de Deus',
    description="As promessas de Deus para cada situa\u00e7\u00e3o da vida: "
                "35 temas, 113 vers\u00edculos, texto da B\u00edblia Livre.",
    tagline='As promessas de Deus para cada situa\u00e7\u00e3o da sua vida',
    compte='7 se\u00e7\u00f5es \u00b7 35 temas \u00b7 113 vers\u00edculos',
    retour='Voltar aos temas',
    haut='Topo da p\u00e1gina',
    fermer='Fechar',
    intro_titre='Como usar',
    intro="Escolha um tema: os vers\u00edculos correspondentes aparecem, com a sua "
          "refer\u00eancia. Nada para instalar, nada para informar.",
    version_titre='O texto b\u00edblico',
    version="Vers\u00e3o <strong>B\u00edblia Livre</strong>, sob licen\u00e7a CC BY 3.0 BR "
            "\u2014 \u00a9 Diego Santos, Mario S\u00e9rgio e Marco Teles.",
    autres="Outros recursos: <a href=\"https://manialibris.com/recursos.html\">"
           "manialibris.com</a>",
    pied='Mania Libris',
)

# Les sept sections et les trente-cinq themes portugais viennent de la version
# portugaise existante : ce sont des traductions deja validees.
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

# Sous-titres portugais : traduction des sous-titres francais. A RELIRE.
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

# --------------------------------------------------------------------- le gabarit

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
 background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
 min-height:100vh;color:#333;line-height:1.6}
.container{max-width:1100px;margin:0 auto;padding:30px 20px 60px}
header{text-align:center;color:#fff;margin-bottom:30px}
h1{font-size:2.6rem;margin-bottom:10px;text-wrap:balance}
header p{font-size:1.1rem;opacity:.92}
header .compte{font-size:.95rem;opacity:.78;margin-top:8px;font-variant-numeric:tabular-nums}
.carte{background:#fff;border-radius:16px;padding:26px 28px;margin-bottom:22px;
 box-shadow:0 8px 28px rgba(0,0,0,.16)}
.carte h2{font-size:1.15rem;color:#764ba2;margin-bottom:8px}
.carte p{color:#555;font-size:.98rem}
.carte a{color:#667eea}
.section{background:#fff;border-radius:16px;padding:26px 28px;margin-bottom:22px;
 box-shadow:0 8px 28px rgba(0,0,0,.16)}
.section-header{display:flex;align-items:center;gap:12px;border-bottom:2px solid #f0f0f5;
 padding-bottom:14px;margin-bottom:20px}
.section-icon{font-size:1.5rem}
.section-title{font-size:1.25rem;color:#764ba2}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px}
.theme{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border:0;
 border-radius:12px;padding:20px 18px;text-align:left;cursor:pointer;font:inherit;
 transition:transform .2s,box-shadow .2s}
.theme:hover{transform:translateY(-4px);box-shadow:0 10px 24px rgba(118,75,162,.4)}
.theme-icon{font-size:1.8rem;display:block;margin-bottom:10px}
.theme-title{display:block;font-weight:600;font-size:1rem;margin-bottom:4px}
.theme-sub{display:block;font-size:.85rem;opacity:.85}
.detail{display:none}
.detail.on{display:block}
.vue.off{display:none}
.retour{background:#fff;color:#764ba2;border:0;border-radius:10px;padding:11px 22px;
 font:inherit;font-weight:600;cursor:pointer;margin-bottom:20px;
 box-shadow:0 4px 14px rgba(0,0,0,.18)}
.retour:hover{background:#f3f0fa}
.verset{background:#f8f9fa;border-left:4px solid #667eea;border-radius:8px;
 padding:18px 20px;margin-bottom:14px}
.verset .ref{color:#764ba2;font-weight:600;margin-bottom:6px}
.verset .txt{color:#333}
.source{color:#999;font-size:.88rem;margin-top:18px}
.verset{cursor:pointer}
.verset:hover{background:#f0eefb}
.modale{position:fixed;inset:0;background:rgba(40,25,70,.86);display:none;
 align-items:center;justify-content:center;padding:24px;z-index:10}
.modale.on{display:flex}
.modale-boite{background:#fff;border-radius:16px;padding:34px 32px;max-width:640px;
 width:100%;max-height:82vh;overflow:auto;position:relative}
.modale-ref{color:#764ba2;font-weight:600;font-size:1.1rem;margin-bottom:14px}
.modale-txt{font-size:1.25rem;line-height:1.75}
.modale-fermer{position:absolute;top:12px;right:14px;border:0;background:none;
 font-size:1.6rem;line-height:1;color:#999;cursor:pointer}
.modale-fermer:hover{color:#764ba2}
.haut{position:fixed;right:24px;bottom:24px;width:46px;height:46px;border:0;
 border-radius:50%;background:#fff;color:#764ba2;font-size:1.2rem;cursor:pointer;
 box-shadow:0 6px 18px rgba(0,0,0,.25);opacity:0;pointer-events:none;
 transition:opacity .25s}
.haut.on{opacity:1;pointer-events:auto}
footer{text-align:center;color:#fff;opacity:.8;font-size:.9rem;margin-top:10px}
button:focus-visible,a:focus-visible{outline:3px solid #fff;outline-offset:3px}
@media (prefers-reduced-motion:reduce){.theme,.haut{transition:none}
 .theme:hover{transform:none}}
@media (max-width:600px){.container{padding:20px 14px 50px}h1{font-size:2rem}
 .section,.carte{padding:20px 18px}.grille{grid-template-columns:1fr}}
"""

JS = """
const DONNEES = %(donnees)s;
const MOTS = %(mots)s;

const vueThemes = document.getElementById('themes');
const vueDetail = document.getElementById('detail');
const titreDetail = document.getElementById('detail-titre');
const listeDetail = document.getElementById('detail-versets');

function ouvrir(n) {
  const t = DONNEES[n];
  titreDetail.textContent = t.icone + '  ' + t.titre;
  listeDetail.innerHTML = t.versets.map(v =>
    '<div class="verset"><div class="ref"></div><div class="txt"></div></div>').join('');
  [...listeDetail.children].forEach((el, i) => {
    el.querySelector('.ref').textContent = t.versets[i].ref;
    el.querySelector('.txt').textContent = t.versets[i].texte;
  });
  vueThemes.classList.add('off');
  vueDetail.classList.add('on');
  history.pushState({ theme: n }, '', '#' + n);
  window.scrollTo(0, 0);
}

function fermer(pousser) {
  vueDetail.classList.remove('on');
  vueThemes.classList.remove('off');
  if (pousser !== false) history.pushState({}, '', '#');
  window.scrollTo(0, 0);
}

document.querySelectorAll('.theme').forEach(b =>
  b.addEventListener('click', () => ouvrir(Number(b.dataset.n))));
document.getElementById('retour').addEventListener('click', () => fermer());

// le bouton « precedent » du navigateur ferme le theme au lieu de quitter
addEventListener('popstate', e => {
  if (e.state && e.state.theme) ouvrir(e.state.theme); else fermer(false);
});

const modale = document.getElementById('modale');
listeDetail.addEventListener('click', e => {
  const bloc = e.target.closest('.verset');
  if (!bloc) return;
  document.getElementById('modale-ref').textContent = bloc.querySelector('.ref').textContent;
  document.getElementById('modale-txt').textContent = bloc.querySelector('.txt').textContent;
  modale.classList.add('on');
});
const fermerModale = () => modale.classList.remove('on');
document.getElementById('modale-fermer').addEventListener('click', fermerModale);
modale.addEventListener('click', e => { if (e.target === modale) fermerModale(); });
addEventListener('keydown', e => { if (e.key === 'Escape') fermerModale(); });

const haut = document.getElementById('haut');
addEventListener('scroll', () => haut.classList.toggle('on', scrollY > 400));
haut.addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));

// une adresse du type ...#12 ouvre directement le theme 12
if (location.hash.length > 1 && DONNEES[Number(location.hash.slice(1))]) {
  ouvrir(Number(location.hash.slice(1)));
}
"""

PAGE = u"""<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="%(description)s">
<title>%(titre)s</title>
<style>%(css)s</style>
</head>
<body>
<div class="container">

<header id="top">
  <h1>%(titre)s</h1>
  <p>%(tagline)s</p>
  <p class="compte">%(compte)s</p>
</header>

<div class="carte">
  <h2>%(intro_titre)s</h2>
  <p>%(intro)s</p>
</div>

<div id="themes" class="vue">
%(sections)s
</div>

<div id="detail" class="detail">
  <button class="retour" id="retour">&larr; %(retour)s</button>
  <div class="section">
    <div class="section-header"><h2 class="section-title" id="detail-titre"></h2></div>
    <div id="detail-versets"></div>
    <p class="source">%(version)s</p>
  </div>
</div>

<div class="carte">
  <h2>%(version_titre)s</h2>
  <p>%(version)s</p>
  <p>%(autres)s</p>
</div>

<footer>%(pied)s</footer>
</div>

<div class="modale" id="modale" role="dialog" aria-modal="true" aria-labelledby="modale-ref">
  <div class="modale-boite">
    <button class="modale-fermer" id="modale-fermer" aria-label="%(fermer)s">&times;</button>
    <div class="modale-ref" id="modale-ref"></div>
    <div class="modale-txt" id="modale-txt"></div>
  </div>
</div>

<button class="haut" id="haut" aria-label="%(haut)s">&uarr;</button>
<script>%(js)s</script>
</body>
</html>
"""


def construire(modele, langue, mots, sections_titres, themes_titres, sous_titres,
               index_biblique, correspondance_livre, sortie):
    donnees, html_sections = {}, []
    n_verset = 0

    for i, sec in enumerate(modele):
        cartes = []
        for carte in sec['cartes']:
            n = carte['num']
            titre = ('%d. %s' % (n, themes_titres[n - 1])) if themes_titres \
                else carte['titre']
            sous = sous_titres[n - 1] if sous_titres else carte['sous_titre']
            versets = []
            for ref in carte['refs']:
                livre, chap, vs = P.decouper(ref)
                texte = P.texte(index_biblique, correspondance_livre(livre), chap, vs)
                if texte is None:
                    raise SystemExit('Verset introuvable : %s (%s)' % (ref, langue))
                versets.append(dict(ref=traduire_reference(ref, langue), texte=texte))
                n_verset += 1
            donnees[n] = dict(icone=carte['icone'], titre=titre, versets=versets)
            cartes.append(
                '      <button class="theme" data-n="%d">'
                '<span class="theme-icon">%s</span>'
                '<span class="theme-title">%s</span>'
                '<span class="theme-sub">%s</span></button>'
                % (n, carte['icone'], titre, sous))
        html_sections.append(
            '  <div class="section">\n'
            '    <div class="section-header"><span class="section-icon">%s</span>'
            '<h2 class="section-title">%s</h2></div>\n'
            '    <div class="grille">\n%s\n    </div>\n  </div>'
            % (sec['icone'], sections_titres[i] if sections_titres else sec['titre'],
               '\n'.join(cartes)))

    champs = dict(mots)
    champs['css'] = CSS
    champs['sections'] = '\n'.join(html_sections)
    champs['js'] = JS % dict(
        donnees=json.dumps(donnees, ensure_ascii=False, indent=None),
        mots=json.dumps({'retour': mots['retour']}, ensure_ascii=False))
    io.open(sortie, 'w', encoding='utf-8', newline='\n').write(PAGE % champs)
    print('ecrit : %s  (%d versets, %d o)'
          % (sortie, n_verset, os.path.getsize(sortie)))


def traduire_reference(ref, langue):
    """« Éphésiens 2:8-9 » -> « Efésios 2:8-9 » pour le portugais."""
    if langue == 'fr':
        return ref
    livre, chap, vs = P.decouper(ref)
    reste = ref[len(livre):].strip()
    return '%s %s' % (P.FR_VERS_PT[livre], reste)


if __name__ == '__main__':
    # Le modele est fige dans un JSON : le generateur ne depend plus de la
    # page francaise, qu'il ecrase. Un ecrasement ne detruit plus la source.
    MODELE = json.load(io.open(MODELE_JSON, encoding='utf-8'))
    assert len(MODELE) == 7, len(MODELE)
    assert sum(len(s['cartes']) for s in MODELE) == 35
    assert sum(len(c['refs']) for s in MODELE for c in s['cartes']) == 113

    construire(MODELE, 'fr', FR, None, None, None, P.charger_segond(),
               lambda l: P.FR_VERS_SEGOND.get(l, l), SORTIE_FR)
    construire(MODELE, 'pt', PT, SECTIONS_PT, THEMES_PT, SOUS_TITRES_PT,
               P.charger_blivre(), lambda l: P.FR_VERS_PT[l], SORTIE_PT)
