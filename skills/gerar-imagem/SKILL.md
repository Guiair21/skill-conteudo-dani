---
name: gerar-imagem
user-invocable: true
description: >
  Use quando a usuária pedir uma imagem gerada por IA, ou quando o fluxo de conteúdo precisar de
  uma: foto conceitual, ilustração, objeto, textura, fundo, capa de artigo, variação de uma imagem
  que já existe. Dispare com "/gerar-imagem", "gera uma imagem de", "cria uma arte de", "faz uma
  foto conceitual", "manda pro Codex gerar", "edita essa imagem". NÃO use para card, carrossel,
  story, slide nem qualquer peça com texto: o texto vai em camada de HTML. Responda sempre em
  português.
---

# /gerar-imagem: Claude Code → Codex → arquivo na pasta do cliente

## Antes da primeira vez: instalar o Codex (uma vez só)

A imagem é gerada pelo **Codex CLI**, logado na conta do **ChatGPT** da usuária. Não usa chave de
API nem cobra por imagem: roda dentro da assinatura.

Se o comando `codex` não existir no terminal, orientar a usuária, passo a passo:

1. Instalar o **Node.js** (versão LTS) em https://nodejs.org e reabrir o terminal.
2. No PowerShell, instalar o Codex:

   ```powershell
   npm install -g @openai/codex
   ```

3. Entrar na conta do ChatGPT (abre o navegador; quem faz o login é ela):

   ```powershell
   codex login
   ```

4. Testar sem gastar nada:

   ```powershell
   python "<pasta-da-skill>/gerar_imagem.py" "teste" --cliente <cliente> --seco
   ```

`<pasta-da-skill>` é o diretório-base desta skill, que o Claude Code informa ao carregá-la.

## O princípio

O Codex CLI tem a ferramenta integrada `image_gen.imagegen`, ligada pela flag
`--enable image_generation`. Ela roda dentro dos limites da assinatura, sem `OPENAI_API_KEY` e sem
cobrança por imagem.

Duas coisas quebram a ponte se você não souber:

1. **A imagem não nasce na pasta do projeto.** Ela cai sempre em
   `~/.codex/generated_images/<thread-id>/exec-<uuid>.png`. A tool não aceita caminho de destino.
2. **O `--json` não devolve o caminho.** Nenhum evento do JSONL cita o arquivo.

Por isso quem manda no destino é o `gerar_imagem.py`: ele lê o `thread_id` que o Codex anuncia no
`--json` e copia só os PNGs da pasta daquele thread.

## Quando não usar

- **Card, carrossel, story, capa com texto.** Texto é camada de HTML. A imagem gerada entra como
  fundo ou como objeto, nunca com a copy dentro.
- **Logo e símbolo de marca.** São arquivos da marca (SVG). Nunca gerar.

## A sequência

**1. Travar o briefing.** Uma frase de assunto, uma de direção visual (luz, fundo, enquadramento),
uma de proibição. Sem isso a imagem sai genérica.

**2. Resolver o cliente.** Pelo contexto da conversa, sem perguntar de novo. O destino sai do
`paths.json` do cliente (`config/<cliente>/`), chave `imagens`.

**3. Rodar.**

```bash
python "<pasta-da-skill>/gerar_imagem.py" \
  "pilha de notas fiscais sobre mesa de madeira, luz lateral suave, fundo desfocado" \
  --cliente <cliente> --marca <cliente> --nome notas-fiscais --abrir
```

| Flag | Para quê |
|---|---|
| `--cliente` | resolve a pasta pelo `paths.json`. Sem ele, cai no diretório atual |
| `--saida` | pasta explícita; sobrepõe `--cliente` |
| `--marca <cliente>` | injeta o `marca.md` do cliente (paleta e proibições) antes do briefing |
| `--nome` | slug do arquivo. Padrão: derivado do briefing |
| `--ref arquivo.png` | **edição**: parte de uma imagem que já existe. Repetível |
| `--variacoes N` | N imagens na mesma chamada, mais barato que N chamadas |
| `--seco` | mostra prompt e comando sem gastar nada. Use para conferir o prompt |
| `--abrir` | abre a pasta no fim |

O script imprime JSON com os caminhos finais. Mostre o caminho à usuária e **abra a imagem**.

**4. Olhar a imagem antes de entregar.** Leia o PNG. Mão com seis dedos, texto inventado no fundo,
rosto onde não podia: tudo isso passa se ninguém abrir.

## O que a ferramenta não faz

- **Não aceita tamanho nem proporção.** O modelo decide pelo texto. Descrever o enquadramento
  influencia, não garante. Formato final é recorte depois.
- **Não aceita mais de 1 imagem por chamada da tool.** `--variacoes` resolve pedindo várias
  chamadas dentro da mesma sessão.
- **Não tem seed.** Duas rodadas do mesmo prompt dão imagens diferentes.

## PNG transparente direto

Para objeto de colagem, comece o prompt com "Gere uma imagem PNG com FUNDO TRANSPARENTE (canal
alfa, background transparent, sem cor de fundo nenhuma), recorte limpo do objeto isolado". Sai RGBA
com alfa real. Confira sobre o fundo da peça antes de usar.

## Custo e tempo

Cada geração leva de 1 a 3 minutos e gasta cerca de 30 mil tokens da assinatura do Codex. Para
lote grande, avise a usuária do tempo antes de disparar.

Existe um caminho de API do Codex que exige `OPENAI_API_KEY` e cobra por imagem. Não usar sem a
usuária pedir com essas palavras.

## Gotchas apurados

- **Windows:** o script passa `-c windows.sandbox="unelevated"` (o sandbox elevado já quebrou com
  `setup refresh had errors`) e `--disable apps` (com apps ligados, o Codex tentava gerar por outro
  aplicativo e falhava). Flag `--modelo` existe para testar outro modelo se um parar de gerar.
- O teste de que funciona é pedir uma imagem e ver se aparece pasta nova em
  `~/.codex/generated_images`. Perguntar ao Codex "image_gen está disponível?" não serve.
- `codex` no Windows é um `.cmd`. O script chama por `cmd.exe /c` e manda o prompt por **stdin**
  (`-`), o que evita quebrar com aspas e acento.
- **Lote em paralelo pode, desde que pelo script** (o corte por `thread_id` evita que uma execução
  pegue a imagem da outra). Ao matar um lote, mate também os processos `codex` órfãos.
- **Uma chamada pode devolver mais de uma imagem.** O script salva as duas, a segunda com sufixo
  `-2`. Olhe as duas antes de escolher.
- **Editar uma imagem que está na própria pasta de saída pode apagar a original.** Antes de editar,
  copie a referência para outra pasta ou use um nome novo.
- Se o script disser "nenhuma imagem nova", quase sempre o Codex respondeu em texto em vez de
  chamar a tool. Rode com `--seco`, leia o prompt e deixe o pedido de imagem mais direto.
