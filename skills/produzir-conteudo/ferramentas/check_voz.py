# -*- coding: utf-8 -*-
"""Varre um texto contra os padrões banidos da marca. Portátil: só stdlib.

Existe porque "rodei o revisor de estilo e deu 9,5" não é verificação: é declaração.
Em 29/07/2026 um agente afirmou "0 travessões" num arquivo que tinha um na linha 1.

Uso:
    python check_voz.py <arquivo> [--cliente exemplo]

Saída: as ocorrências, uma por linha, e um resumo. Exit code 1 se achou algo.
COLE A SAÍDA no arquivo de revisão. Sem a saída colada, a verificação não aconteceu.
"""
import argparse, io, os, re, sys

# Windows usa cp1252 em saída redirecionada e quebra em emoji (corrigido em 06/11/2026).
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, 'reconfigure'):
        _s.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _clientes import pasta_cliente

# Padrões da casa. Cada um é porteiro: se o texto viola, reprova e reescreve.
PADROES = [
    ('falso contraste',
     r'[Nn]ão (é|são|foi|era|se trata|basta) .{2,70}[,.;] ?(é|são|foi|era|mas|É|São)'),
    ('falso contraste (vírgula)', r', não [a-z]'),
    ('falso contraste (mas sim)', r'\bmas sim\b'),
    ('não apenas / não só', r'\bnão (apenas|só)\b'),
    ('nunca é', r'\bnunca é\b'),
    ('travessão longo', r'—'),
    ('vocabulário-robô',
     r'\b(jornada|potencializar|mergulh\w*|divisor de águas|em última análise|'
     r'desbloquear|revolucionári\w*|intrincad\w*|testemunho de|tapeçaria|'
     r'orquestrar|imperativo|inestimável|paisagem em evolução|cenário em evolução)\b'),
    # Anunciar o próprio efeito em vez de produzir o efeito. O narrador avisa
    # que o que vem é forte, e com isso denuncia que não confia no texto.
    # Regra de quem aprova, 26/08/2026: "esse tipo de frase não tem porque existir".
    ('anuncia o próprio efeito',
     r'(?i)(de um jeito que não deixa|não deixa saída|e é pior|porque ela é dur|'
     r'isso é duro|presta atenção|repare bem|leia de novo|leia isso de novo|'
     r'devia constranger|devia incomodar|aqui dói|preste atenção n)'),
    ('advérbio colado',
     r'\b(transforma|impacta|evolui|muda|melhora|cresce)\s+'
     r'(profundamente|diretamente|constantemente|significativamente|drasticamente)\b'),
]


def trinca(texto):
    """Três frases curtas seguidas, o padrão de impacto forçado. Regex não pega bem."""
    achados = []
    for i, par in enumerate(texto.split('\n'), 1):
        # lista numerada ou com bullet não é trinca: é lista. Sem isso, todo
        # checklist de 3 itens vira falso positivo e o alerta perde credibilidade.
        if re.match(r'\s*([-*+]|\d+[.)]|#{1,6})\s', par) or re.search(r'\d+\.\s.*<br>', par):
            continue
        frases = [f.strip() for f in re.split(r'(?<=[.!?])\s+', par) if f.strip()]
        seq = 0
        for f in frases:
            if len(f) <= 45:
                seq += 1
                if seq == 3:
                    achados.append((i, ' / '.join(frases[:3])[:90]))
                    break
            else:
                seq = 0
    return achados


def main():
    ap = argparse.ArgumentParser(description='Varredura de padrões banidos.')
    ap.add_argument('arquivo')
    ap.add_argument('--cliente', default='', help='usa regras extras do voz.md do cliente')
    a = ap.parse_args()

    if not os.path.isfile(a.arquivo):
        sys.exit(f'arquivo não encontrado: {a.arquivo}')

    texto = io.open(a.arquivo, encoding='utf-8', errors='ignore').read()
    linhas = texto.split('\n')

    print(f'VARREDURA DE VOZ · {os.path.basename(a.arquivo)}')
    if a.cliente:
        voz = os.path.join(pasta_cliente(a.cliente), 'voz.md')
        print(f'regras: {voz}' + ('' if os.path.isfile(voz) else '  (NÃO ENCONTRADO)'))
    print('-' * 62)

    total = 0
    for nome, padrao in PADROES:
        for i, linha in enumerate(linhas, 1):
            for m in re.finditer(padrao, linha):
                total += 1
                ctx = linha.strip()
                if len(ctx) > 88:
                    ini = max(0, m.start() - 30)
                    ctx = ('...' if ini else '') + linha[ini:ini + 88].strip() + '...'
                print(f'  L{i:<4} [{nome}] {ctx}')

    for i, ctx in trinca(texto):
        total += 1
        print(f'  L{i:<4} [trinca de frases curtas] {ctx}')

    print('-' * 62)
    if total:
        print(f'REPROVADO: {total} ocorrência(s). Reescrever antes de seguir.')
        sys.exit(1)
    print('APROVADO: nenhuma ocorrência.')
    sys.exit(0)


if __name__ == '__main__':
    main()
