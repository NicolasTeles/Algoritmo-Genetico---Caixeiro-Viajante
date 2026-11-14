# Algoritmo Genético para o Problema do Caixeiro Viajante

Implementação em Python de um algoritmo genético que procura a rota de menor custo para o **Problema do Caixeiro Viajante** (visitar todas as cidades uma única vez e voltar à cidade inicial). O grafo é lido de um arquivo `.gml`, com o custo de cada trecho no atributo `peso`.

Trabalho da disciplina de **Grafos** (UFSJ), desenvolvido em dupla.

## Autores

- Miguel de Assis Viveiros
- Nicolas Teles

## Como funciona

Cada **indivíduo** é uma rota: uma permutação das cidades, com a primeira repetida no fim para fechar o ciclo. O **custo** de um indivíduo é a soma dos pesos dos trechos da rota. A cada geração:

1. **Elitismo:** as rotas são ordenadas pelo custo e metade da população (as melhores) é mantida.
2. **Seleção:** dois pais são sorteados entre as rotas da elite.
3. **Crossover:** um trecho do primeiro pai é copiado para o filho, e as cidades restantes são preenchidas na ordem em que aparecem no segundo pai, sem repetir cidades.
4. **Mutação:** com uma certa probabilidade, duas cidades da rota trocam de posição.
5. Os filhos completam a população até o tamanho original.

Ao final das gerações, o programa imprime a melhor rota encontrada e o seu custo.

## Parâmetros

Definidos no início de `AG.py`:

| Constante | Valor | Significado |
|---|---|---|
| `POPULATION_SIZE` | 150 | Tamanho da população |
| `ELITE_PERCENTAGE` | 0,5 | Fração da população que forma a elite |
| `NUMBER_OF_GENERATIONS` | 500 | Número de gerações |
| `MUTATION_CHANCE` | 0,1 | Probabilidade de mutação de cada filho |

## Como executar

Requisitos: Python 3 e a biblioteca `networkx`.

```
pip install networkx
python AG.py
```

O programa lê o arquivo `PCV.gml`, que precisa estar na mesma pasta.

## Formato do grafo

O grafo deve ser **completo** (existe um trecho entre cada par de cidades) e cada trecho deve ter o atributo `peso`. Exemplo (`PCV.gml`, com 5 cidades):

```
graph [
  directed 0
  node [ id 1 label 1 ]
  node [ id 2 label 2 ]
  ...
  edge [ source 1 target 2 peso 2 ]
  edge [ source 1 target 3 peso 7 ]
  ...
]
```

## Resultado no exemplo

No grafo de exemplo, o custo mínimo é 18, confirmado por força bruta (rota 1 → 2 → 3 → 5 → 4 → 1). O algoritmo genético encontrou esse custo em todas as 15 execuções de teste.

## Limitações conhecidas

- O grafo de exemplo é muito pequeno (5 cidades). O comportamento em instâncias maiores não foi avaliado.
- Na seleção dos pais, a probabilidade de cada rota da elite é proporcional ao seu **custo**. Como o objetivo é minimizar o custo, isso favorece, dentro da elite, as rotas piores. O correto seria usar uma probabilidade inversamente proporcional ao custo.
- Não há semente aleatória fixa, então os resultados podem variar entre execuções.
