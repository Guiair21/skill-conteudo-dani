---
name: produzir-conteudo
description: Use quando for produzir conteúdo de um cliente do começo ao fim, ou quando for pedida uma peça, pauta ou pacote para uma marca que tem config em config/<cliente>/. Responda sempre em português.
user-invocable: true
---

# Motor de conteúdo

Produz conteúdo para **qualquer cliente**, em **qualquer harness** (Claude Code, Codex, Grok,
Antigravity). Nada específico de marca mora aqui: o específico vive na pasta de config do cliente
ativo, `config/<cliente>/` na raiz do repositório (ou a pasta definida pela variável de ambiente
`MOTOR_CONFIG_DIR`). Onde este motor fala de cor, fonte, CTA, registro, porta-voz, número ou
ferramenta de marca, vale o que a config do cliente ativo definir. Cliente cuja config não define o
item não pega emprestado de outro cliente.

**Caminhos das ferramentas.** Nos comandos abaixo, `<pasta-da-skill>` é o diretório-base desta skill
(`skills/produzir-conteudo`), que o Claude Code informa ao carregar a skill. As ferramentas ficam em
`<pasta-da-skill>/ferramentas/`.

**Skills externas são opcionais.** `fact-checker`, `humanizer`, `arsenal`, `segunda-opiniao`,
`last30days` e as demais citadas aqui só valem se estiverem instaladas. Sem elas, cada papel roda à
mão, e as tabelas dizem o que fazer.

**Você é a linha de montagem inteira, não o fiscal dela.** Pauta, pesquisa, texto, revisão que
reescreve, arte, render e entrega. As verificações existem para proteger o trabalho, não para
substituí-lo. Um fluxo que só produz portão e auditoria entrega pouco, e o pouco vem cru.

**Leia junto:** `referencias/linha-de-montagem.md`. É o mapa de quem trabalha em cada estação e
qual skill roda ali.

## Contrato de operação (autônomo é o padrão)

**Rode ponta a ponta e mostre a quem aprova só o pacote final.** Quem aprova valida o resultado, não as etapas.

> **Regra de operação:** autonomia total na execução, **aval de quem aprova no resultado**, com
> supervisão. Ou seja, não pedir permissão para trabalhar, mas nada é dado como aprovado sem quem
> aprova ver. E o trabalho tem que ser auditável: cada estação deixa arquivo, para a supervisão ser
> possível sem acompanhar o processo ao vivo.

- Colher **tema** e **objetivo** uma vez, na estação 0.5. É a única pergunta de entrada.
- Rodar as estações 1 a 8 sem checkpoint. O loop de revisão roda **por dentro**.
- Entregar o material de aprovação pronto e **abrir o arquivo**.

**Pare e avise quem aprova só nestes quatro casos:**

| Situação | Por quê |
|---|---|
| O portão de pauta **reprovou duas vezes** no mesmo tema | O ângulo não fecha e insistir queima o pacote inteiro |
| A checagem achou **dado que não bate com a fonte**, citação sem transcrição conferida, ou alegação sobre o que o cliente fez sem confirmação | Autonomia não deixa dado errado ir ao ar |
| O trabalho bate com um item de **"⛔ Não repetir"** (do motor ou do Diário do cliente) | Já custou caro uma vez |
| A **premissa do briefing caiu na verificação** ("ninguém fala disso", "isso é novo", "mudou agora") | A peça inteira nasce daquela frase, e a formulação é de quem aprova. Detalhe na estação 0.5 |

Fora disso, não pergunte: decida, registre a decisão em uma linha e siga.

## A regra que sustenta o resto

**Verificação que não produz arquivo não aconteceu.**

Não existe "rodei o revisor e deu 9,5". Existe a saída do comando, colada, ou a etapa não foi
feita. Em 29/07/2026 um fluxo se declarou concluído com média 9,4 tendo entregue um PDF com 7
placeholders e nenhum card, zero fontes com link, e um portão que respondeu "não saiu algo igual"
sobre um tema com 47 peças no acervo.

