# Artigo e produção editorial: o roteiro

Artigo é o formato principal deste motor. Este roteiro amarra as estações para ele. Regras de
forma em `formatos/artigo-blog.md` e `formatos/artigo-linkedin.md`.

## A pasta do trabalho

```
<pasta do trabalho>/
  portao.md              estação 1: portão, recorte, perguntas de pesquisa
  estrategia.md          estação 2: StoryBrand e esqueleto do artigo
  fontes/                estação 3: o fiel da balança, só fonte primária conferida
  pesquisa-gemini.md     estação 3b: relatório do Gemini (pista, não fonte)
  conferencia-fontes.md  estação 3c: veredito de cada link
  artigo.md              estação 4: o texto
  revisao/               estação 5a: dados.md, estilo.md, editorial.md, por rodada
  revisao.md             estação 5b: decisões do editor
  verificacao-final.md   estação 5c: veredito do Opus
  _aprovacao.pdf         estação 7: o que vai para quem aprova
```

## As estações, no artigo

| Estação | No artigo | Quem |
|---|---|---|
| 1 · Portão | tese contestável em uma frase; ângulo que o acervo ainda não tem; de 3 a 6 perguntas de pesquisa | orquestrador (Sonnet) |
| 2 · Estratégia | StoryBrand; esqueleto com título, lide e intertítulos; palavra que o público busca | orquestrador |
| 2b · Tese | a melhor evidência contra a tese, antes de escrever | outro modelo ou `segunda-opiniao` |
| 3a · Fontes | um pesquisador por pergunta, em paralelo | `pesquisador-fontes` (Haiku) |
| 3b · Gemini | pesquisa profunda pelo Chrome, para ampliar fontes | orquestrador, via Claude in Chrome |
| 3c · Fiel da balança | reabre cada link; só o que confere fica em `fontes/` | `conferente-de-fontes` (Haiku) |
| 3d · Busca | perguntas reais do público viram intertítulos | orquestrador, no navegador |
| 4 · Escrita | artigo inteiro, cada número com link para a página de `fontes/` | orquestrador |
| 5a · Revisores | dados, estilo, editorial, em paralelo, até nota 8 | três agentes (Haiku) |
| 5b · Editor | alternativa escrita para título, lide e CTA | orquestrador, papel separado |
| 5c · Verificação final | leitura cega, aprova só com nota 9 | `verificador-final` (Opus) |
| 7 · Produção | PDF de aprovação; versão do blog e do LinkedIn | orquestrador |
| 8 · Fechar | `check_entrega.py`, Diário de Bordo | orquestrador |

## Regras de escrita do artigo

- **Tese no primeiro parágrafo**, numa frase que alguém poderia contestar.
- **Lide responde o que o leitor ganha** em ler até o fim.
- **Intertítulos que contam o artigo sozinhos.** Use as perguntas reais da 3d.
- **Cada seção abre com uma resposta direta** de duas ou três frases, com fonte: é o trecho que
  buscador e IA citam.
- **Número com link para a fonte primária**, no próprio texto, e com a data de referência.
- **Norma pelo nome e artigo** (ex.: "art. 12 da LC 214/2025"), com link para o texto oficial.
- **Exemplo do tamanho de quem lê:** a empresa do público, não a multinacional.
- **Fecho com o próximo passo concreto** e CTA que o cliente entrega hoje.

## Quando parar

As quatro paradas do contrato de operação, mais uma própria do artigo: **o dado central da tese
não foi encontrado em fonte primária**. Sem ele, a tese não se sustenta; voltar à estação 1.
