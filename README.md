# Skill de conteúdo · vamos trabalhar

Linha de montagem de conteúdo para o Claude Code, otimizada para **artigo e produção editorial**:
da pauta ao PDF de aprovação, com portão de pauta, fontes primárias como fiel da balança, pesquisa
profunda opcional do Gemini pelo Chrome, revisores em loop (Haiku) e verificação final (Opus). Vem
com uma base de fontes de controladoria, contabilidade, gestão financeira e tributário.

Duas skills trabalham juntas:

| Skill | Papel |
|---|---|
| `vamos-trabalhar` | o gatilho. Diga "vamos trabalhar" e ela escolhe o cliente e dispara o motor |
| `produzir-conteudo` | o motor. As estações 0 a 9, as referências e as ferramentas de checagem |

## Instalação

1. Clone o repositório numa pasta fixa, por exemplo `Documentos\skill-conteudo-dani`.
2. Copie (ou crie um atalho de) `skills/vamos-trabalhar`, `skills/produzir-conteudo` e `skills/gerar-imagem` para a pasta
   de skills do Claude Code: `%USERPROFILE%\.claude\skills\` no Windows, `~/.claude/skills/` no Mac.
3. Diga ao motor onde está a config, definindo a variável de ambiente `MOTOR_CONFIG_DIR` com o
   caminho da pasta `config` do repositório clonado. No PowerShell:

   ```powershell
   [Environment]::SetEnvironmentVariable("MOTOR_CONFIG_DIR", "$HOME\Documents\skill-conteudo-dani\config", "User")
   ```

   Se as skills forem usadas direto de dentro do repositório (atalho em vez de cópia), a variável
   não é necessária: as ferramentas acham `config/` sozinhas.
4. Copie os arquivos da pasta `agents/` para `%USERPROFILE%\.claude\agents\` (Mac:
   `~/.claude/agents/`). São os agentes da cadeia de verificação:

   | Agente | Modelo | Papel |
   |---|---|---|
   | `pesquisador-fontes` | Haiku | acha a fonte primária de cada pergunta de pesquisa |
   | `conferente-de-fontes` | Haiku | reabre cada link e diz se confere |
   | `revisor-dados`, `revisor-estilo`, `revisor-editorial` | Haiku | revisão em loop, até nota 8 |
   | `verificador-final` | Opus | leitura cega final, aprova só com nota 9 |

   O orquestrador é o Sonnet: a skill `produzir-conteudo` fixa `model: sonnet` enquanto roda.
5. Para a pesquisa profunda do Gemini (opcional): instale a extensão **Claude in Chrome**, conecte
   ao Claude Code e deixe o Gemini logado no seu Chrome. Roteiro em
   `skills/produzir-conteudo/referencias/pesquisa-gemini-chrome.md`. Nenhuma chave de API é usada.
6. Para gerar imagem (opcional, usa a assinatura do ChatGPT): copie também
   `skills/gerar-imagem` para a pasta de skills. Na primeira vez que precisar, ela mesma orienta a
   instalar o Codex CLI (`npm install -g @openai/codex` e `codex login`). Nenhuma chave de API é
   usada.
7. Python 3.10 ou mais novo. As ferramentas usam só a biblioteca padrão. O `check_layout.py` e o
   gerador de PDF precisam do Google Chrome instalado.

## Primeiro uso

1. Copie `config/exemplo` para `config/<nome-do-cliente>` e preencha os arquivos (o README de lá
   explica cada um).
2. No Claude Code, diga **"vamos trabalhar"**, informe o tema e o objetivo da peça.
3. O fluxo roda sozinho e só para em quatro casos (pauta reprovada duas vezes, dado que não bate com
   a fonte, item da lista "Não repetir", premissa do briefing que caiu na checagem).

Teste rápido das ferramentas:

```powershell
python skills/produzir-conteudo/ferramentas/busca_acervo.py "fluxo de caixa" --cliente exemplo
python skills/produzir-conteudo/ferramentas/check_voz.py config/exemplo/voz.md --cliente exemplo
```

## Skills opcionais

O motor cita outras skills. Nenhuma é obrigatória: sem elas, o passo é feito à mão.

| Skill | Estação | Sem ela |
|---|---|---|
| `fact-checker` | 5 · reforço do `revisor-dados` | o agente `revisor-dados` faz o papel |
| `humanizer` | 5 · reforço do `revisor-estilo` | o agente `revisor-estilo` faz o papel |
| `arsenal` | 5 · revisor de persuasão em peça curta | avaliar gancho, prova e CTA pela rubrica do `revisao.md` |
| `segunda-opiniao` | 2b · teste da tese | pedir a outro modelo a melhor evidência contra a tese |
| `last30days` | 3 · escuta social | ler os comentários e posts recentes do tema à mão |
| `superpowers` | 5 · revisores em paralelo | rodar os revisores um de cada vez, sem ler o parecer anterior |

## O que este repositório não tem

Nenhuma chave de API, senha, token ou conector. Publicar, enviar e-mail ou gravar em serviço
externo fica com quem aprova a peça.
