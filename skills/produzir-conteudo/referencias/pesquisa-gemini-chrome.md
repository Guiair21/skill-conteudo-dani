# Pesquisa profunda do Gemini, pelo Chrome (estação 3b)

É a pesquisa **secundária**: traz contexto, ângulos e pistas. O Gemini varre muitas páginas e
devolve muita coisa que não é fonte primária nem validada. Por isso o relatório dele nunca é fonte:
cada dado precisa ser validado na fonte primária (estação 3c), e quem decide o que entra é o
orquestrador, com o Opus nos casos duvidosos. A pesquisa primária, que vale como fonte, é a dos
agentes Haiku (estação 3a).

## Pré-requisitos

- Extensão **Claude in Chrome** instalada e conectada ao Claude Code.
- A usuária logada no Gemini (`gemini.google.com`) no próprio Chrome. Quem faz login é ela: o
  Claude nunca digita senha nem troca de conta.
- Sem a extensão ou sem login, a 3b é pulada e registrada em uma linha no `portao.md`. O artigo
  segue só com a 3a.

## Passo a passo

1. **Abrir uma aba** no Chrome em `https://gemini.google.com/app`.
2. **Ligar a Pesquisa Profunda.** No campo de mensagem, abrir as ferramentas e escolher
   "Deep Research" (Pesquisa Profunda). Se a opção não aparecer, a conta não tem acesso: pular a
   3b e registrar.
3. **Colar o pedido**, montado assim:

   ```
   Pesquisa para um artigo sobre: <tema e recorte>.
   Público: <quem lê>. País: Brasil.
   Perguntas que o artigo precisa responder:
   1. <pergunta de pesquisa>
   2. ...
   Priorize fontes primárias oficiais: órgãos públicos, normas no texto oficial, institutos de
   estatística, Banco Central, Receita Federal, CVM, CPC, CFC, documentos de companhias.
   Para cada dado, informe o valor, a data de referência, a fonte e o link exato.
   Separe dado observado de projeção. No fim, liste todas as fontes com link.
   ```

4. **Aprovar o plano.** O Gemini mostra o plano de pesquisa antes de começar. Conferir se ele
   cobre as perguntas; se faltar uma, pedir para incluir; depois clicar em iniciar.
5. **Esperar.** Leva alguns minutos. Enquanto isso, o orquestrador segue com o que não depende
   do resultado (estratégia, estrutura do artigo, pesquisadores da 3a).
6. **Trazer o resultado.** Ler o relatório pela página (leitura de texto, não print) e gravar em
   `<pasta do trabalho>/pesquisa-gemini.md`:
   - o relatório inteiro;
   - a **lista de fontes com os links**, uma por linha;
   - no topo: data, pergunta enviada e a linha "Status: pista, não fonte".
7. **Mandar para a conferência (3c).** O agente `conferente-de-fontes` abre cada link da lista.
   Só o que confere na fonte primária vai para a pasta `fontes/`, que é o fiel da balança.

## O que não fazer

- Não copiar número do relatório direto para o artigo. Número sem a página da fonte aberta e
  conferida não entra.
- Não usar como fonte o que o próprio Gemini escreveu, nem blog, agregador ou matéria que só
  repercute um dado: subir até quem produziu o dado.
- Não exportar para o Google Docs nem compartilhar o relatório: a pesquisa fica na pasta do
  trabalho.
- Não clicar em nada que publique, compartilhe ou apague na conta da usuária.
