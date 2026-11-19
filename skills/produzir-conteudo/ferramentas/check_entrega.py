# -*- coding: utf-8 -*-
"""Audita a pasta de um trabalho antes de dizer que está pronto. Portátil: só stdlib.

Existe porque em 29/07/2026 um fluxo se declarou "concluído com sucesso, média 9,4"
tendo entregue: PDF com 7 placeholders e nenhum card, zero fontes com link, e um
portão que respondeu "não saiu algo igual" sobre um tema com 47 peças no acervo.

Nenhuma dessas falhas foi detectada porque as verificações eram declarativas.
Este script troca declaração por evidência: ou o arquivo prova, ou reprova.

Uso:
    python check_entrega.py "<pasta do trabalho>" [--cliente exemplo]

Exit code 1 se algo reprovou. Rode ANTES de anunciar entrega.
"""
import argparse, datetime as dt, glob, io, os, re, subprocess, sys

# Windows usa cp1252 em saída redirecionada e quebra em emoji (corrigido em 06/11/2026).
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, 'reconfigure'):
        _s.reconfigure(encoding='utf-8', errors='replace')

FERRAMENTAS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _clientes import pasta_cliente


def ler(p):
    return io.open(p, encoding='utf-8', errors='ignore').read()


def main():
    ap = argparse.ArgumentParser(description='Audita a entrega de um trabalho.')
    ap.add_argument('pasta')
    ap.add_argument('--cliente', default='')
    a = ap.parse_args()

    if not os.path.isdir(a.pasta):
        sys.exit(f'pasta não encontrada: {a.pasta}')

    falhas, avisos, ok = [], [], []

    # ---------------------------------------------------------------- portão
    portao = os.path.join(a.pasta, 'portao.md')
    # Arquivos de PROCESSO não contam como "texto da peça": eles nascem e são
    # reescritos junto com o portão. 'segunda-opiniao.md' (estação 2b) e
    # 'revisao.md' (estação 5) entraram em 07/08/2026, quando a 2b passou a
    # rodar ANTES da escrita: quando ela fere a tese, o portão roda de novo e
    # fica legitimamente mais novo que o registro do teste.
    #
    # 11/08/2026: entraram mais quatro. 'apuracao-*' (dado bruto que não virou
    # peça), 'verificacao-*' (auditoria de pesquisa externa), 'transcricao-*'
    # (fala de fonte, que é INSUMO e costuma chegar depois do primeiro portão e
    # derrubar a tese) e 'objecoes-*'. O caso que forçou a mudança: a diretora
    # jurídica do cliente derrubou o ângulo por áudio DEPOIS da estação 5, o
    # portão rodou pela terceira vez e o script reprovou a pasta por isso.
    # Registro de fonte que chega tarde é o fluxo funcionando, não descuido.
    PREFIXOS_PROCESSO = ('apuracao-', 'verificacao-', 'transcricao-', 'objecoes-')
    PROCESSO = ('portao.md', 'estrategia.md', 'segunda-opiniao.md', 'revisao.md')
    textos = [f for f in glob.glob(os.path.join(a.pasta, '*.md'))
              if os.path.basename(f) not in PROCESSO
              and not os.path.basename(f).startswith(PREFIXOS_PROCESSO)]
    if not os.path.isfile(portao):
        falhas.append('portao.md NÃO EXISTE. O portão de pauta foi pulado.')
    else:
        t = ler(portao)
        mais_novo = [f for f in textos
                     if os.path.getmtime(f) < os.path.getmtime(portao)]
        if mais_novo:
            falhas.append(f'portao.md é MAIS NOVO que {len(mais_novo)} arquivo(s) de texto. '
                          'Foi preenchido depois de escrever, o que é o mesmo que não ter portão.')
        else:
            ok.append('portao.md existe e antecede os textos')

        # a pergunta 4 exige a saída do busca_acervo colada
        if not re.search(r'JÁ SAIU SOBRE|TOTAL:\s*\d+\s*peça|NADA no acervo', t):
            falhas.append('portao.md não traz a saída do busca_acervo.py colada. '
                          'A pergunta "já saiu algo igual?" foi respondida de memória.')
        else:
            ok.append('portão traz a consulta ao acervo colada')

        # pergunta 6: o CTA promete algo que a casa consegue entregar?
        # Campo obrigatório desde 07/08/2026, depois de uma peça de conversão ter
        # ido a aprovação prometendo um levantamento que ainda era serviço em desenho.
        if not re.search(r'ENTREGA\??\s*[:\|]?', t) or not re.search(
                r'prateleira|em desenho|n[ãa]o existe', t, re.I):
            falhas.append('portao.md não responde a pergunta 6 (ENTREGA?). '
                          'O CTA promete algo sem dizer se a casa entrega: '
                          'prateleira, em desenho ou não existe.')
        else:
            ok.append('portão declara a capacidade de entrega do CTA')

        if re.search(r'APROVAD', t, re.I) and re.search(r'REPROVAD', t, re.I) is None:
            m = re.search(r'TOTAL:\s*(\d+)\s*peça', t)
            if m and int(m.group(1)) > 15:
                avisos.append(f'portão APROVOU um tema com {m.group(1)} peças no acervo. '
                              'Território saturado exige ângulo novo declarado.')

    # ---------------------------------------------------------------- peça visual
    # Busca RECURSIVA: o pipeline costuma gravar os PNG em subpasta ('cards/'),
    # e a contagem só da raiz dizia "0 PNG" ao lado de um OK, o que lia como
    # aprovação e era cegueira. Corrigido em 07/08/2026.
    htmls = glob.glob(os.path.join(a.pasta, '**', '*.html'), recursive=True)
    pngs = glob.glob(os.path.join(a.pasta, '**', '*.png'), recursive=True)
    ph_total = 0
    for h in htmls:
        ph_total += len(re.findall(r'class="card ph"', ler(h)))
    if ph_total:
        falhas.append(f'{ph_total} PLACEHOLDER(S) no PDF/HTML de aprovação e {len(pngs)} PNG na pasta. '
                      'Os cards não foram renderizados: o PDF mostra retângulos tracejados.')
    elif htmls and not pngs:
        falhas.append('há HTML de peça visual e NENHUM PNG em lugar nenhum da pasta. '
                      'Roteiro de card não é card: renderize antes de montar o material.')
    elif htmls:
        ok.append(f'nenhum placeholder no material de aprovação ({len(pngs)} PNG renderizados)')

    # ---------------------------------------------------------------- fontes
    conteudo = [f for f in textos if 'conteudo' in os.path.basename(f).lower()]
    for c in conteudo:
        t = ler(c)
        tem_numero = re.search(r'\b\d+([.,]\d+)?\s*(%|mil|milh|bilh|R\$)', t)
        tem_link = 'http' in t
        if tem_numero and not tem_link:
            falhas.append(f'{os.path.basename(c)} tem dado numérico e NENHUM link. '
                          'A regra é fonte primária datada com link para todo dado.')
        elif tem_numero:
            ok.append(f'{os.path.basename(c)}: dados com link presente')

    # ---------------------------------------------------------------- voz
    for c in conteudo:
        # subprocess e não os.system: caminho com espaço quebra no shell do Windows
        p = subprocess.run([sys.executable, os.path.join(FERRAMENTAS, 'check_voz.py'), c],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        if p.returncode != 0:
            n = re.search(r'REPROVADO: (\d+)', p.stdout or '')
            falhas.append(f'{os.path.basename(c)} reprovou na varredura de voz '
                          f'({n.group(1) if n else "?"} ocorrência(s)). Rode check_voz.py e veja.')
        else:
            ok.append(f'{os.path.basename(c)}: varredura de voz limpa')

    # ---------------------------------------------------------------- editor
    rev = glob.glob(os.path.join(a.pasta, '*revis*.md'))
    for r_ in rev:
        t = ler(r_)
        if not re.search(r'\b(aceito|recusado)\b', t, re.I):
            falhas.append(f'{os.path.basename(r_)} não tem o bloco de decisão do editor '
                          '(aceito/recusado por linha). Parecer sem decisão registrada não fecha.')
        else:
            ok.append('editor estratégico com decisão registrada')

    # ---------------------------------------------------------------- carrossel pela skill (opcional)
    # Carrossel no padrão marca_projeto_slide-NN_4x5_vNN.png só passa se o PROCESSO da skill de
    # carrossel foi cumprido (propostas, escolha, revisão, texto, entrega). PNG sozinho não prova
    # nada. Opcional: só roda se a variável CARROSSEL_CHECK_SCRIPT apontar para o script de checagem
    # da skill de carrossel (ele recebe marca e projeto como argumentos).
    SKILL_CARROSSEL = os.environ.get('CARROSSEL_CHECK_SCRIPT', '')
    achados_c = set()
    if SKILL_CARROSSEL and os.path.isfile(SKILL_CARROSSEL):
        for p_c in glob.glob(os.path.join(a.pasta, '**', '*.png'), recursive=True):
            m_c = re.match(r'^([a-z0-9-]+)_(.+)_slide-\d{2}_4x5_v\d{2}\.png$', os.path.basename(p_c))
            if m_c:
                achados_c.add((m_c.group(1), m_c.group(2)))
    for marca_c, proj_c in sorted(achados_c):
        pc = subprocess.run([sys.executable, '-I', SKILL_CARROSSEL, marca_c, proj_c],
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
        if pc.returncode != 0:
            falhas.append(f'carrossel {marca_c}/{proj_c}: processo da skill NÃO cumprido. '
                          + (pc.stdout or '').strip().replace(chr(10), ' | '))
        else:
            ok.append(f'carrossel {marca_c}/{proj_c}: processo da skill cumprido')

    # ---------------------------------------------------------------- validade do formatos.md
    # Estação 9 do motor: até 60 dias OK; acima de 60 avisa; acima de 90 só passa com a
    # linha explícita "DADO VELHO: <motivo>" no portao.md. Texto solto não vale, porque
    # "nenhum dado velho foi usado" também contém as palavras.
    if not a.cliente:
        avisos.append('validade do formatos.md não conferida: falta --cliente.')
    else:
        fmt = os.path.join(pasta_cliente(a.cliente), 'formatos.md')
        if not os.path.isfile(fmt):
            avisos.append(f'formatos.md não encontrado para {a.cliente}: validade não conferida.')
        else:
            m = re.search(r'(?:última apuração|apurado|apuração)(?: em| de)?:?\s*\*{0,2}(\d{2}/\d{2}/\d{4})',
                          ler(fmt), re.I)
            try:
                dias = (dt.date.today() - dt.datetime.strptime(m.group(1), '%d/%m/%Y').date()).days
            except (AttributeError, ValueError):
                dias = None
                avisos.append('formatos.md sem data de apuração legível: validade não conferida.')
            if dias is not None and dias < 0:
                avisos.append(f'formatos.md com data de apuração no futuro ({m.group(1)}): validade não conferida.')
            elif dias is not None and dias > 90:
                decl = ler(portao) if os.path.isfile(portao) else ''
                # Motivo real: exige texto depois da marca, e recusa negação, vazio e o modelo.
                decl_m = re.search(r'^\W*DADO VELHO\W*:\W*(.*)$', decl, re.M)
                motivo = decl_m.group(1).strip(' *_`') if decl_m else ''
                if (len(motivo) >= 10 and '<' not in motivo
                        and not re.match(r'(não|nao|nenhum|nenhuma|sem|n/?a)\b', motivo, re.I)):
                    avisos.append(f'formatos.md tem {dias} dias, e o portao.md declara o dado velho. Propor reapuração.')
                else:
                    falhas.append(f'formatos.md tem {dias} dias (limite 90). Reapure ou escreva no portao.md '
                                  'a linha "DADO VELHO: <motivo>".')
            elif dias is not None and dias > 60:
                avisos.append(f'formatos.md tem {dias} dias (limite de aviso 60). Propor reapuração a quem aprova.')
            elif dias is not None:
                ok.append(f'formatos.md apurado há {dias} dias')

    # ---------------------------------------------------------------- saída
    print(f'AUDITORIA DA ENTREGA · {os.path.basename(a.pasta)}')
    print('=' * 72)
    for x in ok:
        print(f'  OK      {x}')
    for x in avisos:
        print(f'  AVISO   {x}')
    for x in falhas:
        print(f'  FALHA   {x}')
    print('=' * 72)
    if falhas:
        print(f'REPROVADO: {len(falhas)} falha(s). NÃO anunciar entrega.')
        sys.exit(1)
    print('APROVADO' + (f' com {len(avisos)} aviso(s)' if avisos else '') + '.')
    sys.exit(0)


if __name__ == '__main__':
    main()
