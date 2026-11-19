# Revisão em loop

Estação 5. Roda **antes de qualquer imagem existir** e depois entrega o texto ao editor
estratégico.

## Por que existe do jeito que existe

O fluxo de 29/07/2026 trocou os revisores por uma varredura mecânica de voz e um editor. O texto
passou a sair correto e morno: nada segurava a qualidade da escrita, só a ausência de erro. Uma
varredura por expressão proibida acha travessão e vocabulário de robô. Ela não acha texto sem
tensão, dado sem contexto, card sem hierarquia, nem herói trocado.

**Ferramenta acha o defeito conhecido. Revisor acha o que ninguém listou.**

## Os revisores

Cada um recebe **o mesmo material** (texto completo mais plano de design) e devolve, de forma
independente:

- **nota de 0 a 10** com justificativa em duas linhas;
- **lista objetiva de correções**, cada uma acionável.

| # | Revisor | Skill | O que confere |
|---|---|---|---|
| 5a | **Dados** | `fact-checker`, se instalada; senão à mão: abrir cada fonte e conferir número, data e edição mais recente | Todo número com fonte primária datada e link. Nada desatualizado quando existe edição nova. Citação só com transcrição conferida. Nenhuma alegação sobre o que o cliente fez sem confirmação. |
| 5b | **Escrita** | `humanizer`, se instalada; senão à mão: varrer travessão, trinca, falso contraste e vocabulário de robô e reescrever | Marca de IA, travessão, trinca, falso contraste, vocabulário de robô, ritmo, escaneabilidade, força da primeira linha. |
| 5c | **Design** | agente de auditoria de design, se houver; senão à mão: conferir grid, hierarquia e regras de peça item a item | Grid, hierarquia, espaçamento, e as regras de peça do `marca.md` do cliente, item a item. |
| 5d | **Conteúdo e marca** | skill de posicionamento declarada no `perfil.md`, se instalada; senão à mão com o `perfil.md` | Herói e guia certos, tom, coesão entre as peças, força do CTA, se a peça sustenta a promessa do título. |
| 5e | **Persuasão** | `arsenal`, Módulo 1, se instalada; senão à mão com a tabela de gatilhos (fato verificável, promessa com lastro, regra 95-5) | Se o texto convence quem decide. Gatilho que não corresponde a fato verificável, promessa sem gravidade construída, consequência que o leitor ainda não somou (V-02), e a regra 95-5 (B-01): a peça fala com quem não está comprando hoje? |

**A nota do 5e sai da rubrica preenchida, nunca da impressão.** O `arsenal` exige a tabela do
Módulo 1 antes do número e o princípio citado pelo código com a página conferida na biblioteca.
Nota sem tabela é opinião, e o próprio `arsenal` lista isso como red flag.

**O 5e opina dentro da voz do cliente, não por cima dela.** Ele recebe o `voz.md` junto com o texto.
Princípio de persuasão que só funciona reescrevendo a peça fora da voz **é recusado por escrito**,
com o motivo, como qualquer outra correção. A ordem é: a voz é o limite, a persuasão trabalha
dentro dele. Sugestão de urgência, escassez ou prova social que não corresponde a fato verificável
cai pela mesma régua, e o público do cliente pune isso.

**Rodar em paralelo, em uma mensagem só**, com subagentes separados (skill `superpowers:dispatching-parallel-agents`, se instalada).
Revisor que enxerga o parecer do vizinho converge com ele e a nota perde valor.

Sem subagente no harness: rodar em sequência e **não ler o parecer anterior antes de escrever o
seguinte**. O que não pode é um papel só fazendo os quatro.

### Se um revisor morrer no meio (erro de API, limite de sessão, agente que não volta)

Isso é diferente de "o harness não tem subagente", e o motor não previa. Aconteceu em 07/08/2026:
dois revisores foram despachados e morreram por limite de sessão da API.

**O relançamento é obrigatório e acontece dentro do fluxo. Não se pergunta a quem aprova se pode.**
Transformar a queda de um agente em pergunta empurra para quem aprova uma decisão que é do fluxo, e
contraria o contrato autônomo do mesmo jeito que qualquer outro checkpoint inventado.

**O procedimento:**

1. **Ler a hora do reset na própria mensagem de erro.** Ela vem no formato "resets 3:30pm" com o
   fuso. Anotar.
2. **Seguir trabalhando no que não depende dos revisores**: imagem, produção gráfica, registro.
   O tempo de espera é tempo de trabalho, não de parada.
3. **Relançar os revisores que caíram assim que a hora passar**, sem avisar e sem pedir permissão.
   Conferir a hora atual contra o reset antes de concluir que ainda está bloqueado: qualquer
   resposta de API com timestamp serve de relógio.
4. **Rodar o loop de correção normalmente** com o que eles trouxerem, e só então fechar a peça.
5. Se a peça já tiver sido mostrada a quem aprova, **avisar o que mudou depois da revisão de verdade**.