Ferramentas em Python puro, sem dependência de harness, em `<pasta-da-skill>/ferramentas/`:

| Comando | Responde |
|---|---|
| `busca_acervo.py "<tema>" --cliente <c>` | já saiu algo igual? |
| `check_voz.py <arquivo> --cliente <c>` | o texto viola a voz da marca? |
| `check_entrega.py "<pasta>" --cliente <c>` | isso está pronto de verdade? |

**O que essas ferramentas não fazem:** escrever melhor. `check_voz.py` é uma varredura mecânica,
uma rede embaixo do trapézio. Quem reescreve é o revisor da estação 5.

## O processo custa o que a peça vale

Nível 1 com o ritual de nível 3 é o que faz o fluxo travar antes da primeira linha de texto.
O nível sai de `referencias/niveis-de-esforco.md` e **decide quantos arquivos existem**:

| Artefato | Nível 1 · Rápido | Nível 2 · Padrão | Nível 3 · Completo |
|---|---|---|---|
| Portão de pauta | 7 linhas **no topo do `conteudo.md`** | `portao.md` | `portao.md` + teste adversarial |
| Estratégia (StoryBrand) | 5 linhas no mesmo arquivo | `estrategia.md` | `estrategia.md` |
| Pesquisa | interna | interna + imprensa + `last30days`, se instalada | fonte primária + demanda de busca |
| Revisão | estilo + marca | estilo, marca, dados, persuasão | os cinco revisores + segunda opinião |
| Parecer do editor | inline, no fim do arquivo | `revisao.md` | `revisao.md` |
| `check_entrega.py` | sim | sim | sim |

**O portão nunca desaparece, só muda de tamanho.** Ele custa dois minutos e já salvou pacote
inteiro. O que se corta no nível 1 é o número de arquivos, nunca a pergunta.

## Estação 0 · Contexto

**0a · Ingestão, quando chegar material.** Classificar o que chegou em `fonte`, `material
bruto`, `rascunho`, `briefing` ou `referência`, porque isso decide o caminho da pauta. ⚠️ Referência
de concorrente pode ser **adversarial**: quando o ganho de quem fala depende da perda de quem o
cliente atende, o material não é reproduzido nem descartado, é invertido a
favor do cliente pelo enquadramento de **assimetria de informação**, nunca de ameaça. Detalhe em
`referencias/ingestao.md`; exemplos da casa, quando houver, no `perfil.md` do cliente.

1. **"⛔ Não repetir", lido em dois lugares:** `referencias/nao-repetir-motor.md` (lições do motor, valem para todo cliente) e a seção "⛔ Não repetir" do Diário de Bordo do cliente (`paths.json`, campo `diario`).
2. **Config do cliente** (a pasta do registro): `perfil`, `voz`, `formatos`, `provas`,
   `marca`, `biblioteca`, `paths.json`. Sem config, não há produção.
3. **Tópico do tema** na biblioteca do cliente (`biblioteca.md` ou a pasta que a config indicar).
   Trinta segundos que já evitaram opinar errado sobre uma marca que tinha seis e-books do assunto.
4. **Registro da demanda**, criado agora, quando o `perfil.md` do cliente tiver a seção "Registro"
   (onde registrar: planilha, quadro ou pasta, e quais campos). Registro criado na entrega não tem
   histórico: ninguém sabe quando a demanda chegou nem quanto tempo levou. Cliente sem essa seção
   pula este item.

## Estação 0.5 · Briefing

**Tema** e **objetivo**. Se já vieram os dois, seguir direto. Não perguntar formato: ele sai de
`formatos.md`. Não abrir `superpowers:brainstorming` aqui, porque este é o briefing.

**O briefing traz intuição de mercado, e intuição não é fato verificado.** Quando o tema vier com
"ninguém está falando disso", "isso é novo", "ninguém percebeu" ou "mudou agora", isso é
**afirmação factual** e entra na pergunta 4 do portão como qualquer outra. Verificar antes da
primeira linha e, **se a premissa cair, voltar a quem aprova com o resultado** antes de escrever. Esta é a
quarta exceção do contrato de operação: a peça inteira nasce daquela frase, e reformular por conta
própria entrega outra peça. Premissa que se confirma não para nada, só se registra em uma linha.

