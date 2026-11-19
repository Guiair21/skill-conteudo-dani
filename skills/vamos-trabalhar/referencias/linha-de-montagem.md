# Linha de montagem, camada do cliente (modelo)

**Este arquivo não define a ordem das estações.** Quem define é a genérica, em
`referencias/linha-de-montagem.md` da skill `produzir-conteudo`. Aqui fica só **o que o cliente
pluga em cada cadeira**: a ferramenta da casa e o portão de qualidade que essa marca cobra. Copie
este modelo, troque `<cliente>` e preencha a coluna da direita com o que a config do cliente definir.

Se a numeração daqui divergir da genérica, a genérica ganha. Os postos são os mesmos; por que cada
um existe separado do vizinho está lá, e repetir aqui só cria duas versões da mesma coisa.

## Contrato de operação

Padrão: **rodo ponta a ponta e quem aprova vê o pacote final**, não as etapas. Tema e objetivo são
colhidos uma vez, na estação 0.5.

Param o fluxo e chamam quem aprova, só isto:

1. O portão de pauta reprovou **duas vezes** o mesmo tema.
2. A checagem achou dado que não bate com a fonte, citação sem transcrição conferida, ou alegação
   sobre o que o cliente fez sem confirmação. Regras que valem sempre: fonte primária com link,
   citação só com transcrição verificada, não inventar o que o cliente fez.
3. O trabalho bate com um item de "⛔ Não repetir" do Diário.
4. A premissa do briefing caiu na verificação ("ninguém fala disso", "isso é novo", "mudou agora").
   A peça inteira nasce daquela frase, e reformular por conta própria entrega outra peça.

A nota de registro do acervo, na estação 8, é proposta junto com o pacote e gravada só com o "pode"
de quem aprova. Isso não é checkpoint no meio: vai na mesma mensagem da entrega.

## O que o cliente pluga

**Só as estações que têm ferramenta ou portão próprios estão aqui.** As que não aparecem
(0.5, 2+, 2b, 3b, 4+, 5a, 5b, 5f, 9 e o loop) rodam exatamente como na genérica.

| # | Posto | Ferramenta da casa | Portão do cliente |
|---|---|---|---|
| 0 | **Secretaria de Redação** | registro da demanda que a config do cliente definir (planilha, quadro ou pasta) | demanda registrada na entrada, antes de qualquer trabalho |
| 1 | **Portão de Pauta** | `python "<pasta-da-skill>/ferramentas/busca_acervo.py" --cliente <cliente>` | saída do comando colada. Território com muitas peças exige ângulo novo declarado por escrito |
| 2 | **Estratégia de Conteúdo** | `perfil.md` (StoryBrand) e, se estiver instalada, a skill de posicionamento declarada nele | cliente atendido é o herói, a marca é o guia. Três ângulos não explorados |
| 3 | **Reportagem de Dados** | `referencias/fontes-confiaveis.md` (veículos por linha de serviço) | dado duro só da Camada 1, com link. Cuidado com agregados que escondem o recorte (ex.: "PME" dominado por MEI) |
| 3c | **Escuta Social** | `last30days`, se instalada; senão, busca manual nas redes e fóruns | traz o termo que o mercado usa, nunca número nem o tom da rede |
| 3d | **Inteligência de Busca** | Google Trends e "pessoas também perguntam", à mão no navegador | o que o mercado digita sozinho. No Trends vale o que está em alta, não o volume absoluto |
| 4 | **Redação** | a skill de voz declarada no `perfil.md` do cliente | tom definido em `voz.md` |
| 5c | **Direção de Arte** | `marca.md` do cliente | regras de peça do cliente, grid e hierarquia |
| 5d | **Guarda da Marca** | a skill de posicionamento declarada no `perfil.md` | herói e guia certos, coesão entre as peças, tom |
| 5e | **Direção de Persuasão** | `arsenal`, se instalada; senão, rubrica manual de persuasão (gatilho com fato, promessa com lastro) | rubrica preenchida antes da nota. Opina dentro da voz, nunca por cima dela |
| 6 | **Pesquisa de Imagem** | banco curado, marca, banco gratuito, geração | regras de imagem do `marca.md` |
| 7 | **Produção Gráfica** | template de carrossel HTML e `templates/gen_pdf_aprovacao_template.py` | artigo antes dos cards no PDF, regras de CTA do `marca.md` |
| 8 | **Secretaria de Redação** | `check_entrega.py`, registro da demanda, Diário (arquivo local apontado no `paths.json`, campo `diario`) | Log sempre. Nota de acervo gravada só com o "pode" |

## Quantas estações rodam

O nível de esforço decide, e a régua é a do motor (`niveis-de-esforco.md`):

| Nível | Estações |
|---|---|
| **1 · Rápido** | 0, 0.5, 1, 2, 3b, 4, 5b, 5d, 5f, 7, 8 |
| **2 · Padrão** | as do nível 1 mais 3, 3c, 5a e 5e |
| **3 · Completo** | todas, incluindo 2+, 2b, 3d e 4+ |

A demanda de busca (3d) é o que separa o nível 3 do nível 2 na pesquisa, ao lado da fonte primária.

**Imagem foge dessa tabela.** Carrossel, card, story e capa passam por 6 e 5c em qualquer nível,
inclusive no 1.

**Nunca saem:** 0, 1, 5f e 8.

## O que este mapa não decide

Formato e pacote. Isso sai de `formatos.md` do cliente, por desempenho medido, e do catálogo em
`modulos-de-saida.md` do motor. **Não existe trio fixo obrigatório:** quando um acervo foi medido,
artigo mais carrossel mais story era a pior combinação, formato por formato.