| Situação | O que fazer |
|---|---|
| O reset já passou | Relançar agora. É o caminho padrão e não tem exceção. |
| O reset é daqui a pouco | Adiantar imagem, produção e registro, e relançar quando passar. |
| Quem aprova pediu a peça para agora e o reset não cabe | Rodar os passes em sequência e **declarar em bloco próprio no topo do `revisao.md`**: quais revisores não rodaram, por quê, e que as notas valem menos por viés de autor. Relançar depois mesmo assim. |
| O revisor exige rubrica que não dá para preencher sem a skill (caso do `arsenal`, Módulo 1) | **Deixar sem nota.** Escrever "não executado" e o motivo. |

**Nota inventada é pior que nota ausente.** Um "8,5" sem parecer vira histórico e contamina a
próxima decisão; um "não executado" é um buraco que alguém pode fechar depois. O `arsenal` lista
nota sem tabela como red flag da própria skill.

**A declaração é obrigatória e vai no topo do `revisao.md`, não em rodapé.** Quem lê o pacote precisa
saber, antes das notas, que elas não passaram por olho independente.

⚠️ **Peça fechada com revisor caído fica com dívida aberta.** Enquanto o relançamento não rodar, a
peça não está revisada, mesmo que todas as outras estações tenham passado.

## Quais entram por nível

| Nível | Revisores |
|---|---|
| **1 · Rápido** | 5b e 5d. Sem fact-check formal, porque não há dado externo. |
| **2 · Padrão** | 5a, 5b, 5d, 5e. |
| **3 · Completo** | os cinco. |

**O 5c entra por formato, não por nível.** Peça com card, carrossel, story ou capa passa pelo
diretor de arte mesmo no nível 1, junto com a estação 6. Quem decide é o que a peça tem, não quanto
a pesquisa custou.

Apareceu número externo em peça de nível 1? Subiu de nível. Não existe "rápido com um dadinho".

## O loop

1. Recebe os pareceres.
2. **Aplica a lista inteira de uma vez.**
3. Re-submete o texto corrigido.
4. Para **assim que todas as notas ficarem ≥ 8**. Pode ser na primeira rodada.

**Teto de 4 rodadas.** Se depois delas alguma nota não bateu 8, **não entregue a peça com a lista do
que falta**. Nota que não sobe em quatro rodadas não é problema de redação, é sinal de que a peça
está errada mais atrás: volte às estações 1 e 2, reabra o ângulo e a tese, reescreva a partir do
ângulo novo e rode o loop uma vez. Só então chame quem aprova, se ainda não bater. Detalhado no
`SKILL.md` do motor.

Registrar as notas de cada rodada no `revisao.md` (ou no fim do `conteudo.md`, no nível 1). **A
reprovação se registra tanto quanto a aprovação:** histórico em que nenhuma nota ficou abaixo de 8
significa revisor carimbando, não texto bom. É a mesma defesa que o portão de pauta usa contra o
carimbo, e o loop precisa dela pelo mesmo motivo, porque quem escreve e quem dá a nota são a mesma
pessoa.

**Aplicar 8 de 12 correções garante regressão.** As que ficam voltam na rodada seguinte, o revisor
gasta a rodada repetindo o que já disse, e a nota cai. Se uma correção não vai ser aplicada, ela é
**recusada por escrito com o motivo**, não ignorada.

## Nota alta não é aprovação de pauta

O loop mede execução, não pertinência. Um post levou 8 / 8,5 / 8,5 e foi descartado: a tese era o
consenso mais repetido do assunto, e os revisores otimizaram a forma do que estava lá. É por isso
que o portão roda antes, na estação 1, e é por isso que o editor roda depois.

## Depois dos revisores: o editor

O revisor acha erro. O editor pergunta se o que está lá é o teto, e **escreve a alternativa**.
Rubrica e formato do parecer em `editor-estrategico.md`.

O bloco de decisão (`aceito` / `recusado` mais o motivo, uma linha por elemento) é obrigatório.
O `check_entrega.py` reprova a pasta sem ele.

## A tese não se discute aqui

O teste de tese roda na **estação 2b**, antes de existir texto, e está descrito no `SKILL.md` do
motor. Foi movido para lá em 07/08/2026 pelo motivo mais simples possível: se a tese cai depois da
escrita, do loop e do editor, o pacote inteiro morre e a peça volta para a estação 1 do mesmo jeito.

Se um revisor daqui derrubar a **premissa** em vez de apontar erro de execução, isso não é correção
de rodada. É a peça voltando para a estação 1, pela mesma porta do teto de rodadas.

## A rede mecânica

```bash
python "<pasta-da-skill>/ferramentas/check_voz.py" conteudo.md --cliente <cliente>
```

Roda **depois** de aplicar as correções, para pegar o que voltou na reescrita. Exit code 1 é
reescrever, não negociar a nota.

**Ela não substitui o revisor 5b.** Uma passa por lista de proibições; o outro reescreve o que
está fraco. Trocar um pelo outro foi exatamente o que fez a qualidade cair.
