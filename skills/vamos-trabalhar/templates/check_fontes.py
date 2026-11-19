# -*- coding: utf-8 -*-
# ============================================================================
# PORTAO DE FONTES — skill "vamos-trabalhar"
#
# POR QUE ISSO EXISTE (16/07/2026): o pacote FIDC foi produzido e APROVADO no loop
# com "Dados 9" estampando "R$ 1 trilhao" cuja fonte (Capital Aberto) retornava 404.
# A verificacao era auto-declarada: bastava eu escrever "Fonte: X" e ninguem abria o X.
# Este script troca a promessa por prova mecanica.
#
# O QUE ELE FAZ: le o fontes.json do pacote e REPROVA (exit 1) se:
#   1. a URL nao responde 200 (link morto = dado nao verificavel = nao publica);
#   2. um dado marcado "heroi" (card de dado, story, capa) for PROJECAO e nao observado;
#   3. um dado "heroi" vier de fonte SECUNDARIA;
#   4. faltar o trecho literal que sustenta o numero (prova de leitura);
#   5. a publicacao for mais velha que "validade_dias" sem reverificacao no periodo.
#
# USO:  python check_fontes.py            (valida o fontes.json da mesma pasta)
#       python check_fontes.py --quiet    (so o veredito)
# O gen_pdf.py chama este script sozinho antes de gerar. Nao gera se reprovar.
#
# VALVULA: nenhuma automatica. Pra publicar com dado irregular, quem aprova decide na mao
# e o registro fica no fontes.json (campo "excecao_autorizada" + motivo).
# ============================================================================
import json, os, sys
from datetime import date, datetime

try:
    import requests
except ImportError:
    print("FALTA: pip install requests"); sys.exit(2)

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
OK, ERRO, AVISO = "  [ok]  ", "  [ERRO]", "  [aviso]"


def carregar(pasta=None):
    p = os.path.join(pasta or AQUI, "fontes.json")
    if not os.path.exists(p):
        print(f"{ERRO} nao achei o fontes.json em {p}")
        print("         Todo pacote com numero precisa de um. Modelo: veja o cabecalho da skill.")
        return None, p
    with open(p, encoding="utf-8") as f:
        return json.load(f), p


# status do teste de link
VIVO, MORTO, INCERTO = "vivo", "morto", "incerto"

# 404/410/451 e falha de DNS sao link morto de verdade. 403/429 e timeout sao
# defesa anti-robo do site, e dizem nada sobre o dado.
HTTP_MORTO = {404, 410, 451}


def testa_url(url, tentativas=2):
    """Devolve (status, detalhe), com status em VIVO / MORTO / INCERTO.

    17/08/2026: o portao reprovou um pacote inteiro por "link morto" em PDFs de
    RI que estavam vivos e ja tinham sido lidos. Duas descobertas:

    1. O CDN da MZ (api.mziq.com) NAO responde HEAD em arquivo grande. O release
       de 1,6 MB pendura ate o timeout; o fato relevante de 315 KB responde em
       1,7 s. Por isso o resultado parecia intermitente.
    2. Depois de muitas requisicoes seguidas ao mesmo arquivo, o CDN passa a
       recusar tudo. Bloqueio anti-robo, nao link quebrado.

    A regra antiga tratava as duas coisas como link morto e travava a peca. Agora
    o portao separa: 404 continua reprovando (foi o caso do Capital Aberto que fez
    este script nascer), e bloqueio ou timeout viram AVISO de "confira na mao".
    """
    if not url:
        return MORTO, "sem url"
    ultimo = "?"
    for _ in range(tentativas):
        try:
            r = requests.get(url, headers=UA, timeout=25, allow_redirects=True,
                             stream=True)
            r.close()  # so o status interessa, nao baixa o corpo
            if r.status_code == 200:
                return VIVO, f"HTTP {r.status_code}"
            if r.status_code in HTTP_MORTO:
                return MORTO, f"HTTP {r.status_code}"
            ultimo = f"HTTP {r.status_code}"
        except Exception as e:
            # Nao classificar falha de rede como link morto. Em 17/08/2026 tres
            # veiculos que tinham respondido 200 minutos antes apareceram como
            # "dominio nao resolve" numa oscilacao de DNS da propria maquina, e o
            # portao quase mandou trocar fonte boa. So o servidor dizendo 404
            # prova que o link morreu.
            ultimo = f"falhou: {type(e).__name__}"
    return INCERTO, ultimo


def testa_urls(urls):
    """Testa cada URL UNICA uma vez so. Devolve {url: (status, detalhe)}.

    17/08/2026: seis dados do pacote apontavam pro mesmo release de RI, e o
    portao baixava o PDF seis vezes. Cinco passavam e a sexta estourava timeout,
    reprovando o pacote por um link que estava vivo. Agora cada URL e testada uma
    vez, e o resultado vale pra todos os dados que a citam.
    """
    unicas = sorted({u for u in urls if u})
    return {u: testa_url(u) for u in unicas}


def dias(iso):
    try:
        return (date.today() - datetime.strptime(iso, "%Y-%m-%d").date()).days
    except Exception:
        return None


