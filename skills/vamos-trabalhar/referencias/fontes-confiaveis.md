# Radar de fontes (Passo 1 da skill "vamos-trabalhar")

## Por que este arquivo existe

Rodar `last30days` sobre Reddit, HackerNews e GitHub é radar de tecnologia. Para tema de gestão
empresarial brasileira devolve ruído: uma busca sobre reforma tributária já trouxe console portátil
e isenção fiscal de Ohio. A pesquisa deve sair de veículos confiáveis, mapeados por linha de
serviço, em 3 camadas que respondem perguntas diferentes.

| Camada | Pergunta que responde | Obrigatória? |
|---|---|---|
| 1 · Dado duro | O que é verdade e está atual? | sim |
| 2 · Pauta | O que está sendo discutido agora? | sim |
| 3 · Demanda | O que o público digita quando está com o problema? | sim, à mão |

Regra que atravessa as três: **número sai da Camada 1**. Camada 2 dá ângulo e Camada 3 dá
vocabulário. Nenhuma das duas vira dado herói de card. A casa (o que o cliente já publicou) se
consulta pelo `busca_acervo.py`, no Passo 2.

---

## Camada 1 — Dado duro (fonte primária, edição mais recente)

Antes de usar qualquer indicador mensal, checar na sala de imprensa do instituto
se já saiu edição nova. "Verificado na fonte primária" não é o mesmo que "está
atual", e o revisor de dados cobra as duas coisas.

### Reestruturação (turnaround, RJ/extrajudicial, NPL)
- **Serasa Experian**, sala de imprensa: indicador mensal de recuperações
  judiciais e falências, e inadimplência PJ.
- **Observatório da Insolvência (ABJ)**: deságio, tempo de processo, taxa de
  aprovação de plano. É jurimetria, não opinião.
- **CNJ**: estatística processual.
- **Planalto**: Lei 11.101/2005 lida no artigo, nunca por resumo.

### Performance (financeiro, controladoria/FP&A, BI, comercial)
- **Banco Central**: API do SGS
  (`api.bcb.gov.br/dados/serie/bcdata.sgs.NNNNN/dados?formato=json`) e as
  Estatísticas Monetárias e de Crédito. Nunca sumarizar PDF do BCB: baixar e extrair.
- **IBGE**: Demografia das Empresas, Cempre, IPCA, PIB.
- **Sebrae**: Sobrevivência das Empresas (é a única série pública que isola porte
  de forma útil) e Datasebrae.
- **Mapa de Empresas (MDIC)**: abertura e fechamento de CNPJ, quadrimestral.
- **FGV/IBRE**: sondagens empresariais e índices de confiança.
- **CNI**: sondagem industrial, indicadores de custo.

### Recebíveis, FIDC e crédito
- **Anbima**: boletim de FIDC e de mercado de capitais (assina emissões).
- **CVM**: Resolução 175 e normativos de fundos.
- **Banco Central**: Resolução BCB 339/2023, convenção da duplicata escritural,
  séries SGS de custo de crédito PJ.
- **Registradoras** (CERC, B3, Núclea): estoque e volume registrado.

### Tributário e reforma
- **Planalto**: LC 214/2025 e LC 227/2026, texto compilado, lido por artigo.
- **Receita Federal** e **CGIBS**: cronograma e atos oficiais.

### Fontes regionais (quando o ângulo for local)
- Federação da indústria, junta comercial e instituto de pesquisa do estado em questão. Exemplo: no Paraná, Fiep, JucePAR e Ipardes.


---

## Camada 2 — Pauta (o que está no ar)

Serve para achar ângulo e saber o que já saturou. **Não se tira número daqui**,
nem quando a matéria diz "segundo a própria empresa" (já houve "80%
digital" atribuído a uma empresa que não existia no comunicado oficial).

- **Geral e negócios**: Valor Econômico, Exame, NeoFeed, Brazil Journal,
  InfoMoney, Estadão.
- **Jurídico e tributário**: JOTA, Conjur, Migalhas.
- **Mercado de capitais e crédito**: Capital Aberto, Valor Investe, FIDC News.
- **Regional**: o jornal de economia do estado do cliente. Exemplo: Gazeta do Povo, Bem Paraná e Economia PR, no Paraná.

Critério de admissão: o veículo precisa ter **data, autor e link para a fonte
primária**. Blog de SEO brasileiro fica fora, porque consultorias e escolas
reciclam o mesmo relatório antigo como se fosse novo.

---

## Camada 3: demanda de busca (à mão)

Sem API nem ferramenta paga. Três consultas manuais, feitas no navegador:

1. **Google Trends**: comparar o termo-raiz e uma variação, região Brasil, últimos 12 meses.
   Vale o que aparece em alta, não o volume absoluto.
2. **"Pessoas também perguntam"** e o autocomplete do Google: anotar as perguntas reais.
3. **YouTube e fóruns**: ver como a pessoa nomeia o problema nos títulos e comentários.

Buscar o **sintoma curto** ("fluxo de caixa", "renegociar dívida"), nunca a pergunta inteira: frase
longa não tem sugestão de autocomplete e volta vazia. Descartar termo com nome de empresa, clube ou
faculdade: é gente lendo notícia, não demanda de serviço.

Serve para título e H2 do artigo com a palavra que a pessoa usa, hook do card 1 com uma pergunta que
existe de verdade e priorização de pauta. **Volume de busca é fonte secundária**: entra como insumo
de decisão e, se for ao texto, vai nomeado e datado. Nunca como dado herói de card, capa ou story.
Dado herói exige fonte primária e passa pelo `check_fontes.py`.

---

## Quando ainda vale o `last30days`

Só quando o tema tiver componente de tecnologia, IA ou software, que é onde Reddit, HackerNews e
GitHub têm sinal, e só se a skill estiver instalada. Para tema jurídico, tributário ou de gestão
nacional, pular.
