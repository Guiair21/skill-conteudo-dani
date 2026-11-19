# -*- coding: utf-8 -*-
"""Responde "já saiu algo igual?" com fato, não com memória. Portátil: só stdlib.

Existe porque em 29/07/2026 um agente respondeu "não saiu algo igual" sobre Reforma
Tributária, e o acervo tinha 29 peças do tema, três delas com taxa acima de 50%.

Uso:
    python busca_acervo.py "reforma tributaria" --cliente exemplo
    python busca_acervo.py "caixa|capital de giro" --cliente exemplo --top 15

COLE A SAÍDA no portao.md. Sem a saída colada, a pergunta 4 não foi respondida.
"""
import argparse, glob, io, json, os, re, sys

# Windows usa cp1252 em saída redirecionada e quebra em emoji (corrigido em 06/11/2026).
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, 'reconfigure'):
        _s.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _clientes import pasta_cliente


def carrega_paths(cliente):
    p = os.path.join(pasta_cliente(cliente), 'paths.json')
    if not os.path.isfile(p):
        sys.exit(f'falta {p}\nCrie com: {{"acervo": {{"LinkedIn": "<caminho>", ...}}}}')
    return json.load(io.open(p, encoding='utf-8'))


def campo(t, nome):
    # [ \t]* e não \s*: \s engole a quebra de linha e captura a linha seguinte
    # quando o campo está vazio, que é o caso das notas sem taxa.
    m = re.search(rf'^{nome}:[ \t]*"?([^"\n]*)"?', t, re.M)
    return m.group(1).strip() if m else ''


def main():
    ap = argparse.ArgumentParser(description='O que já saiu sobre um tema.')
    ap.add_argument('termo', help='regex; use | para alternativas')
    ap.add_argument('--cliente', required=True)
    ap.add_argument('--top', type=int, default=12, help='quantas peças listar')
    a = ap.parse_args()

    paths = carrega_paths(a.cliente)
    acervo = paths.get('acervo', {})
    if not acervo:
        sys.exit('paths.json sem a chave "acervo"')

    try:
        rx = re.compile(a.termo, re.I)
    except re.error as e:
        sys.exit(f'regex inválida: {e}')

    achados = []
    for canal, pasta in acervo.items():
        # caminho relativo é lido a partir da pasta de config do cliente
        pasta = os.path.join(pasta_cliente(a.cliente), pasta)
        if not os.path.isdir(pasta):
            print(f'  ! pasta não encontrada: {pasta}', file=sys.stderr)
            continue
        for f in glob.glob(os.path.join(pasta, '*.md')):
            t = io.open(f, encoding='utf-8', errors='ignore').read()
            if not rx.search(t):
                continue
            taxa = campo(t, 'taxa_engajamento')
            achados.append({
                'data': campo(t, 'data_publicacao') or '?',
                'canal': canal,
                'formato': campo(t, 'formato_post') or '?',
                'taxa': float(taxa) if taxa else None,
                'confiavel': campo(t, 'alcance_confiavel') == 'sim',
                'servico': campo(t, 'servico'),
                'grau': campo(t, 'grau_consciencia'),
                'arq': os.path.basename(f)[:-3],
            })

    print(f'JÁ SAIU SOBRE "{a.termo}" · cliente {a.cliente}')
    print('=' * 74)
    if not achados:
        print('NADA no acervo. Território inédito.')
        sys.exit(0)

    print(f'TOTAL: {len(achados)} peça(s)\n')

    # Taxa acima de 100% é impossível como engajamento ÷ alcance: indica erro no dado.
    # Fica fora do ranking e aparece separada para conferência (06/11/2026).
    com_taxa = [x for x in achados if x['confiavel'] and x['taxa'] is not None and x['taxa'] <= 100]
    suspeitas = [x for x in achados if x['confiavel'] and x['taxa'] is not None and x['taxa'] > 100]
    if com_taxa:
        print(f'--- as {min(a.top, len(com_taxa))} de melhor taxa (só alcance confiável) ---')
        for x in sorted(com_taxa, key=lambda r: -r['taxa'])[:a.top]:
            print(f"  {x['data']}  {x['canal']:<10} {x['formato']:<14} "
                  f"{x['taxa']:>6.2f}%  {x['arq'][:44]}")
        print()

    if suspeitas:
        print(f'--- {len(suspeitas)} com taxa acima de 100%, fora do ranking: conferir o dado ---')
        for x in sorted(suspeitas, key=lambda r: -r['taxa'])[:a.top]:
            print(f"  {x['data']}  {x['canal']:<10} {x['formato']:<14} "
                  f"{x['taxa']:>6.2f}%  {x['arq'][:44]}")
        print()

    print(f'--- as {min(a.top, len(achados))} mais recentes ---')
    for x in sorted(achados, key=lambda r: r['data'], reverse=True)[:a.top]:
        t = '     .'
        if x['confiavel'] and x['taxa'] is not None:
            t = f"{x['taxa']:>6.2f}%" if x['taxa'] <= 100 else '  erro?'
        print(f"  {x['data']}  {x['canal']:<10} {x['formato']:<14} {t}  {x['arq'][:44]}")

    fmt = {}
    for x in achados:
        fmt[x['formato']] = fmt.get(x['formato'], 0) + 1
    print(f"\n--- por formato --- {' · '.join(f'{k}: {v}' for k, v in sorted(fmt.items(), key=lambda i: -i[1]))}")

    print('\nLEITURA: território com muitas peças exige ângulo novo, não repetição.')
    sys.exit(0)


if __name__ == '__main__':
    main()