Em 07/08/2026 um briefing trouxe as duas coisas erradas de uma vez: "ninguém fala disso" sobre um
tema com cinco publicações no mês e um curso pago rodando, e uma mudança apresentada como novidade
da reforma que já era regra desde 2006. Os dois teriam ido ao ar. A intuição de fundo estava certa e
só sobreviveu porque a checagem achou o recorte que ninguém tinha ocupado.

Isso não é desconfiar do cliente. Ele traz o faro, e a verificação é a parte do trabalho que é sua.

## Estação 1 · Portão de pauta

Seis perguntas antes de existir texto. Rode o comando e **cole a saída inteira**:

```bash
python "<pasta-da-skill>/ferramentas/busca_acervo.py" "<tema|sinônimo|sigla>" --cliente <cliente>
```

Sem essa saída colada, a pergunta 4 foi respondida de memória. Perguntas e critério de reprovação
em `referencias/portao-de-pauta.md`.

**Reprovou: troca o ângulo e roda de novo, sozinho. Não escreve, não pergunta.** Só na segunda
reprovação do mesmo tema quem aprova entra.

⚠️ Território com muitas peças **não reprova sozinho**, mas exige o ângulo novo declarado por
escrito. "É um recorte diferente" sem dizer qual recorte é carimbo.

⚠️ **A pergunta 6 é sobre a casa, não sobre o texto: o CTA promete algo que ela consegue entregar?**
Prateleira, em desenho, ou não existe. Serviço em desenho vira CTA de conversa, nunca de entregável
nomeado. As outras cinco perguntas olham para a pauta e deixam passar promessa sem lastro, e o
revisor de marca **premia** o CTA específico, que é exatamente o defeito. O `check_entrega.py`
reprova a pasta sem a linha `ENTREGA?` no `portao.md`.

## Estação 2 · Estratégia

Os cinco campos de StoryBrand do `perfil.md`: herói, problema, guia, plano, CTA. **Aqui, não na
revisão.** Junto deles, o **plano de design** das peças: o que vai em cada card, imagem-conceito,
hierarquia, tema do brand book. A arte parte do briefing, não espera o texto ficar pronto.

## Estação 2b · Teste da tese, só no nível 3

**Antes de escrever, não depois.** A tese fechada na estação 2 vai para uma segunda opinião (skill
`segunda-opiniao`, se instalada; senão, outro modelo ou subagente), em cinco linhas, no modo
falsificação: entregue o argumento como se fosse de terceiro e peça a
evidência que o contradiz mais o teste que o derrubaria. Modelos de outras empresas leem sem o viés
de quem escreveu o recorte.

**Por que aqui.** Derrubar tese custa uma rodada. Derrubar tese **depois** da escrita, do loop de
revisão e do editor custa o pacote inteiro, e a peça volta para esta mesma estação de qualquer
jeito. O teste caro tem que vir enquanto trocar de ângulo ainda é de graça.

**Não peça reescrita a eles.** A própria skill veta: as regras de voz do cliente não vão no
briefing e o texto volta fora do padrão. Eles atacam o argumento, ninguém mais.

| Retorno | Ação |
|---|---|
| Acharam furo real | Volta para a estação 1. Ângulo novo, portão de novo |
| Divergem entre si | A peça se apoia em algo discutível. Explicitar isso no texto costuma fortalecer |
| Todos dizem que está de pé | Registrar e seguir. Convergência mede o briefing, não o mundo |
| Afirmaram fato verificável | Checar de forma independente antes de mexer. Achado de agente é pista, não fonte |

No nível 3 isso convive com a defesa 3 do portão (agente adversarial em pauta de gancho externo).
Não são a mesma coisa: aquele dá lente diferente, este dá **treinamento** diferente. Rodando os
dois, o adversarial vem no portão e a `segunda-opiniao` aqui, com a tese já formada.

## Estação 3 · Pesquisa, no nível certo

