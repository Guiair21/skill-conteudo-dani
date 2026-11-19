# Linha de montagem

O mapa da máquina: **quem senta em cada estação e qual ferramenta roda ali**. Cada estação é um
posto de redação, nomeado pela função que exerce.

Este arquivo é genérico. Onde a coluna diz "do cliente", a ferramenta certa está na config do
cliente ativo (`config/<cliente>/`) e na camada dele.

## Os postos

| # | Posto | Ferramenta | Portão da estação |
|---|---|---|---|
| 0 | **Secretaria de Redação** (abre) | Diário de Bordo do cliente (`paths.json`, `diario`), registro da demanda do `perfil.md` (se houver), tópico na biblioteca do cliente | ler "⛔ Não repetir" e abrir o registro antes de começar, quando o cliente tiver |
| 0.5 | **Coordenação de Pauta** | tema + objetivo | única pergunta de entrada |
| 1 | **Portão de Pauta** | `busca_acervo.py` + `portao-de-pauta.md` | saída do comando colada, não memória. Seis perguntas |
| 2 | **Estratégia de Conteúdo** | `perfil.md` do cliente (StoryBrand) | herói, problema, guia, plano, CTA antes do texto |
| 2+ | **Conselho Editorial** | agente de conselho editorial, se houver | só campanha ou mês: pressiona a tese antes da copy |
| 2b | **Banca de Contraprova** | `segunda-opiniao`, se instalada; senão, outro modelo ou subagente em modo falsificação | só nível 3. Ataca a tese **antes** de existir texto. Não pede reescrita |
| 3 | **Reportagem de Dados** | fontes do cliente, WebSearch, skill de cluster de SEO se instalada | dado duro só de fonte primária, com link |
| 3b | **Arquivo** | acervo publicado do cliente | reaproveitar sem forçar conexão |
| 3c | **Escuta Social** (30 dias) | `last30days`, se instalada; senão, busca manual em redes e fóruns | traz conversa e ângulo, nunca número. Do nível 2 para cima |
| 3d | **Inteligência de Busca** | Google Trends e "pessoas também perguntam", à mão | o que o mercado digita sozinho. Recorte e termo, nunca dado. Só nível 3 |
| 4 | **Redação** | skill de voz do cliente, `referencias/formatos/` | reforço: agente narrador, se houver |
| 4+ | **Descoberta por IA** | `claude-seo:seo-geo`, se instalada | só no artigo: passagens citáveis |
| 5a | **Checagem** | `fact-checker`, se instalada | fonte primária datada com link; citação com transcrição |
| 5b | **Copidesque** | `humanizer`, se instalada | sem travessão, trinca, falso contraste, robô |
| 5c | **Direção de Arte** | agente de auditoria de design, se houver, + `marca.md` | grid, hierarquia, regras de peça do cliente |
| 5d | **Guarda da Marca** | posicionamento do cliente (skill declarada no `perfil.md`) | herói e guia certos, coesão, tom |
| 5e | **Direção de Persuasão** | `arsenal`, Módulo 1, se instalada | nota pela rubrica preenchida, princípio citado pelo código. Do nível 2 para cima |
| — | **Loop** | repetir 5a a 5e aplicando **todas** as correções | parar quando as notas ≥ 8 (teto: 4 rodadas) |
| 5f | **Edição-Chefe** | `editor-estrategico.md` | escreve a alternativa; decisão registrada |
| 6 | **Pesquisa de Imagem** | banco curado → marca → banco pago → gerar | regras de imagem do `marca.md` |
| 7 | **Produção Gráfica** | template do cliente + gerador do PDF de aprovação do cliente (`perfil.md`, estação 7) | reforços: skills de slides e `pptx`, se instaladas |
| 8 | **Secretaria de Redação** (fecha) | `check_entrega.py`, registro do cliente (`perfil.md`), pasta de notas, Diário | Log sempre; nota de acervo só com o "pode" de quem aprova |
| 9 | **Inteligência de Performance** | métrica do cliente → `formatos.md` | por gatilho, em lote: apuração com mais de 60 dias avisa, com mais de 90 não é mais citável |

## Por que os postos são separados

Não é organograma decorativo. **Cada posto existe porque acumular a função com o vizinho já
estragou peça:**

- **Portão de Pauta separado da Redação.** Quem vai escrever já quer escrever, e responde "passou"
  para chegar no texto. O portão carimbado é pior que portão nenhum.
- **Checagem separada da Reportagem.** Quem levantou o dado defende o dado.
- **Copidesque separado da Redação.** Autor não enxerga o próprio vício de escrita.
- **Direção de Arte e Guarda da Marca separadas.** Uma olha grid e hierarquia, a outra olha se a
  peça ainda é daquela marca. Peça bonita fora da marca passa quando é o mesmo olho.
- **Edição-Chefe depois dos revisores, não junto.** Revisor acha erro; editor pergunta se o que
  está lá é o teto. Misturar os dois entrega texto correto e morno.
- **Banca de Contraprova antes da Redação.** Tese derrubada depois do texto custa o pacote inteiro.

## Quantas estações rodam

Não são todas, sempre. **O nível de esforço decide** (`niveis-de-esforco.md`):

| Nível | Estações |
|---|---|
| **1 · Rápido** | 0, 0.5, 1, 2, 3b, 4, 5b, 5d, 5f, 7, 8 |
| **2 · Padrão** | as do nível 1 mais 3, 3c, 5a e 5e |
| **3 · Completo** | todas, incluindo 2+, 2b, 3d e 4+ |

**Imagem não é função do nível, é função do formato.** As estações **6** e **5c** entram sempre que
a peça tem card, carrossel, story ou capa, inclusive no nível 1. O nível decide profundidade de
pesquisa e de revisão de texto, nunca se a peça vai ter imagem. Um carrossel de nível 1 sem a
estação 6 chega na produção sem imagem definida, e a estação 7 exige que ela já esteja escolhida.

**As que nunca saem:** 0 (Diário), 1 (portão), 5f (editor) e 8 (fechamento). Uma peça de dois
parágrafos ainda passa pelo portão, porque o que o portão barra é a pauta ruim, e pauta ruim custa
igual em qualquer tamanho.

## O que este mapa não decide

Formato e pacote. Isso sai de `formatos.md` do cliente, por desempenho medido, e do catálogo em
`modulos-de-saida.md`. Não existe pacote fixo obrigatório: na primeira conta em que o acervo foi
medido, o trio fixo de artigo, carrossel e story era a pior combinação, formato por formato.
