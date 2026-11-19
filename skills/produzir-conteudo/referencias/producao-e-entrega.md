# Produção e entrega

Estações 7 e 8. Começa **depois** do portão de qualidade liberado, nunca antes.

## Ordem de produção (não inverter)

1. **Imagens** definidas (estação 6), pela ordem de prioridade do `marca.md` do cliente.
2. **Peças renderizadas**: PNG no tamanho do canal, mais o HTML fonte de cada uma.
   - **Gerador, ordem de verificação e pasta de saída** são os que a config e a camada do cliente
     declaram (`marca.md`, `perfil.md` e a `linha-de-montagem.md` da skill do cliente).
3. **Texto longo em `.docx`**, quando houver artigo ou roteiro. O `.md` é arquivo de trabalho, o
   entregável é o `.docx`.
4. **Material de aprovação** montado por último, porque ele mostra as peças **já renderizadas** ao
   lado da copy.

Montar o PDF antes de renderizar produz o pior erro possível: um material que parece pronto e está
cheio de retângulo tracejado. O template desenha placeholder quando o PNG não existe, e **nada
avisa** que ele ficou.

## Material de aprovação

Quem aprova precisa ler a tese antes de ver as peças que saíram dela. **O texto longo vem antes dos
cards**, logo depois da capa.

No modo autônomo, gerar o **material completo sem perguntar**. É decisão travada. Só gerar a
versão reduzida (só as peças visuais) se ele pedir na hora.

Layout canônico e pegadinhas do pipeline: `marca.md` do cliente. O caminho do template está no
`perfil.md`, seção "Skills e ativos que o motor pluga aqui". Em template pronto, troca-se só os
blocos `CONFIG` e `CONTEÚDO`: o layout é fixo de propósito.

## Quando o pipeline gráfico quebra

É a parte que mais custa token quando dá errado. Dois reflexos, nesta ordem:

1. **Erro de biblioteca ou parâmetro** (`python-docx`, Pillow, Playwright, reportlab,
   `python-pptx`): consultar a documentação oficial da biblioteca (Context7, se disponível) antes
   de tentar por tentativa e erro. Chutar assinatura de função e rodar para ver o que acontece é o
   caminho caro.
2. **Erro de render, layout, caminho ou encoding**: depurar de forma sistemática (skill `superpowers:systematic-debugging`, se instalada;
   senão, hipótese, teste e só então correção) em vez de remendar. As pegadinhas já pagas estão no `marca.md` do cliente. Conferir essas primeiro,
   porque já custaram uma vez.

## Onde salvar

Na pasta do trabalho dentro da pasta de produção do cliente (`paths.json`, campo `producao`),
**nunca no Desktop**. Nomes claros em português.

## Antes de anunciar

```bash
python "<pasta-da-skill>/ferramentas/check_entrega.py" "<pasta do trabalho>" --cliente <cliente>
```

Exit code 1 significa que não está pronto: não anunciar, não abrir para o cliente, não dizer
"concluído". Ele confere que o portão existe e antecede os textos, que a consulta ao acervo está
colada, que não há placeholder no material de aprovação, que todo dado tem link, que a varredura de
voz passa e que o editor deixou decisão registrada.

Passou: **abrir a saída** (`Start-Process` no Windows, `open` no macOS, `xdg-open` no Linux). Arquivo
único para peça avulsa, a **pasta** quando for lote.

## Registro do cliente e pasta de notas

O registro da demanda, quando o cliente tem um (seção "Registro" do `perfil.md`), **nasce na
entrada**, na estação 0. Aqui ele fecha, do jeito que essa seção mandar: status, colunas, link da
nota, campos de frontmatter.

**Na pasta de notas do cliente**, com o "pode" de quem aprova: nota da peça no lugar, no formato
e com os campos que o `perfil.md` ou a camada do cliente definir, com ligação para os tópicos que a
peça toca.

**A proposta da nota vai junto com o pacote**, na mesma mensagem da entrega: caminho, título e as
conexões sugeridas. Perguntar antes de gravar é regra fixa; entregar sem propor o registro é
esquecer o acervo, que é onde o histórico do cliente fica consultável.

**Reconciliar em lote é outra operação**, declarada no `perfil.md` do cliente quando existir. Ela
roda quando quem aprova pede, não no fim de cada peça.

## Diário de Bordo (obrigatório, sempre)

Acrescentar uma entrada no **Log** do Diário de Bordo do cliente, um arquivo local apontado no
`paths.json` (campo `diario`):

```markdown
### AAAA-MM-DD · [nome do trabalho]

**Contexto.** O que foi pedido, em uma frase.
**O que custou caro.** Retrabalho, caminho errado, token queimado à toa. Específico e honesto.
**O que rendeu.** Template, atalho, ângulo ou verificação que vale reusar. Cite o caminho.
**Verificações feitas.** Que dado foi checado e contra qual fonte primária.
**Verificação pendente.** O que ficou sem conferir. Nunca em branco por conveniência.
```

Se um item de "O que custou caro" **já apareceu antes** no Log, promova: escreva na seção
"⛔ Não repetir" e, se o harness tiver memória persistente, registre lá também. Log é
rascunho, a lista de "⛔ Não repetir" é lei.

Não invente entrada positiva para parecer produtivo. Trabalho liso que não ensinou nada se resolve
em uma linha.

## Timing de publicação

| Canal | O que lembrar |
|---|---|
| LinkedIn | Terça, quarta ou quinta, entre 8h e 10h. Ficar 30 a 60 min respondendo os primeiros comentários. |
| Instagram | Link vai no story ou nos destaques, nunca na legenda: o IG não deixa link clicável no texto. |