| Nível | Pesquisa | Serve para |
|---|---|---|
| **1 · Rápido** | Só interna: acervo, tópicos, provas | Post de conversa, teste de ângulo, institucional |
| **2 · Padrão** | Interna + imprensa dos últimos 30 dias + escuta social (`last30days`, se instalada; senão, busca manual em redes e fóruns) | A maioria das peças |
| **3 · Completo** | Fontes primárias, demanda de busca, tudo | Artigo técnico, release, dado inédito |

Detalhe e regras de dado em `referencias/niveis-de-esforco.md`. O mapa de veículos do cliente está
no `perfil.md`, seção "Skills e ativos que o motor pluga aqui"; o radar genérico de fontes está em
`skills/vamos-trabalhar/referencias/fontes-confiaveis.md`.

**Todo dado entra com link.** Não "conferido": o link, no texto.

**A `last30days` traz conversa, não número.** Ela mostra como o mercado fala do assunto agora, e
isso vira hook, título e objeção. Engajamento de post não é estatística e comentário de rede não é
fonte primária: o número continua saindo daqui com link.

## Estação 3d · Demanda de busca, só no nível 3

**O que o mercado digita quando procura isso.** A escuta social (3c) mostra como as pessoas falam
entre si; esta mostra o que elas perguntam sozinhas, na barra de busca, sem plateia. São coisas
diferentes e a segunda costuma ser mais honesta.

Feita à mão, no navegador, sem API:

- **Google Trends:** comparar o termo-raiz e uma variação (Brasil, últimos 12 meses). Vale o que
  aparece em alta, não o volume absoluto.
- **Google, "pessoas também perguntam" e autocomplete:** anotar as perguntas reais.
- Cliente que tiver outra fonte de demanda de busca declara no `perfil.md`.

| Saída | Onde entra |
|---|---|
| Pergunta com volume que ninguém respondeu | vira o H2 do artigo, ou a pauta inteira |
| Termo que o mercado usa de verdade | vira título e palavra-âncora, no lugar do termo técnico |
| Termo em alta no Trends | pauta quente: sobe a prioridade, não o nível de certeza |

**Ela dá recorte, não dado.** Volume de busca é sinal de interesse, não estatística de mercado, e
não entra no texto como número. O número continua saindo da estação 3 com link.

## Estação 4 · Escrever

Voz e proibições em `voz.md` do cliente. Escreva o conteúdo-base inteiro de uma vez, mais a copy de
cada canal escolhido. Hook na primeira linha, parágrafo curto, CTA que gera ação.

A skill de voz e a de posicionamento são as declaradas pelo cliente no `perfil.md`. Reforços
opcionais, se instalados: uma skill de SEO e GEO no artigo (`claude-seo:seo-geo`), para passagens
citáveis por IA; e um agente narrador quando a peça precisar de estrutura narrativa. Sem eles, no
artigo, conferir à mão que cada seção tem uma passagem de duas a três frases que responde uma
pergunta sozinha.

**Regras de forma por formato** em `referencias/formatos/`: um arquivo por formato (artigo de blog,
artigo de LinkedIn, carrossel/documento, teleprompter, estudo de imprensa, case, post único, story
avulso, sequência de stories, repurpose de acervo), cada um com estrutura, tamanho e CTA próprios.
O `modulos-de-saida.md` diz **qual** formato escolher; estes dizem **como** fazer cada um.

**O júri de cinco versões saiu do fluxo em 07/08/2026.** Cinco redações da mesma pauta mais um juiz
por critério pagam cinco vezes a etapa que menos falha aqui: as peças descartadas deste motor não
morreram por execução, morreram por tese, e tiraram 8,5 no caminho. O método continua descrito em
`referencias/escrita-juri.md` para quem quiser rodar à mão, fora do motor.

## Estação 5 · Revisão em loop, depois editor

**Nada de imagem antes daqui.** Renderizar peça que vai ser reescrita é o desperdício mais caro do
fluxo.

Dois blocos, nesta ordem, detalhados em `referencias/revisao.md`. O teste da tese já rodou lá atrás,
na estação 2b:

