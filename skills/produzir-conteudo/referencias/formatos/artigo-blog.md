# Artigo de blog (SEO + GEO)

Para o site do cliente (`perfil.md`, seção "Canais"). **Não é o artigo do LinkedIn com outro título.** Muda a estrutura, o
cabeçalho e a preocupação com citação por IA.

## O que o diferencia do artigo de LinkedIn

| | LinkedIn | Blog |
|---|---|---|
| Descoberta | Feed, quem já segue | Busca, quem nunca ouviu falar |
| Título | Promessa | Promessa **com a consulta de busca dentro** |
| Estrutura | Livre | Hierarquia de cabeçalhos que o crawler lê |
| Vida útil | Semanas | Anos, se for mantido |
| Sucesso | Engajamento | Posição, tráfego e **ser citado pela IA** |

## Estrutura

1. **H1** com a consulta principal
2. **Resposta direta nos primeiros 2 parágrafos.** É o trecho que a IA extrai para citar. Se a
   resposta só aparece no meio, a peça não é citada
3. **H2 por subtema**, cada um respondendo uma pergunta que alguém digitaria
4. **Trechos citáveis:** parágrafos curtos, autossuficientes, que fazem sentido fora do contexto
5. **FAQ** no fim quando o tema tiver perguntas laterais
6. **CTA** para o serviço correspondente

## Antes de escrever

Uma skill de cluster de SEO (`claude-seo:seo-cluster`, se instalada) mostra como o tema se organiza: o que é hub, o que é spoke, o que já está
saturado. Isso decide o recorte.

Uma skill de SXO (`claude-seo:seo-sxo`, se instalada) diz se o tipo de página bate com a intenção de busca. Artigo respondendo
consulta transacional não ranqueia, por melhor que seja.

## Revisores extras

O schema é obrigatório aqui (`claude-seo:seo-schema`, se instalada; senão, escrever à mão): JSON-LD de Article, e FAQPage quando houver FAQ. É o
único formato do catálogo em que ele entra.

## Regras da peça

- Toda afirmação com link para a fonte primária
- Cabeçalho descritivo, nunca criativo. O crawler e o leitor de busca precisam entender pelo texto
- Sem travessão
- Nada de keyword stuffing. Texto que soa forçado perde na leitura e não ganha na busca

## Entregável

`.docx` mais o JSON-LD em arquivo separado, prontos para publicar no CMS do cliente.
