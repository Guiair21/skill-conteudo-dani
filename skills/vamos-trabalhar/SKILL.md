---
name: vamos-trabalhar
description: GATILHO OBRIGATÓRIO quando a usuária disser "vamos trabalhar" em qualquer forma, ou pedir para produzir conteúdo de um cliente do começo ao fim, principalmente artigo e produção editorial (também post, carrossel, roteiro, pacote de aprovação). Pensado para conteúdo de controladoria, contabilidade, gestão financeira e tributário. Responda sempre em português.
model: sonnet
---

# Vamos trabalhar · conteúdo do começo ao fim

Atalho de produção. **O fluxo mora na skill `produzir-conteudo`**, que é genérica e serve a
qualquer cliente. Esta skill só escolhe o cliente, aponta as referências da área e dispara o motor.

## O que fazer

1. **Descobrir o cliente.** Listar as subpastas de `config/` na raiz do repositório (ou da pasta
   em `MOTOR_CONFIG_DIR`). Se só existir uma além de `exemplo`, usar essa. Se houver mais de uma,
   perguntar qual, junto com o tema e o objetivo, numa mensagem só. Se só existir `exemplo`, avisar
   que a config precisa ser preenchida antes (ver `README.md`) e parar.
2. **Rodar a skill `produzir-conteudo`** com `cliente = <nome da pasta>`, **no modo autônomo**:
   colher tema e objetivo uma vez e ir até o pacote final sem checkpoint. As quatro exceções que
   fazem parar estão no contrato de operação do motor.
3. Config do cliente em `config/<cliente>/`: `perfil`, `voz`, `formatos`, `provas`, `marca`,
   `biblioteca`, `paths.json`.
4. Ler `referencias/linha-de-montagem.md` do motor. É o mapa das estações.

## Ativos que moram aqui

O motor e a config apontam para estes arquivos. **Não movê-los sem atualizar a referência.**

| Caminho | O que é |
|---|---|
| `referencias/fontes-confiaveis.md` | radar de fontes por área: controladoria, contabilidade, FP&A, BI, tributário e reforma, crédito e recebíveis, reestruturação. Estação 3 |
| `referencias/linha-de-montagem.md` | versão comentada do elenco. A genérica, que vale, está no motor |
| `templates/check_fontes.py` | checagem de fontes: todo dado com link |
| `templates/gen_pdf_aprovacao_template.py` | **template do PDF de aprovação.** A4 **retrato**, fundo branco. Trocar só os blocos `CONFIG` e `CONTEÚDO` |
| `templates/check_layout.py` | **obrigatório antes de entregar PDF.** Mede transbordamento em cada página do `_aprovacao.html` (precisa de Chrome ou Chromium) |

## O que fica com quem aprova

Tudo que publica, envia ou grava em serviço externo (rede social, e-mail marketing, site,
planilha compartilhada) **o fluxo não faz**. O pacote sai pronto e quem aprova publica.

## Lições que vieram junto

**A4 paisagem é o formato errado para peça vertical** (4:5 e 9:16). O PDF de aprovação é A4
retrato, com a peça em cima e a ficha embaixo. Copy acima de 1.400 caracteres cai em 2 colunas.
Extrair texto do PDF não pega página cortada; só a medida de layout (`check_layout.py`) pega.

**Imagem depende do formato, e o nível de esforço não decide isso.** Carrossel de nível 1 também
passa pela estação de imagem.

**Tese derrubada depois da escrita mata o pacote inteiro.** Por isso o teste da tese roda na
estação 2b, antes do texto.

## Skills irmãs (opcionais)

Se estiverem instaladas, o motor as usa; senão, faz o passo à mão. Lista completa e o que fazer
sem cada uma no `README.md` da raiz.
