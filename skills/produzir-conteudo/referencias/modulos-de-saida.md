# Módulos de saída

O conteúdo-base é escrito uma vez. As saídas são **escolhidas**, não impostas.

## Por que existe

A skill anterior entregava sempre artigo longo, carrossel de 9 cards e story. Quando o acervo foi
medido, essa era **a pior combinação da conta**, formato por formato. O pacote fixo não era uma
decisão editorial: era um hábito que ninguém tinha testado.

## Como escolher

**Consultar `formatos.md` do cliente.** Ele tem a tabela de desempenho medido por canal, formato e
grau de consciência. Sem esse arquivo, não há escolha informada, e a peça vira palpite.

Regra: **o objetivo escolhe o formato, e o dado desempata.**

⚠️ **Declarar qual métrica está na mesa.** Taxa e volume absoluto dão rankings opostos, porque o
que alcança mais acumula mais interação e converte proporcionalmente menos. Volume responde "o que
trouxe mais retorno total"; taxa responde "o que prendeu quem viu". Nunca comparar o ranking de
uma com o da outra.

## Catálogo

| Módulo | Quando | Cuidados |
|---|---|---|
| **Documento (LinkedIn)** | alcance e engajamento | PDF nativo. Sem numeração de slide. |
| **Artigo** | autoridade, SEO, ser citado por IA | Aceitar taxa baixa: ele serve a coisas que a taxa não mede. Passar uma skill de GEO (`claude-seo:seo-geo`, se instalada) ou conferir à mão que há passagens citáveis. |
| **Post de texto** | conversa, testar tese | Formato legítimo e completo. Não inventar imagem para "completar". |
| **Carrossel (Instagram)** | desdobrar dado ou lista | Sem numeração. Regras de peça no `marca.md`. |
| **Reels** | alcance no Instagram | **Roteiro e direção de cena, nunca vídeo editado.** |
| **Story** | levar ao link | Botão vazio no PNG que vai ao ar. |
| **Newsletter** | base própria | Deriva do conteúdo-base. |
| **Roteiro de vídeo** | porta-voz | Teleprompter mais direção. |
| **FAQ / GEO** | ser citado por IA | Afirmação clara, dado com contexto, trecho autônomo. |
| **Landing / e-mail** | campanha | Só quando há oferta. |

## Regras que valem para qualquer combinação

**Nunca inventar peça para completar pacote.** Se o objetivo pede um documento, entregar um
documento. Três peças fracas não valem uma forte.

**Uma peça por canal, no máximo, por rodada.** Duas peças disputando a mesma audiência no mesmo dia
canibalizam alcance.

**A derivação é seletiva.** Um conteúdo-base pode virar 2 a 4 peças, cada uma com ângulo próprio e
justificativa. Não 20. Volume não é gargalo: o gargalo é pertinência, e derivar em massa multiplica
revisão e repete o mesmo ângulo em cinco lugares.

## Reaproveitamento

Antes de escrever peça nova, **checar o acervo**. Quando o cliente tiver lista de candidatos a
reaproveitar, ela está no `formatos.md` dele.

Peça antiga que voltou a ser relevante custa uma abertura nova, não um pacote inteiro. Ao
reaproveitar, marcar a nota de origem no campo que o cliente usar (`formatos.md`), para não repetir.

## Antes de renderizar

Nada de imagem antes do portão de qualidade passar. Renderizar peça que vai ser reescrita é o
desperdício mais caro do fluxo, porque o pipeline gráfico é a parte que mais custa quando dá
errado.
