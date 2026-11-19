# Júri de cinco versões (fora do motor desde 07/08/2026)

> ⚠️ **Isto não é mais uma estação.** O motor não chama este método. Ele saiu porque cobrava cinco
> redações na etapa que menos falha: as peças descartadas aqui morreram por tese, não por execução,
> e tiraram 8 e 8,5 antes de serem jogadas fora. O arquivo fica como método disponível para rodar à
> mão, quando quem aprova pedir, em peça em que o custo do erro justifique. Estação 4 do motor: uma
> redação, e o loop de revisão faz o resto.

Cinco agentes escrevem a peça. Um júri escolhe. O melhor dos perdedores é enxertado no vencedor.

## Por que cinco e não um

Um agente escrevendo sozinho entrega a primeira solução que encontra e depois só a defende. Cinco
ângulos diferentes escritos em paralelo produzem coisas que uma única passada não produz, e o custo
está na escrita, que é barata perto de publicar peça morna.

## Como os cinco se dividem

Os cinco não escrevem a mesma peça cinco vezes. Cada um recebe uma **entrada diferente** para a
mesma pauta: abertura pelo número, abertura pela cena, abertura pela pergunta, abertura pela
objeção do leitor, abertura pelo caso concreto. Mesma pauta, mesmo StoryBrand, entradas distintas.

Se as cinco versões voltarem parecidas, as entradas não estavam distintas o bastante. Refazer a
divisão, não seguir para o júri.

## O júri: um juiz por critério

**Não usar rubrica única.** Rubrica composta produz efeito halo: o juiz gosta da abertura e a nota
inteira sobe junto. Um juiz isolado por critério, cada um cego para a nota dos outros:

| Juiz | Pergunta que ele responde |
|---|---|
| Abertura | A primeira linha faz o público do cliente parar? |
| Argumento | O plano se sustenta ou é conselho genérico? |
| Prova | Os dados sustentam o que o texto afirma? |
| Voz | Soa à voz do cliente (`voz.md`) ou soa a IA escrevendo sobre o assunto? |
| Fecho | O CTA é consequência do texto ou foi colado no fim? |

O vencedor é o que ganha em mais critérios. Depois disso, **enxertar**: se outra versão tem uma
abertura melhor, a abertura dela entra. O produto final não precisa ser uma das cinco versões
puras.

Método de juiz isolado por critério; nenhum harness é necessário.

## A voz

- `voz.md` do cliente é a fonte, sempre
- as skills de voz e de posicionamento são as que o `perfil.md` do cliente declara, na seção
  "Skills e ativos que o motor pluga aqui"
- em texto longo, exigir a peça completa e recusar placeholder ou "resto igual ao anterior"

## Regras de escrita humana

Valem para as cinco versões e para o texto final:

- **Travessão proibido.** Em qualquer texto
- Sem falso contraste ("não é X, é Y" como muleta)
- Sem trinca de adjetivos
- Sem vocabulário-robô
- Tom de colega que entende do assunto, não de palestrante

## O tom do cliente

Sai do `perfil.md` e do `voz.md` do cliente. Mesma dor, sem chantagem, quando a config pedir.

## Erro objetivo x convenção da área

Em texto que leva a assinatura de um especialista da casa, **não corrigir, apontar**. E apontar só
o que se prova. Convenção da área vai como pergunta, não como correção.

## O que sai daqui

Dois arquivos, e eles precisam ficar **separados**:

| Arquivo | Conteúdo |
|---|---|
| `conteudo.md` | A peça, o briefing e o StoryBrand. Só isso |
| `montagem.md` | Qual versão venceu cada critério, o que foi enxertado de onde, e o que foi descartado por quê |

**Por que separados:** o registro de montagem cita os padrões que foram rejeitados (o falso
contraste que não entrou, o número inventado que saiu). A varredura de voz roda no `conteudo.md` e
acusa essas citações como violação, reprovando peça limpa. Aconteceu no primeiro uso da skill.

O `check_voz.py` roda **só no `conteudo.md`**. O `montagem.md` fica de fora da varredura de
propósito.

## A varredura não é o revisor

Rodar `<pasta-da-skill>/ferramentas/check_voz.py` (ver `SKILL.md`) no `conteudo.md`, e depois **ler as junções de
linha no olho**: a varredura não atravessa quebra de linha, e falso contraste partido em duas
linhas passa limpo.

E ler o texto inteiro procurando o que regex nenhum pega: pronome sem antecedente (aparece quando
se enxerta trecho de outra versão), repetição de palavra em parágrafos vizinhos, e argumento que
ficou sem elo depois do corte.
