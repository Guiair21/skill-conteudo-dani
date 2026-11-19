# Skill de conteúdo · vamos trabalhar

Linha de montagem de conteúdo para o Claude Code: da pauta ao PDF de aprovação, com portão de
pauta, pesquisa com fonte, escrita na voz da marca, revisão em loop e checagem de entrega. Vem
com uma base de fontes de controladoria, contabilidade, gestão financeira e tributário.

Duas skills trabalham juntas:

| Skill | Papel |
|---|---|
| `vamos-trabalhar` | o gatilho. Diga "vamos trabalhar" e ela escolhe o cliente e dispara o motor |
| `produzir-conteudo` | o motor. As estações 0 a 9, as referências e as ferramentas de checagem |

## Instalação

1. Clone o repositório numa pasta fixa, por exemplo `Documentos\skill-conteudo-dani`.
2. Copie (ou crie um atalho de) `skills/vamos-trabalhar` e `skills/produzir-conteudo` para a pasta
   de skills do Claude Code: `%USERPROFILE%\.claude\skills\` no Windows, `~/.claude/skills/` no Mac.
3. Diga ao motor onde está a config, definindo a variável de ambiente `MOTOR_CONFIG_DIR` com o
   caminho da pasta `config` do repositório clonado. No PowerShell:

   ```powershell
   [Environment]::SetEnvironmentVariable("MOTOR_CONFIG_DIR", "$HOME\Documents\skill-conteudo-dani\config", "User")
   ```

   Se as skills forem usadas direto de dentro do repositório (atalho em vez de cópia), a variável
   não é necessária: as ferramentas acham `config/` sozinhas.
4. Python 3.10 ou mais novo. As ferramentas usam só a biblioteca padrão. O `check_layout.py` e o
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
| `fact-checker` | 5 · revisor de dados | conferir cada número contra a fonte com link |
| `humanizer` | 5 · revisor de estilo | revisar contra as proibições do `voz.md` |
| `arsenal` | 5 · revisor de persuasão | avaliar gancho, prova e CTA pela rubrica do `revisao.md` |
| `segunda-opiniao` | 2b · teste da tese | pedir a outro modelo a melhor evidência contra a tese |
| `last30days` | 3 · escuta social | ler os comentários e posts recentes do tema à mão |
| `superpowers` | 5 · revisores em paralelo | rodar os revisores um de cada vez, sem ler o parecer anterior |

## O que este repositório não tem

Nenhuma chave de API, senha, token ou conector. Publicar, enviar e-mail ou gravar em serviço
externo fica com quem aprova a peça.
