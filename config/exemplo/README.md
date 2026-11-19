# Config de cliente · modelo

Copie esta pasta inteira para `config/<nome-do-cliente>/` (letras minúsculas, sem espaço) e
preencha cada arquivo. O motor não produz nada sem config: é ela que diz quem é a marca, como
ela fala, o que já foi publicado e o que funciona.

| Arquivo | O que vai nele | O motor usa em |
|---|---|---|
| `perfil.md` | quem é a marca, público, StoryBrand, quem aprova, canais, skills plugadas | todas as estações |
| `voz.md` | tom, vocabulário, proibições | estação 4 e `check_voz.py` |
| `formatos.md` | o que funciona, medido, com data de apuração | estação 7 e `check_entrega.py` |
| `provas.md` | números, cases e depoimentos liberados para citar | estação 4 |
| `marca.md` | cores, fontes, regras visuais, pipeline de cards | estações 6 e 7 |
| `biblioteca.md` | temas já trabalhados e fontes da área | estações 0 e 3 |
| `paths.json` | pastas do acervo, produção, tópicos e Diário de Bordo | ferramentas |
| `Diario-de-Bordo.md` | lições "Não repetir" e o log de cada entrega | estações 0 e 8 |

Caminhos no `paths.json` podem ser relativos: eles são lidos a partir desta pasta.
