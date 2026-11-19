# Estação 0 · Ingestão e varredura

Duas partes, nesta ordem. **A varredura vem antes do briefing**, não depois. Perguntar formato e
objetivo sem saber o que já foi publicado produz briefing errado, e o erro só aparece quando a peça
já está escrita.

---

# Parte A · Ingestão

Classificar o que chegou antes de decidir qualquer coisa. Nem todo trabalho começa em tema.

## O que fazer com cada coisa

| Chegou | Ferramenta | Cuidado |
|---|---|---|
| Link do YouTube | `youtube-full` (se instalada), ou `yt-dlp --write-auto-sub --skip-download` | A `youtube-full` usa a transcriptapi.com e gasta crédito. O `yt-dlp` é local e de graça: tentar ele primeiro |
| Reel, TikTok, Shorts | `gallery-dl` com o Chrome logado | Anti-bot resolve pelo navegador logado, nunca por CLI de terceiro nem extração de cookie |
| Post de LinkedIn ou Instagram | Chrome logado, `get_page_text` mais screenshot | O texto não traz o criativo. Ver a imagem também |
| Vídeo ou áudio sem legenda | `faster-whisper` | Extrair o áudio com ffmpeg antes. Modelo `small` já basta para português de reunião |
| PDF | leitura direta | PDF de slide vem com texto quebrado por caixa. Conferir a ordem de leitura |
| Imagem, print | leitura direta | Se for print de post, extrair o texto e a métrica que aparece |
| `.docx` | leitura direta | |
| Texto colado no chat | usar como está | Classificar pela tabela abaixo |
| Pasta inteira | um agente por arquivo, em paralelo | Consolidar no fim em um resumo só |
| Nada, só um tema | seguir direto para a Parte B | |

## As cinco classificações

A classificação decide o caminho da estação 2. Errar aqui contamina tudo que vem depois.

| Classificação | O que é | Caminho |
|---|---|---|
| `fonte` | Dado de fora que a peça vai citar | Verificar antes de usar. Se não sustenta, o ângulo cai junto |
| `material bruto` | Fala ou material da própria casa | A pauta sai do material, não de pesquisa nova |
| `rascunho` | Quem aprova já trouxe o texto escrito | Pula para a revisão |
| `briefing` | Instrução sobre o que fazer, não conteúdo | Radar de ângulo |
| `referência` | Peça de concorrente ou de terceiro trazida como estímulo | Ver abaixo |

## Referência: o caminho próprio

Quando quem aprova traz peça de concorrente ou de terceiro, ele quase nunca quer aquilo reproduzido.
Antes de tratar como pauta, separar **o que exatamente** está sendo trazido:

- **O tema** ("fala disso também")
- **O ângulo** ("essa tese é interessante")
- **O formato** ("gostei de como montaram")
- **A oportunidade** ("eles erraram, dá pra fazer melhor")

São quatro pedidos diferentes e produzem peças diferentes. Perguntar qual é, na estação 1.

E medir o que a referência realmente entregou antes de tomá-la como modelo. Seguidor não é
desempenho: uma peça de conta com centenas de milhares de seguidores pode ter engajamento pior que
o do cliente, e nesse caso ela não é referência de nada.

**Nunca citar concorrente na peça** sem quem aprova pedir de forma explícita.

## Material adversarial: o que joga contra o cliente

Nem toda referência é neutra. Parte do material que chega foi feito **por quem está do outro lado
da mesa** de quem o cliente atende.

**Como reconhecer.** Perguntar de quem é a voz do material e de onde vem o dinheiro dela. Se o
ganho de quem fala depende da perda de quem o cliente atende, o material é adversarial. Casos e
exemplos do cliente, quando houver, estão no `perfil.md` dele.

**O que fazer: virar munição.** O material não é descartado nem reproduzido. Ele é **invertido**,
e quem o cliente atende volta ao centro.

### A armadilha, e ela é séria

Material adversarial puxa a peça para o **medo**. O enquadramento que vale é o de **assimetria de
informação**, nunca o de ameaça: ameaça é chantagem e faz o herói virar vítima; assimetria mostra o
que ele não sabe e o põe para agir. O plano da peça é concreto: o que ele precisa saber, perguntar
ou exigir.

### Duas travas

1. **Não citar quem falou.** O material serve de gancho, não de fonte a creditar. Citar dá palco a
   quem está do outro lado.
2. **O fato de mercado precisa de fonte primária própria.** A fala do material **não** é a fonte.
   Levantar o dado de forma independente na estação 3, ou a peça não afirma nada sobre o tamanho ou
   o comportamento desse mercado.

⚠️ Cuidado com o falso contraste na tese. "Não é sobre X, é sobre a informação" é
exatamente o molde proibido. A tese precisa ser afirmativa.

---

# Parte B · Varredura

Duas consultas obrigatórias, sempre, antes de perguntar qualquer coisa a quem aprova.

## 1. O acervo

```bash
PYTHONIOENCODING=utf-8 python "<pasta-da-skill>/ferramentas/busca_acervo.py" --cliente <cliente> --top 10 "<regex do tema>"
```

⚠️ O `PYTHONIOENCODING=utf-8` evita quebra em emoji no título das notas (no PowerShell:
`$env:PYTHONIOENCODING="utf-8"` antes do comando).

**Rodar pelo menos três consultas com termos diferentes**, não uma. Uma única busca já deixou passar
peça idêntica publicada semanas antes. Buscar o tema, o conceito e o serviço.

Depois, **abrir as notas** das peças recentes que voltarem. O título não basta: a tese está no texto.

O que a varredura decide:

| Achou | Consequência |
|---|---|
| Nada sobre o tema | Território livre |
| Peça antiga (mais de 12 meses) | Candidata a repurpose declarado |
| Peça recente com a mesma tese | **Território queimado.** O ângulo precisa mudar antes do briefing |
| Peça recente com tese próxima | Mapear o que ela disse e achar o que sobrou |

## 2. O Diário de Bordo

O Diário do cliente (`paths.json`, campo `diario`), seção **"⛔ Não repetir"**.

Não é só sobre tema. Ali estão os erros de método que já custaram caro, e vários mudam como a peça
é escrita. Reprovado duas vezes no mesmo tema, parar e falar com quem aprova.

---

## O que sai da estação 0

Quatro coisas, todas antes do briefing:

1. **Resumo do que entrou**
2. **Classificação** entre as cinco
3. **O que a casa já publicou sobre isso**, com data, formato e taxa
4. **O que ficou queimado** e o que sobrou de território

## Regra de citação

Se o material for fala de alguém da casa do cliente e a peça for citar em aspas, a transcrição do
trecho precisa ser **reprocessada isolada** antes de virar citação. Transcrição automática de trecho
longo inventa palavra, e aspas erradas na boca de um porta-voz é erro que vai ao ar.

## Antes de usar qualquer voz

Conferir em `perfil.md` do cliente se a pessoa ainda é da casa.
