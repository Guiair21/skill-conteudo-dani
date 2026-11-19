# -*- coding: utf-8 -*-
# ============================================================================
# TEMPLATE do PDF de APROVAÇÃO — skill "vamos-trabalhar"
# Layout: A4 RETRATO, fundo branco, Poppins.
# 25/08/2026: era A4 paisagem e saía quebrado em TODO pacote. Quatro defeitos consertados:
#   (1) .imgwrap/.card pediam 165mm de altura numa área útil menor, e a peça estourava a margem;
#   (2) a coluna de texto era ancorada no topo e deixava um terço da página em branco;
#   (3) .role tinha margin-top negativa e o número gigante colidia com o chip;
#   (4) o rodapé trazia um travessão, que a marca proíbe, e só existia na capa.
# A página agora é retrato porque a peça é vertical (4:5 e 9:16): peça em cima, ficha embaixo.
#
# ORDEM CANÔNICA (não inverter): Capa → ARTIGO → 1 página por card → Story → Legenda → Copy.
#   O artigo vem ANTES dos cards: quem aprova lê a tese primeiro, depois vê as peças.
#
# DOIS MODOS (perguntar a quem aprova qual quer, antes de gerar):
#   python gen_pdf.py          → "completo": capa + artigo + cards + story + legenda + copy
#   python gen_pdf.py cards    → "cards":    capa + cards + story  (sai como "... (cards).pdf")
#
# Pra reusar: troque só o bloco "CONTEÚDO" e os caminhos em "CONFIG". Rode com python.
#   - Se o PNG do card ainda não existir, entra um placeholder (dá pra gerar antes de renderizar).
#   - Blocos vazios (ARTIGO/STORY/LINKEDIN) são pulados sem quebrar.
# ============================================================================
import base64, os, subprocess, sys, tempfile, shutil, time, json, random
import requests, websocket

# ----------------------------- CONFIG ---------------------------------------
OUT        = os.path.dirname(os.path.abspath(__file__))   # pasta do trabalho (padrão: a pasta deste script)
IMG_DIR    = OUT                                    # onde estão os PNG dos cards
IMG_PATTERN= "card-{num}.png"                       # nome do PNG por card (num = 01, 02, ...)
STORY_PNG  = "story-1.png"                          # PNG do story (deixe "" se não houver)
FINAL_NAME = "Duplicata Escritural - APROVACAO.pdf"
LOGO_PATH  = os.path.join(OUT, "logo.png")          # logo da marca (versão escura: as páginas são brancas). Sem arquivo, sai sem logo
MARCA_RODAPE = "Nome da marca · @perfil"            # texto do rodapé de todas as páginas