def validar(pasta=None, quiet=False):
    doc, caminho = carregar(pasta)
    if doc is None:
        return 1
    validade = doc.get("validade_dias", 45)
    fontes = doc.get("fontes", [])
    if not fontes:
        print(f"{ERRO} fontes.json sem nenhuma fonte."); return 1

    erros, avisos, excecoes = 0, 0, 0
    if not quiet:
        print(f"\nPORTAO DE FONTES — {doc.get('pacote','(sem nome)')} — {len(fontes)} dado(s)\n")
    cache_url = testa_urls([f.get("url") for f in fontes])

    for f in fontes:
        rot = f.get("id") or f.get("afirmacao", "?")[:40]
        heroi = bool(f.get("heroi"))
        tipo = (f.get("tipo") or "").lower()
        excecao = f.get("excecao_autorizada")

        # 1. link vivo
        status_url, det = cache_url.get(f.get("url"), (MORTO, "sem url"))
        if status_url == VIVO:
            if not quiet: print(f"{OK} {rot} — link vivo ({det})")
        elif status_url == MORTO:
            print(f"{ERRO} {rot} — LINK MORTO ({det}) — {f.get('url')}")
            erros += 1
        else:
            print(f"{AVISO} {rot} — link NAO VERIFICAVEL automaticamente ({det}). "
                  f"O site bloqueia robo. Abra na mao antes de publicar: {f.get('url')}")
            avisos += 1

        # 2. heroi tem que ser observado
        if heroi and tipo != "observado":
            if excecao:
                print(f"{AVISO} {rot} — e '{tipo or 'sem tipo'}' e esta como numero-heroi. "
                      f"Liberado por excecao autorizada.")
                avisos += 1
            else:
                print(f"{ERRO} {rot} — e '{tipo or 'sem tipo'}' e esta como numero-heroi. "
                      f"Heroi so aceita dado OBSERVADO. Projecao vai pro corpo, rotulada.")
                erros += 1

        # 3. heroi tem que ser primaria
        if heroi and not f.get("primaria", False):
            if excecao:
                print(f"{AVISO} {rot} — heroi apoiado em fonte SECUNDARIA ({f.get('veiculo','?')}). "
                      f"Liberado por excecao autorizada.")
                avisos += 1
            else:
                print(f"{ERRO} {rot} — heroi apoiado em fonte SECUNDARIA ({f.get('veiculo','?')}). "
                      f"Busque a primaria.")
                erros += 1

        # 4. prova de leitura
        if not (f.get("trecho") or "").strip():
            print(f"{ERRO} {rot} — sem 'trecho' literal. Cole a frase da fonte que sustenta o numero.")
            erros += 1

        # 5. validade
        d_pub, d_ver = dias(f.get("data_publicacao", "")), dias(f.get("data_verificacao", ""))
        if d_pub is None:
            print(f"{ERRO} {rot} — data_publicacao ausente/invalida (use AAAA-MM-DD)."); erros += 1
        elif d_pub > validade and (d_ver is None or d_ver > validade):
            print(f"{AVISO} {rot} — publicado ha {d_pub} dias (limite {validade}). "
                  f"Confira se ja saiu numero mais novo antes de publicar.")
            avisos += 1

        if excecao:
            print(f"{AVISO} {rot} — EXCECAO AUTORIZADA por quem aprova: {excecao}")
            excecoes += 1

    print()
    if erros:
        print(f"REPROVADO: {erros} erro(s), {avisos} aviso(s). O PDF NAO sera gerado.")
        print("Conserte o fontes.json (ou o dado) e rode de novo.")
        return 1
    if excecoes:
        print(f"APROVADO COM EXCECAO: 0 erro, {avisos} aviso(s), "
              f"{excecoes} dado(s) liberado(s) na mao por quem aprova.")
        print("A excecao vale so pra este pacote e fica registrada no fontes.json.")
        return 0
    print(f"APROVADO: 0 erro, {avisos} aviso(s).")
    return 0


# ---- helpers pros geradores (fonte unica da verdade) ----
def _fmt(f):
    br = lambda iso: datetime.strptime(iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    t = f'{f.get("veiculo","")}, "{f.get("titulo","")}"'
    try:
        t += f', publicado em {br(f["data_publicacao"])}'
    except Exception:
        pass
    if f.get("tipo") == "projecao":
        t += " [projecao]"
    return t


def fontes_html(pasta=None):
    """<p class='src2'>Fontes: ...</p> pro PDF/artigo, montado do fontes.json."""
    doc, _ = carregar(pasta)
    if not doc:
        return ""
    itens = "; ".join(_fmt(f) for f in doc.get("fontes", []))
    return f"<p class='src2'><b>Fontes:</b> {itens}.</p>"


def fontes_bullets(pasta=None):
    """Lista de strings pro .docx."""
    doc, _ = carregar(pasta)
    if not doc:
        return []
    out = []
    for f in doc.get("fontes", []):
        linha = _fmt(f)
        if f.get("url"):
            linha += ". " + f["url"]
        out.append(linha)
    return out


if __name__ == "__main__":
    sys.exit(validar(quiet="--quiet" in sys.argv))
