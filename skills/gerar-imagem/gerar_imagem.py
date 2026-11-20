#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_imagem.py — ponte Claude Code -> Codex (tool image_gen.imagegen) -> arquivo na pasta do cliente.

A tool integrada do Codex salva sempre em CODEX_HOME/generated_images/<thread>/exec-*.png
e não aceita caminho de destino. O JSONL de --json também não devolve o caminho.
Então quem controla o destino é este script: fotografa a pasta antes, roda o Codex,
e move o que apareceu de novo.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ.parent / "produzir-conteudo" / "ferramentas"))
from _clientes import pasta_cliente as _pasta_cliente  # config/<cliente> ou MOTOR_CONFIG_DIR


def pasta_cliente(nome: str) -> Path:
    return Path(_pasta_cliente(nome))


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))


def fotografar(raiz: Path) -> set:
    if not raiz.exists():
        return set()
    return {p for p in raiz.rglob("*.png")}


def slugificar(txt: str, limite: int = 48) -> str:
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", "-", txt).strip("-").lower()
    return (txt[:limite].rstrip("-")) or "imagem"


def pasta_destino(args) -> Path:
    if args.saida:
        return Path(args.saida)
    if args.cliente:
        pj = pasta_cliente(args.cliente) / "paths.json"
        if pj.exists():
            dados = json.loads(pj.read_text(encoding="utf-8"))
            base = pasta_cliente(args.cliente)  # caminho relativo vale a partir da config
            if dados.get("imagens"):
                return base / dados["imagens"]
            if dados.get("producao"):
                return base / dados["producao"] / "Imagens-geradas"
        sys.exit(f"ERRO: cliente '{args.cliente}' nao tem 'imagens' nem 'producao' em paths.json. Use --saida.")
    return Path.cwd()


def bloco_marca(nome: str) -> str:
    f = pasta_cliente(nome) / "marca.md"  # identidade visual vem da config do cliente
    if not f.exists():
        sys.exit(f"ERRO: nao achei {f}. Use --marca com o nome da pasta do cliente em config/.")
    return f.read_text(encoding="utf-8").strip()


def montar_prompt(args) -> str:
    partes = []
    if args.marca:
        partes.append(bloco_marca(args.marca))
    partes.append("BRIEFING DA IMAGEM:\n" + args.briefing.strip())
    if args.ref:
        caminhos = "\n".join(f"- {Path(r).resolve()}" for r in args.ref)
        partes.append(
            "EDICAO: parta das imagens abaixo, passando os caminhos em "
            "referenced_image_paths:\n" + caminhos
        )
    if args.variacoes > 1:
        partes.append(
            f"Gere {args.variacoes} variacoes desta mesma ideia, uma chamada da "
            "ferramenta por variacao. Varie composicao e enquadramento, nao o assunto."
        )
    partes.append(
        "COMO EXECUTAR: use a ferramenta integrada image_gen (built-in). Nao use a API, "
        "nao use scripts/image_gen.py, nao escreva codigo Python e nao instale nada. "
        "Nao copie, nao mova e nao renomeie arquivo nenhum: o destino final e "
        "responsabilidade do script que te chamou. Ao terminar, responda so com a "
        "contagem de imagens geradas."
    )
    return "\n\n".join(partes)


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera imagem pelo Codex e salva na pasta do cliente.")
    ap.add_argument("briefing", help="descricao da imagem")
    ap.add_argument("--cliente", help="nome da pasta do cliente em config/")
    ap.add_argument("--marca", help="cliente cujo marca.md entra no prompt (normalmente o mesmo de --cliente)")
    ap.add_argument("--nome", help="slug do arquivo final; padrao vem do briefing")
    ap.add_argument("--saida", help="pasta de destino; sobrepoe --cliente")
    ap.add_argument("--ref", action="append", default=[], help="imagem de referencia para edicao (repetivel)")
    ap.add_argument("--variacoes", type=int, default=1, help="quantas imagens gerar na mesma chamada")
    ap.add_argument("--timeout", type=int, default=900, help="segundos ate abortar (padrao 900)")
    ap.add_argument("--abrir", action="store_true", help="abre a pasta de destino no fim")
    ap.add_argument("--seco", action="store_true", help="mostra o prompt e o comando, sem executar")
    ap.add_argument("--modelo", default=None,
                    help="modelo do Codex (padrao: o do config.toml)")
    ap.add_argument("--sandbox", default="unelevated",
                    help="windows.sandbox do Codex; 'elevated' quebrou com 'setup refresh had errors' em 20/10/2026")
    args = ap.parse_args()

    destino = pasta_destino(args)
    destino.mkdir(parents=True, exist_ok=True)
    prompt = montar_prompt(args)

    raiz_img = codex_home() / "generated_images"
    ultima_msg = destino / ".codex-ultima-msg.txt"

    cmd = ["cmd.exe", "/c", "codex", "exec", "--skip-git-repo-check",
           "-c", f'windows.sandbox="{args.sandbox}"',
           "--enable", "image_generation", "--disable", "apps", "--json", "-C", str(destino),
           "-o", str(ultima_msg)]
    if args.modelo:
        cmd[5:5] = ["-m", args.modelo]
    for r in args.ref:
        cmd += ["--add-dir", str(Path(r).resolve().parent)]
    cmd.append("-")

    if args.seco:
        print("COMANDO:", " ".join(cmd))
        print("\nPROMPT:\n" + prompt)
        return 0

    antes = fotografar(raiz_img)
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, input=prompt.encode("utf-8"),
                              capture_output=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f"ERRO: o Codex passou de {args.timeout}s sem terminar.", file=sys.stderr)
        return 3
    segundos = round(time.time() - t0, 1)

    # A pasta do Codex e compartilhada: duas geracoes ao mesmo tempo roubam o
    # arquivo uma da outra. Por isso o corte e pelo thread desta execucao, e a
    # diferenca de pastas fica so como rede de seguranca.
    thread = None
    saida = proc.stdout.decode("utf-8", "replace")
    for linha in saida.splitlines():
        if '"thread.started"' in linha:
            try:
                thread = json.loads(linha).get("thread_id")
            except json.JSONDecodeError:
                pass
    if thread and (raiz_img / thread).exists():
        novos = sorted((raiz_img / thread).glob("*.png"), key=lambda p: p.stat().st_mtime)
    else:
        novos = sorted(fotografar(raiz_img) - antes, key=lambda p: p.stat().st_mtime)

    if not novos:
        print(f"ERRO: nenhuma imagem nova em {raiz_img} depois de {segundos}s.", file=sys.stderr)
        print("--- saida do codex ---", file=sys.stderr)
        print(saida[-2000:], file=sys.stderr)
        print(proc.stderr.decode("utf-8", "replace")[-1000:], file=sys.stderr)
        return 2

    base = args.nome or slugificar(args.briefing)
    hoje = date.today().strftime("%Y-%m-%d")
    finais = []
    for origem in novos:
        n = 1
        while True:
            sufixo = "" if n == 1 else f"-{n}"
            alvo = destino / f"{hoje}-{base}{sufixo}.png"
            if not alvo.exists():
                break
            n += 1
        shutil.copy2(origem, alvo)
        finais.append(str(alvo))

    if ultima_msg.exists():
        ultima_msg.unlink()

    print(json.dumps({
        "arquivos": finais,
        "destino": str(destino),
        "segundos": segundos,
        "thread": thread,
        "origem_codex": [str(p) for p in novos],
    }, ensure_ascii=False, indent=2))

    if args.abrir:
        os.startfile(str(destino))  # noqa: S606
    return 0


if __name__ == "__main__":
    sys.exit(main())