def _achar_chrome():
    """Chrome via variável CHROME_PATH ou nos lugares padrão de cada sistema."""
    cands = [os.environ.get("CHROME_PATH", "")]
    for var in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(var, "")
        if base:
            cands.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
    cands += ["/usr/bin/google-chrome", "/usr/bin/chromium",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    raise SystemExit("Chrome não encontrado. Defina a variável de ambiente CHROME_PATH.")


CHROME     = _achar_chrome()

# MODO: "completo" (padrão) ou "cards". PERGUNTE a quem aprova antes de gerar.
MODO = (sys.argv[1] if len(sys.argv) > 1 else "completo").strip().lower()
if MODO not in ("completo", "cards"):
    raise SystemExit('MODO inválido. Use "completo" ou "cards".')
if MODO == "cards":
    FINAL_NAME = FINAL_NAME.replace(".pdf", " (cards).pdf")

# ----------------------------- CONTEÚDO -------------------------------------
COVER = {
 "serie":  "Duplicata Escritural",          # aparece no topo direito
 "kick":   "Carrossel para aprovação",
 "h1_a":   "Quem registra primeiro",        # 1ª linha do título (cor principal)
 "h1_b":   "leva o recebível",              # 2ª linha (cor de destaque)
 "formato":"carrossel Instagram · 8 cards · 1080×1350 (4:5)",
 "artigo": "\"Duplicata escritural: quem registra primeiro vai levar o recebível\"",
 "objetivo":"topo de funil / descoberta · educar por dados + autoridade",
 "posic":  "cliente atendido é o herói, a marca é o guia (StoryBrand)",
}

# card: (num, role/chip, txt_html)  — use <b> destaque, <i> apoio, <span class='k'>KICKER</span>, <span class='btn'>botão</span>
CARDS = [
 ("01","Capa · Gancho",
   "<span class='k'>A regra da antecipação vai mudar</span><b>Quem registra primeiro leva o recebível.</b><br>A nova duplicata escritural muda a fila de prioridade.<br><span class='btn'>Arraste pra ver →</span>"),
 ("02","O contexto",
   "<span class='k'>O papel está saindo de cena</span><b>A duplicata vira 100% digital</b>, registrada em ambiente central ligado ao Banco Central.<br><i>Res. BCB nº 339/2023</i>"),
 ("03","O que muda",
   "<b>A prioridade nasce no registro.</b><br>Antes pesava a data da assinatura. Agora vale quem <b>registra primeiro</b>."),
 ("04","O alerta",
   "<span class='k'>Onde mora o risco</span><b>No recebível que ainda vai nascer.</b><br>É aí que a nova ordem de prioridade pega mais forte."),
 ("05","Onde ficar de olho",
   "<span class='k'>Casos de atenção</span>Fornecimento por etapas · serviço contínuo · garantia sobre venda futura.<br>Nesses casos a proteção forte passa a ser o registro."),
 ("06","O lado bom",
   "<span class='k'>A casa já dizia antes de virar regra</span><b>Antecipar o mesmo título em dois bancos fica inviável.</b><br>O velho desconto em duplicidade perde a brecha. Os sócios já trataram disso <i>em artigo publicado</i>."),
 ("07","Antes do seu prazo",
   "<span class='k'>Sua lista</span>Mapear contratos · ajustar cláusulas · revisar garantias · conciliar recebíveis.<br>Quem se organiza antes chega na virada na frente."),
 ("08","Fechamento · CTA",
   "<b>Entenda o que muda pra sua empresa.</b><br>Artigo completo no link. <i>Link no story e na bio.</i>"),
]

# ARTIGO completo, em 2 páginas de 2 colunas. Use <h3> no título, <p class='sub'> nos intertítulos,
# <p class='src2'> no rodapé de fontes. Deixe as duas strings vazias se o pacote não tiver artigo.
ARTIGO_A = ""   # ex.: "<h3>Título do artigo</h3><p>lede...</p><p class='sub'>Intertítulo</p><p>...</p>"
ARTIGO_B = ""   # continuação + <p class='src2'><b>Fontes:</b> ...</p>

# Copy do story (o PNG entra à esquerda). Deixe "" se não houver story.
STORY_COPY = ("<span class='k'>Story · 1080×1920</span><b>Frase-âncora do story.</b><br>"
  "<i>Botão \"Ler o artigo\" + sticker de link com a URL (colar na hora de postar).</i>")

# Copy do LinkedIn. Deixe "" se não houver.
LINKEDIN = ""

LEGENDA = """A duplicata de papel está saindo de cena. A nova duplicata escritural chega digital e registrada, e traz uma regra nova: a prioridade sobre o seu recebível passa a ser de quem registra primeiro.<br><br>
Pra quem antecipa duplicata pra girar o caixa, isso mexe direto na garantia. E fecha a porta do velho desconto em duplicidade.<br><br>
Explicamos o que muda e o que fazer antes do seu prazo no artigo completo. Como está a preparação da sua empresa pra esse novo registro? Conta aqui embaixo.<br><br>
<span class='warn'>⚠️ Link do artigo a definir — publicar o artigo primeiro e colar no story / bio / 1º comentário.</span><br><br>
<span class='tags'>#gestaoempresarial #recebiveis #duplicataescritural #fluxodecaixa #antecipacao #reestruturacaoempresarial #gestaofinanceira</span>"""

# ----------------------------- LAYOUT FIXO ----------------
def b64_file(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

# logo opcional: sem arquivo, entra um pixel transparente
_PIXEL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
LOGO = b64_file(LOGO_PATH) if os.path.exists(LOGO_PATH) else _PIXEL

def card_img(num):
    p = os.path.join(IMG_DIR, IMG_PATTERN.format(num=num))
    if os.path.exists(p):
        return f'<img class="card" src="{b64_file(p)}">'
    return f'<div class="card ph">Card {num}<br><small>PNG a renderizar</small></div>'

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
@page{size:A4 portrait;margin:0}
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:'Poppins','Segoe UI',sans-serif;color:#1F2937}
.page{width:210mm;height:297mm;page-break-after:always;position:relative;background:#fff;
  padding:14mm 16mm 11mm;display:flex;flex-direction:column;overflow:hidden}
.top{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid #E4E1DB;padding-bottom:6mm}
.top img{height:7mm}
.top .meta{font-size:8pt;letter-spacing:2px;text-transform:uppercase;color:#9d9890;font-weight:600}
.top .meta b{color:#2F6FED}
/* rodape: em TODA pagina, e sem travessao */
.foot{flex:0 0 auto;margin-top:auto;padding-top:4mm;border-top:1px solid #EFEDE8;
  display:flex;justify-content:space-between;align-items:center;
  font-size:7.5pt;letter-spacing:1.2px;text-transform:uppercase;color:#9d9890}
/* ---- CAPA ---- */
.cover .mid{flex:1;display:flex;flex-direction:column;justify-content:flex-start;padding-top:32mm}
.cover .kick{font-size:11pt;letter-spacing:4px;text-transform:uppercase;color:#2F6FED;font-weight:700;margin-bottom:6mm}
.cover h1{font-size:34pt;font-weight:800;line-height:1.05;letter-spacing:-1px}
.cover h1 .am{color:#2F6FED}
.cover .info{margin-top:12mm;font-size:11pt;color:#55606e;line-height:1.9}
.cover .info b{color:#1F2937}
/* ---- PAGINA DE PECA: peca em cima, ficha embaixo ---- */
.slide{flex:1;display:flex;flex-direction:column;padding-top:7mm;min-height:0}
.slide .imgwrap{flex:0 0 auto;display:flex;justify-content:center;align-items:flex-start}
.slide img.card{height:176mm;width:auto;max-width:100%;object-fit:contain;
  border-radius:3mm;box-shadow:0 4mm 12mm rgba(21,33,50,.16)}
.slide .card.ph{height:176mm;width:141mm;border-radius:3mm;border:2px dashed #cfd6df;display:flex;
  flex-direction:column;align-items:center;justify-content:center;color:#a9b1bc;font-size:18pt;font-weight:700;text-align:center}
.slide .card.ph small{font-size:9pt;font-weight:500}
.slide .copy{flex:0 0 auto;display:flex;gap:8mm;align-items:flex-start;
  border-top:0.6mm solid #1F2937;margin-top:8mm;padding-top:5mm}
.slide .idcol{flex:0 0 auto;width:26mm}
.slide .num{font-size:30pt;font-weight:800;color:#1F2937;line-height:.9;letter-spacing:-1.5px}
.slide .role{display:block;font-size:7.5pt;letter-spacing:1.6px;text-transform:uppercase;
  color:#9d9890;font-weight:700;margin-top:2mm;line-height:1.3}
.slide .body{flex:1;min-width:0}
.slide .txt{font-size:11.5pt;line-height:1.55;color:#2b3543;font-weight:300}
.slide .txt b{font-weight:600;color:#1F2937}
.slide .txt i{font-style:normal;color:#7b8494}
.slide .k{display:block;font-size:8.5pt;letter-spacing:2px;text-transform:uppercase;color:#2F6FED;font-weight:700;margin-bottom:2.5mm}
.slide .btn{display:inline-block;border:1.2px solid #2F6FED;color:#1E50B8;border-radius:20mm;
  padding:1.2mm 4mm;font-size:9pt;font-weight:600;margin-top:3mm}
/* ---- LEGENDA / COPY ---- */
.leg .mid{flex:1;padding-top:8mm;min-height:0}
.leg h2{font-size:17pt;font-weight:800;margin-bottom:5mm}
.leg h2 .am{color:#2F6FED}
.leg .box{background:#F7F6F3;border:1px solid #E4E1DB;border-radius:3mm;padding:7mm 8mm;
  font-size:11pt;line-height:1.6;color:#2b3543}
/* copy longa em A4 retrato nao cabe em 1 coluna: transborda e corta o fim.
   Acima de COPY_LIMITE caracteres a caixa vira 2 colunas. */
.leg .box.cols{column-count:2;column-gap:8mm;font-size:9.5pt;line-height:1.55}
.leg .box.cols p{break-inside:avoid}
.leg .tags{color:#1E50B8;font-weight:500}
.leg .warn{color:#b5480f;font-weight:600;background:#FBEBDD;padding:1mm 2.5mm;border-radius:2mm}
/* ---- ARTIGO (2 colunas) ---- */
.art .mid{flex:1;padding-top:6mm;min-height:0}
.art h2{font-size:15pt;font-weight:800;margin-bottom:4mm}
.art h2 .am{color:#2F6FED}
.art .box{background:#fff;column-count:2;column-gap:9mm;font-size:10pt;line-height:1.5;color:#2b3543;font-weight:300}
.art .box h3{font-size:12pt;font-weight:800;color:#1F2937;line-height:1.15;margin-bottom:3mm;break-after:avoid}
.art .box p{margin-bottom:2.4mm}
.art .box p.sub,.art .box h3{break-inside:avoid;break-after:avoid}
.art .box p.sub{font-size:10.5pt;font-weight:700;color:#2F6FED;text-transform:uppercase;letter-spacing:1px;margin-top:2mm}
.art .box p.src2{font-size:8.5pt;color:#7b8494;margin-top:3mm}
.art .box b{font-weight:600;color:#1F2937}
.art .box i{font-style:italic;color:#55606e}
"""

N = len(CARDS)

COPY_LIMITE = 1400   # acima disso a caixa de copy vai para 2 colunas


def box_cls(texto):
    """Copy longa em pagina retrato precisa de 2 colunas, senao transborda."""
    return "box cols" if len(texto or "") > COPY_LIMITE else "box"


RODAPE = (f'<div class="foot"><span>{MARCA_RODAPE}</span>'
          '<span>Documento de aprovação</span></div>')


def pg_capa():
    return [f"""<div class="page cover">
  <div class="top"><img src="{LOGO}"><div class="meta"><b>{COVER['serie']}</b></div></div>
  <div class="mid">
    <div class="kick">{COVER['kick']}</div>
    <h1>{COVER['h1_a']}<br><span class="am">{COVER['h1_b']}</span></h1>
    <div class="info">
      <b>Formato:</b> {COVER['formato']}<br>
      <b>Artigo:</b> {COVER['artigo']}<br>
      <b>Objetivo:</b> {COVER['objetivo']}<br>
      <b>Posicionamento:</b> {COVER['posic']}
    </div>
  </div>
  {RODAPE}
</div>"""]


def pg_artigo():
    if not ARTIGO_A:
        return []
    out = [f"""<div class="page art">
  <div class="top"><img src="{LOGO}"><div class="meta">Artigo completo (1/2) · <b>{COVER['serie']}</b></div></div>
  <div class="mid">
    <h2>Artigo <span class="am">completo · LinkedIn / Blog</span></h2>
    <div class="box">{ARTIGO_A}</div>
  </div>
  {RODAPE}
</div>"""]
    if ARTIGO_B:
        out.append(f"""<div class="page art">
  <div class="top"><img src="{LOGO}"><div class="meta">Artigo completo (2/2) · <b>{COVER['serie']}</b></div></div>
  <div class="mid"><div class="box">{ARTIGO_B}</div></div>
  {RODAPE}
</div>""")
    return out


def pg_cards():
    return [f"""<div class="page">
  <div class="top"><img src="{LOGO}"><div class="meta">Card {num} / {N:02d} · <b>{COVER['serie']}</b></div></div>
  <div class="slide">
    <div class="imgwrap">{card_img(num)}</div>
    <div class="copy">
      <div class="idcol"><div class="num">{num}</div><span class="role">{role}</span></div>
      <div class="body"><div class="txt">{txt}</div></div>
    </div>
  </div>
  {RODAPE}
</div>""" for num, role, txt in CARDS]


def pg_story():
    p = os.path.join(IMG_DIR, STORY_PNG) if STORY_PNG else ""
    if not p or not os.path.exists(p):
        return []
    return [f"""<div class="page">
  <div class="top"><img src="{LOGO}"><div class="meta">Story · <b>{COVER['serie']}</b></div></div>
  <div class="slide">
    <div class="imgwrap"><img class="card" src="{b64_file(p)}"></div>
    <div class="copy">
      <div class="idcol"><div class="num">ST</div><span class="role">Story · link</span></div>
      <div class="body"><div class="txt">{STORY_COPY}</div></div>
    </div>
  </div>
  {RODAPE}
</div>"""]


def pg_copies():
    out = [f"""<div class="page leg">
  <div class="top"><img src="{LOGO}"><div class="meta">Legenda do post · <b>{COVER['serie']}</b></div></div>
  <div class="mid">
    <h2>Legenda <span class="am">do post (Instagram)</span></h2>
    <div class="{box_cls(LEGENDA)}">{LEGENDA}</div>
  </div>
  {RODAPE}
</div>"""]
    if LINKEDIN:
        out.append(f"""<div class="page leg">
  <div class="top"><img src="{LOGO}"><div class="meta">Copy LinkedIn · <b>{COVER['serie']}</b></div></div>
  <div class="mid">
    <h2>Copy <span class="am">do LinkedIn</span></h2>
    <div class="{box_cls(LINKEDIN)}">{LINKEDIN}</div>
  </div>
  {RODAPE}
</div>""")
    return out


# ORDEM CANÔNICA: o artigo vem ANTES dos cards.
if MODO == "completo":
    pages = pg_capa() + pg_artigo() + pg_cards() + pg_story() + pg_copies()
else:
    pages = pg_capa() + pg_cards() + pg_story()

html = "<!doctype html><html><head><meta charset='utf-8'><style>"+CSS+"</style></head><body>"+"".join(pages)+"</body></html>"
SRC = os.path.join(OUT, "_aprovacao.html")
with open(SRC, "w", encoding="utf-8") as f: f.write(html)
print("HTML:", SRC, "| cards:", N)

# ----------------------------- IMPRIME VIA CDP (retrato) ---------------------
FINAL = os.path.join(OUT, FINAL_NAME)
PORT = random.randint(9400, 9800)
udd = tempfile.mkdtemp(prefix="crcdp_")
uri = "file:///" + SRC.replace("\\", "/")
proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
    "--user-data-dir=" + udd, f"--remote-debugging-port={PORT}",
    "--remote-allow-origins=*", uri],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ws = None
try:
    ws_url = None
    for _ in range(60):
        try:
            tabs = requests.get(f"http://127.0.0.1:{PORT}/json", timeout=1).json()
            ps = [t for t in tabs if t.get("type") == "page" and "webSocketDebuggerUrl" in t]
            if ps: ws_url = ps[0]["webSocketDebuggerUrl"]; break
        except Exception: pass
        time.sleep(0.2)
    if not ws_url: raise RuntimeError("nao conectou ao Chrome CDP")
    ws = websocket.create_connection(ws_url, max_size=64*1024*1024, suppress_origin=True)
    _id = 0
    def cmd(method, params=None):
        global _id
        _id += 1; mid = _id
        ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == mid: return m
    cmd("Page.enable"); cmd("Page.navigate", {"url": uri})
    t0 = time.time()
    while time.time() - t0 < 20:
        try:
            m = json.loads(ws.recv())
            if m.get("method") == "Page.loadEventFired": break
        except Exception: break
    time.sleep(1.5)
    res = cmd("Page.printToPDF", {"landscape": False, "displayHeaderFooter": False,
        "printBackground": True, "preferCSSPageSize": True})
    data = res.get("result", {}).get("data")
    if not data: raise RuntimeError("printToPDF sem dados")
    tmp_pdf = os.path.join(tempfile.gettempdir(), "aprov_cdp.pdf")
    with open(tmp_pdf, "wb") as f: f.write(base64.b64decode(data))
    if os.path.exists(FINAL): os.remove(FINAL)
    shutil.move(tmp_pdf, FINAL)
    print("OK ->", FINAL, os.path.getsize(FINAL), "bytes")
finally:
    try:
        if ws: ws.close()
    except Exception: pass
    proc.terminate()
    try: proc.wait(timeout=5)
    except Exception: proc.kill()
    shutil.rmtree(udd, ignore_errors=True)
