# -*- coding: utf-8 -*-
"""Mede transbordamento em cada .page do HTML de aprovacao, antes de virar PDF.

Existe porque em 25/08/2026 dois PDFs sairam quebrados sem ninguem perceber:
a peca estourava a margem e a copy do LinkedIn era cortada no meio. Extrair o
texto do PDF nao pega isso, so a medida de layout pega.
Uso:  python check_layout.py [arquivo.html]
"""
import json, os, subprocess, sys, tempfile, shutil

HTML = sys.argv[1] if len(sys.argv) > 1 else "_aprovacao.html"
def _cands():
    yield os.environ.get("CHROME_PATH", "")
    for var in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(var, "")
        if base:
            yield os.path.join(base, "Google", "Chrome", "Application", "chrome.exe")
    yield "/usr/bin/google-chrome"
    yield "/usr/bin/chromium"
    yield "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


CHROME = next((c for c in _cands() if c and os.path.exists(c)), None)
assert CHROME, "Chrome nao encontrado (defina CHROME_PATH)"

SONDA = """
<script>
window.addEventListener('load', function () {
  var out = [];
  document.querySelectorAll('.page').forEach(function (pg, i) {
    var lim = pg.getBoundingClientRect();
    var pior = 0, quem = '';
    pg.querySelectorAll('*').forEach(function (el) {
      var r = el.getBoundingClientRect();
      var d = Math.round(r.bottom - lim.bottom);
      if (d > pior) { pior = d; quem = el.className || el.tagName; }
    });
    out.push({p: i + 1, sobra: Math.round(lim.height - (pg.scrollHeight)),
              estouro: pior, quem: String(quem).slice(0, 40)});
  });
  document.title = 'SONDA' + JSON.stringify(out);
});
</script>
"""

src = open(HTML, encoding="utf-8").read()
tmp = tempfile.mkdtemp(prefix="sglay")           # caminho SEM espacos
alvo = os.path.join(tmp, "a.html")
open(alvo, "w", encoding="utf-8").write(src.replace("</body>", SONDA + "</body>")
                                        if "</body>" in src else src + SONDA)
r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=8000",
                    "--dump-dom", alvo], capture_output=True, text=True, encoding="utf-8")
shutil.rmtree(tmp, ignore_errors=True)

dom = r.stdout or ""
i = dom.find("SONDA[")
if i < 0:
    print("FALHOU: a sonda nao rodou"); raise SystemExit(2)
dados = json.loads(dom[i + 5: dom.index("]", i) + 1])

ruins = [d for d in dados if d["estouro"] > 2]
for d in dados:
    flag = "ESTOURA" if d["estouro"] > 2 else "ok     "
    print(f"  p{d['p']:02d}  {flag}  estouro={d['estouro']:>4}px  em <{d['quem']}>")
print("-" * 58)
if ruins:
    print(f"REPROVADO: {len(ruins)} pagina(s) com conteudo fora da margem.")
    raise SystemExit(1)
print("APROVADO: nenhuma pagina transborda.")
