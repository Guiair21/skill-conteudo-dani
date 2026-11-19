# Níveis de esforço

Um eixo só define pesquisa, revisão e entregáveis. **Nem toda peça merece pesquisa completa.**

## Por que existe

O fluxo antigo rodava a mesma pesquisa de quatro camadas em qualquer peça: fonte primária,
imprensa dos últimos 30 dias, demanda de busca e acervo. Um post institucional levava o mesmo
esforço de um artigo com dado inédito.

## Os três níveis

### 1 · Rápido

**Pesquisa:** só interna. Acervo publicado, tópicos do cliente, provas.
**Revisão:** escrita e estratégica. Sem fact-check formal, porque não há dado externo.
**Serve para:** post de conversa, teste de ângulo, institucional, comentário de pauta própria.

Se apareceu número externo, subiu de nível. Não existe "rápido com um dadinho".

### 2 · Padrão

**Pesquisa:** interna, mais imprensa dos últimos 30 dias, mais escuta social pela skill
`last30days` (se instalada; senão, busca manual em redes e fóruns). **As duas servem para ângulo, nunca para número.**
**Revisão:** escrita, estratégica, dados e persuasão.
**Serve para:** a maioria das peças.

Extração de página web em markdown limpo (skill `defuddle`, se instalada), o que corta o custo de
token.

**O que a `last30days` responde e o que ela não responde.** Ela varre Reddit, X, YouTube, TikTok,
Hacker News e web dos últimos 30 dias e mostra **como as pessoas falam do assunto agora**: a
reclamação repetida, a pergunta que ninguém respondeu, o termo que o mercado usa de verdade. Isso
vale ouro para hook, título e objeção. O que sai dela **não entra como dado no texto**: engajamento
de post não é estatística de mercado, e comentário de rede não é fonte primária. Número continua
vindo da estação 3 com link.

Antes de rodar, `last30days doctor` diz quais fontes estão de pé. Rodada com fonte caída é rodada
parcial, e isso se declara em vez de virar conclusão.

**O termo do mercado entra, o tom da rede não.** O que vem de Reddit, X e TikTok mostra como as
pessoas nomeiam o problema, e essa palavra vale muito no título. O ritmo, a gíria e a informalidade
de lá ficam de fora: a peça sai na voz do cliente, definida em `voz.md`, e é o revisor 5b que
segura isso.

### 3 · Completo

**Pesquisa:** fonte primária do dado, na edição mais recente. Demanda de busca (estação 3d,
feita à mão no Google Trends e em "pessoas também perguntam"). Imprensa. Escuta social (`last30days`).
**Teste de tese:** segunda opinião na estação 2b (`segunda-opiniao`, se instalada), antes de escrever.
**Revisão:** os cinco revisores.
**Serve para:** artigo técnico, release, white paper, peça com dado inédito ou número que vai virar
manchete.

## O que o nível não decide

**Imagem.** As estações 6 e 5c entram por formato: peça com card, carrossel, story ou capa passa
por elas em qualquer nível, inclusive no 1. Nível mede pesquisa e revisão de texto. Um carrossel
rápido continua sendo um carrossel, e chegar na produção sem imagem definida trava a estação 7.

## Como escolher

O objetivo sugere, quem aprova confirma em uma linha.

| Objetivo | Nível |
|---|---|
| Testar ângulo, manter frequência | 1 |
| Educar, atrair, gerar conversa | 2 |
| Autoridade, imprensa, ser citado | 3 |

**Na dúvida entre dois, subir.** O custo de pesquisar demais é tempo; o de pesquisar de menos é
dado errado publicado.

## Fact-check acontece na coleta

Não é etapa depois. **O dado nasce verificado ou não entra.**

Quando se separa coleta de verificação, a verificação vira conferência de algo que já está escrito
no texto, e a pressão passa a ser confirmar em vez de checar.

Regras que valem em qualquer nível:

- Todo número com **fonte primária datada e link**
- **Não usar dado de mês antigo quando existe mês novo publicado.** "Está verificado" não é o
  mesmo que "está atual"
- **Não afirmar recorde que a fonte não afirma.** Testar o máximo da série inteira antes de
  escrever "recorde" ou "maior da história"
- **Não usar sumarizador em PDF de dado.** Baixar e extrair. Um resumo de PDF do BCB já devolveu
  9,63% onde o texto dizia 25,3%
- **Testar a escala de campo de taxa vindo de API.** Dividir a métrica bruta pela base de um
  registro e comparar. Divergência por fator de 100 significa fração, não porcentagem
- **Achado de agente é pista, não fonte**
