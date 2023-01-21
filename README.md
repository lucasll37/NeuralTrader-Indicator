# NeuralTrader-Indicator

Este é um projeto de indicador gráfico que utiliza Inteligência Artificial para tentar prever o comportamento de ativos no curtíssimo prazo

[![Vídeo descritivo](https://img.youtube.com/vi/kHevGWlsoNo/0.jpg)](https://www.youtube.com/watch?v=kHevGWlsoNo)

## Descrição das pastas e arquivos

**data**: contém os dados para treinamento, teste e inferência e ainda recebe uma planilha gerada ao fim do treinamento com as métricas obtidas por candle ao fim da validação.

**graphics**: contém os gráficos gerados com a massa de dados de validação após a inferência.

**logs**: logs gerados pelo tensorflow de métricas do treinamento. Devem ser consultadas através do tensorboar com o comando:

    `tensorboard --logdir ./logs`

**saveModel**: contém os pesos do modelo pré-treinado.

**saveModel/tmp**: pasta destinada para o armazenamento temporário dos checkpoints que ocorrem ao longo do treinamento.

**src**: Código Fonte

- callbacks: configuração dos callbacks de treinamento
- checkGPU: função utilitáro que verifica a integração das bibliotecas com a GPU
- dataWrangling: pacote de funçãos destinadas ao remodelamento dos dados
- downloadData: destinado ao download dos dados
- graphicTrain: contém função destinada a geração dos gráficos
- model: Modelo preditivo
- mt5: API para comunicação com o homebroker MetaTrader5
- optimizers: configuração dos otimizadores de treinamento
- train: arquivo principal do treinamento. gerencia depois funcionalidades
- trainerModel: módulo de treinamento que abstrai as especificidades do framework de treinamento
- utils: funções utilitárias
- variable: variáveis de configuração

## Principais variáveis de configuração

- `trainCandles`: quantidade de candles utilizados ao todo para treino, teste e validação.
- `seed`: semente de criação de variáveis eleatórias.
- `selection`: ativa modo de seleção para minimizar a carga de geração de gráficos de acordo com os critérios (`CoefAngInf`, `CoefAngSup`, `maxIndLucas`, `minModDelta`).
- `graphic`: habilita a geração de gráficos.
- `account`: define a qual conta do MetaTrader5 acessar (previamente cadastradas em `./src/.env`).
- `stepsShow`: define a quantidade de candles de previsão serão mostrados (por padrão é o mesmo número de candles que o algoritmo utiliza pra a previsão).
- `useSaveModel`: define se o modelo será retreinado a partir de pesos aleatórios ("do zero") ou se será utilizado um modelo já treinado. por padrão, o indicador gráfico utiliza o modelo já treinado. A depender da configuração do seu computador, o treinamento por ser computacionamente exaustivamente.

## Modo de operação

### Escolha a fonte dos dados:

1º Opção)
Utilizar para o treinamento os dados fornecidos na pasta data (`downloadData = False`)

2º Opção)
Utilizar API MetaTrader5 para obtenção dos dados (`downloadData = True`) (permite maior controle para escolha de ativos e períodos)

Para isso, crie uma cópia do arquivo `.env.example` no mesmo local do diretório do arquivo original e renomei-o para `.env`, preenchendo os campos de credenciais da sua conta. Para maiores detalhes, consulte a [documentação oficial](https://www.mql5.com/pt/docs) da plataforma.

### Configure o ambiente

Com o terminal aberto no diretório raiz do projeto, siga os passos:

Feita essa escolha e estando num ambiente configurado com `Python 3.9.x`, execute o seguinte comando para o download das dependências:
`pip install -r ./requirements.txt`

A relação nominal das dependências pode ser consultada no arquivo `requirements.txt`

### Executar aplicação

Execute o comando:

`python ./src/train.py`

Ao término do processamento, será criado:

- pasta `./graphics/train`: uma subpasta com gráficos de inferência do indicador gráfico.
- pasta `./data`: Planilha de excel com as métricas obtidas por candle ao fim da validação.