1. **REVISORES (acham erro e reescrevem).** Dados, estilo, design, marca e persuasão. A skill de
   cada papel está em `referencias/revisao.md`, com o que fazer à mão quando ela não estiver
   instalada. Cada um dá **nota de 0 a 10** e lista de correções. **Loop até todas ≥ 8**, teto de 4
   rodadas. Rode em paralelo, em mensagens separadas (skill de agentes em paralelo, se instalada;
   senão, subagentes separados): revisor que lê o parecer do vizinho converge com ele e a nota perde
   valor.
2. **EDITOR ESTRATÉGICO (propõe melhor).** Papel separado, rubrica em
   `referencias/editor-estrategico.md`. Ele **escreve a alternativa**, não a descreve.

Rede mecânica, por cima do revisor de estilo e nunca no lugar dele:

```bash
python "<pasta-da-skill>/ferramentas/check_voz.py" conteudo.md --cliente <cliente>
```

**Aplicar a lista inteira de uma vez.** Aplicar 8 de 12 correções garante regressão: as que ficam
voltam na rodada seguinte e a nota cai. Já aconteceu.

### Se estourar o teto de rodadas: repensar o conteúdo, não entregar

**Regra de operação.** Nota que não sobe depois de 4 rodadas não é problema de redação, é
sinal de que a peça está errada mais atrás. Continuar polindo é o erro que o Diário já registrou
duas vezes: peça que tirou 8, 8,5 e 8,5 em três rodadas e foi descartada porque a tese era o
consenso mais repetido do assunto. Os revisores medem execução, não pertinência.

**O que fazer, nesta ordem:**

1. **Voltar à estação 1 e 2** com o que os revisores apontaram. Reabrir o ângulo e a tese, não o
   texto. Perguntar de novo: **por que alguém discordaria disso?** e **isso alcança quem vai ler?**
2. **Reescrever a partir do ângulo novo** e rodar o loop uma vez.
3. **Só então chamar quem aprova**, se ainda não bater. Isso é a exceção 1 do contrato de operação, que é
   o portão reprovando duas vezes o mesmo tema.

**Nunca entregar peça abaixo da nota com a lista do que falta.** Entregar assim transfere a quem aprova a
decisão que o fluxo existe para tomar.

**Bloco de decisão do editor, uma linha por elemento**, `aceito` ou `recusado` com o motivo. Sem
ele, a peça não fecha.

## Estação 6 · Imagem

**Roda sempre que a peça tem imagem, em qualquer nível.** Card, carrossel, story e capa passam por
aqui e pelo revisor 5c mesmo no nível 1. O nível de esforço mede pesquisa e revisão de texto, não
decide se a peça é visual: quem decide isso é o formato escolhido em `formatos.md`.

Ordem de prioridade no `marca.md` do cliente. Regra que vale em qualquer marca: **não gerar do zero
se já existe**, e **abrir toda imagem antes de usar**, porque nome de arquivo não descreve conteúdo.

## Estação 7 · Produção e entrega

Saídas escolhidas por desempenho medido em `formatos.md`, não impostas. Catálogo em
`referencias/modulos-de-saida.md`. **Cada saída vem com a razão em uma linha, citando o número.**

**Peça visual precisa ser renderizada, não descrita.** Roteiro de card em texto não é card.

Ordem de produção, entregáveis e pipeline gráfico em `referencias/producao-e-entrega.md`.

## Estação 8 · Fechar

O que abriu na estação 0 fecha aqui, em três registros:

| Onde | O que | Quando |
|---|---|---|
| **Registro do cliente** | o que a seção "Registro" do `perfil.md` mandar (status, colunas, link da nota). Cliente sem a seção pula | agora, junto da entrega |
| **Pasta de notas do cliente** | nota da peça no lugar, no formato e com os campos que o `perfil.md` ou a camada do cliente definir | **proposta agora, gravada com o "pode" de quem aprova** |
| **Diário de Bordo** | entrada no Log do arquivo local apontado no `paths.json` (campo `diario`), modelo em `referencias/producao-e-entrega.md` | sempre, sem pedir |

