# Portão de pauta

Roda **antes de qualquer texto existir**. Seis perguntas, resposta por escrito, seis linhas.

## Por que existe

O loop de revisão mede execução, não pertinência. Uma premissa errada atravessa o portão de
qualidade com nota alta, porque os revisores otimizam a forma do que está lá.

Casos reais, todos em 48 horas:

| Peça | O que aconteceu |
|---|---|
| Post do LinkedIn | Três rodadas, notas 8 / 8,5 / 8,5, descartado: a tese era o consenso mais repetido do assunto |
| CPC 51 | O próprio briefing dizia que a norma não alcança o público, e o pacote foi escrito assim mesmo |
| NF-e de devolução | O ângulo aprovado era um falso contraste, e só o teste adversarial pegou |

O terceiro é o mais instrutivo: o teste rodou **antes** de escrever e custou dois minutos, em vez
de um pacote inteiro.

## As seis perguntas

### 1. Quem discordaria disso?

Se ninguém discorda, não vira conversa. Consenso morno não gera comentário, não gera
compartilhamento e não constrói posição.

**Reprova quando:** a resposta é "ninguém, é óbvio" ou "todo mundo concorda".

⚠️ Cuidado com a armadilha inversa: colocar a aresta no lugar indefensável. Se a única frase que
gera reação é uma generalização que não se sustenta, o ângulo está errado nos dois sentidos.

### 2. Isso alcança quem vai ler?

O público da peça precisa ser atingido pelo tema. Parece óbvio e falha na prática.

**Em pauta regulatória, ler o item de alcance da norma antes de escolher o público.** É o que
decide se a peça existe. Uma norma que só vale para companhias abertas não serve a conteúdo para
médio porte, por mais atual que seja.

**Reprova quando:** o tema não alcança quem a marca quer atingir.

### 3. Tem prova da casa?

Case, número próprio, fala de sócio, método ou pesquisa da marca. Conforme o `provas.md` do
cliente.

Sem isso, a peça é conteúdo que **qualquer concorrente poderia assinar**. Autoridade não vem de
citar fonte externa, vem do que a casa faz com ela.

**Reprova quando:** a peça funcionaria igual com o logo de outra empresa.

### 4. Já saiu algo igual?

Consultar o acervo publicado do cliente pelo `busca_acervo.py`. Se saiu:
- ângulo novo sobre o mesmo tema, **ou**
- a peça vira atualização e cita a anterior, **ou**
- a peça vira reaproveitamento (ver `formatos/repurpose-acervo.md`)

**Reprova quando:** é a mesma tese, com as mesmas palavras, sem gancho novo.

### 5. A tese tem forma de falso contraste?

Testar se a tese tem a forma **"não é A, é B"**. Não a frase: a **tese**.

Exemplo real que passou e foi pego só pelo adversarial: *"sua devolução vai ficar mais cara em
setembro, e o problema não é o imposto"*. Isso é literalmente "não é A, é B", e nenhum Grep pega,
porque ainda não existe texto.

O falso contraste na tese **força a aresta para o lugar errado**: para sustentar o "não é A", é
preciso atacar algo que não merecia ataque.

**Correção:** reescrever como afirmação positiva. "É A e também é B", ou escolher só B. Território
é aditivo, quase nunca excludente.

### 6. A casa entrega o que o CTA promete?

O CTA é uma **promessa comercial**. Se a peça converter, alguém do outro lado vai pedir o que ela
ofereceu. A pergunta é se existe serviço, pessoa e prazo para atender.

Três estados possíveis, e cada um tem uma ação:

| Estado | Ação |
|---|---|
| **Serviço de prateleira**, já vendido e entregue hoje | CTA pode nomear o entregável. Segue. |
| **Serviço em desenho**, sem preço, sem dono ou sem processo fechado | CTA vira **conversa**, não entregável. "Fale com o time X", nunca "a gente faz Y e devolve Z". |
| **Não existe** | Trocar o CTA ou trocar a pauta. Peça que gera demanda impossível de atender queima a marca com quem ela mais quer. |

**Reprova quando:** o CTA nomeia um entregável que a casa ainda não empacotou, e a peça vai ao ar
sem isso ser decidido por quem responde pela operação.

⚠️ **Isto não é zelo excessivo, é dano real e já aconteceu.** Em 07/08/2026 o motor produziu uma peça
de conversão cujo CTA prometia um levantamento que a casa ainda não vendia: serviço em desenho, com
decisões abertas na operação. Os serviços em desenho de cada cliente ficam no `perfil.md` dele.
As cinco perguntas anteriores passaram todas, porque nenhuma delas olha para a
capacidade da casa. O texto estava certo e a promessa não tinha lastro.

**Por que o portão e não a revisão.** O revisor de marca (5d) confere a **força** do CTA, e um CTA
com entregável nomeado é mais forte, então ele **premia** exatamente o defeito. Só o portão, que roda
antes e olha para fora do texto, pega isso.

## O que fazer com o resultado

| Resultado | Ação |
|---|---|
| Passou nas seis | Seguir para a estratégia |
| Reprovou em uma | Trocar o ângulo e rodar de novo. **Não escrever.** |
| Reprovou duas vezes no mesmo tema | Levar a quem aprova com as duas tentativas e o motivo |
| Escopo travado por quem aprova e a resposta é ruim | Dizer em uma linha **antes** de produzir, não depois, e produzir |

## Formato da resposta

Uma linha por pergunta, não um parágrafo por pergunta. O portão precisa ser barato, senão vira
etapa que se pula.

**Gravar como `portao.md` na pasta do trabalho, antes de qualquer arquivo de texto existir.**

```
PAUTA       <tema> · <data>
DISCORDA?   quem discordaria e por quê
ALCANÇA?    o público é atingido pelo tema
PROVA?      qual prova da casa entra
INÉDITO?    o que já saiu sobre isso
FORMA?      a tese não é "não é A, é B"
ENTREGA?    o que o CTA promete · prateleira | em desenho | não existe
VEREDITO    passou | reprovou em <qual> → novo ângulo: <qual>
```

**A linha `ENTREGA?` é obrigatória e o `check_entrega.py` reprova a pasta sem ela.** Foi feita campo
do template, e não parágrafo de recomendação, exatamente porque a falha é de omissão: quem escreve
já está com o CTA pronto na cabeça e não volta para perguntar se a casa entrega.

## O risco real não é pular o portão. É carimbá-lo.

Reprovar custa um dia; responder "passou" custa dois minutos. Quem preenche as seis perguntas é
o mesmo que já quer escrever, então o incentivo empurra para o carimbo. **Um portão carimbado é
pior que portão nenhum**, porque produz a sensação de ter validado.

Três defesas, em ordem de custo:

1. **O arquivo existe antes do texto.** Sem `portao.md` gravado, não se escreve. É verificável:
   basta olhar a data dos arquivos. Entra na verificação final.
2. **A reprovação é registrada, não só a aprovação.** Um histórico com 10 pautas e zero reprovações
   não significa pauta boa: significa portão quebrado.
3. **Em pauta de gancho externo** (notícia, regulação, celebridade), rodar o teste com um agente
   adversarial cuja tarefa é **derrubar a tese**. Custa 2 minutos e já salvou um pacote inteiro:
   o ângulo da NF-e foi aprovado e derrubado pelo adversarial.