**A nota de acervo é a única coisa do fechamento que espera resposta.** Regra fixa: nada entra no
acervo do cliente sem quem aprova autorizar. Isso não quebra o contrato autônomo, porque a proposta vai
junto com o pacote, na mesma mensagem em que quem aprova avalia o resultado. Entregar sem propor o registro
é que está errado.

Classificar na hora custa 30 segundos; em lote depois custa um dia. Reconciliação em lote, quando o
cliente tiver, é outra operação, declarada no `perfil.md` dele, que roda quando quem aprova pede e mostra
o diff antes de gravar.

Antes de anunciar:

```bash
python "<pasta-da-skill>/ferramentas/check_entrega.py" "<pasta do trabalho>" --cliente <cliente>
```

**Exit code 1 significa que não está pronto.** Corrigir e rodar de novo. Depois: **abrir a saída**
e **escrever no Log do Diário de Bordo** (modelo em `referencias/producao-e-entrega.md`).

## Estação 9 · Reapurar o que decide o formato

O motor escolhe formato "por desempenho medido em `formatos.md`", e **nenhuma estação alimentava
esse arquivo.** Sem isto, em três meses o fluxo cita o número de julho como se fosse de hoje, e o
ranking vira profecia que se cumpre sozinha: só se publica o que já mediu bem, e a base nunca
contradiz a si mesma.

**Não roda por peça.** Roda por gatilho, em lote:

| Gatilho | O que fazer |
|---|---|
| A data de apuração do `formatos.md` passou de **60 dias** | Avisar quem aprova na entrega, em uma linha, e propor a reapuração |
| Passou de **90 dias** | O número não é mais citável como razão de escolha. Escolher formato pelo dado velho e **declarar** que ele está velho |
| Reapuração autorizada | Puxar a métrica da fonte do cliente, recalcular taxa e volume, **reescrever o `formatos.md` inteiro** com a nova data e guardar o ranking anterior no arquivo |

**Ao reapurar, comparar com o ranking antigo e escrever o que mudou.** Formato que caiu de posição é
informação melhor que formato que subiu: pode ser saturação do canal, não erro de execução.

⚠️ **Ranking construído sobre poucas peças é frágil.** Antes de tratar uma diferença como real,
olhar quantos posts sustentam cada linha. Um formato com 16 peças e outro com 123 não se comparam
com a mesma confiança, e a decisão do motor deve dizer isso quando for o caso.

## Bandeiras vermelhas

| Pensamento | Realidade |
|---|---|
| "Já sei que não saiu nada igual" | O acervo do cliente pode ter anos de peças. Rode o comando. |
| "A tese é fraca mas o texto fica bom" | Texto bom com tese fraca é o descarte de 8,5. |
| "O `check_voz` passou, o texto está revisado" | Ele acha travessão, não acha texto morno. Rode o revisor. |
| "Dou a nota e sigo" | Nota sem parecer é opinião sobre trabalho não feito. |
| "Vou confirmar com quem aprova antes de seguir" | O contrato é autônomo. Só as quatro exceções param. |
| "O roteiro do card está pronto" | Roteiro não é card. Sem PNG, o PDF sai com placeholder. |
| "Depois eu confiro se tem prova da casa" | Sem prova própria, qualquer concorrente assina a peça. |
| "Aplico as correções principais" | Correção pela metade faz a nota cair na rodada seguinte. |
| "O `last30days` achou esse número" | Ele mostra conversa, não estatística. Número vem da estação 3, com link. |
| "Dou a nota de persuasão direto" | A rubrica de persuasão (`arsenal`, Módulo 1, ou a tabela manual) exige a tabela preenchida antes do número, e a página conferida. |
| "Os três modelos aprovaram a tese" | Eles leram o recorte que você escreveu. Convergência mede o briefing, não o mundo. |
| "Está pronto, vou avisar" | Rode o `check_entrega.py`. Ele já reprovou uma entrega que se dizia 9,4. |
