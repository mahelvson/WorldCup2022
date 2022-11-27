# WorldCup2022
Repositório criado para o desafio SigmaGeek / ReiDoPitaco.com por Mahelvson B. Chaves

## Ideia principal
Criei este repositório para o desafio SigmaGeek utilizei alguns datasets disponíveis no Kaggle, bem como realizei alguns scraps para criar meu próprio dataset para a competição. Nas seções a seguir estão descritas um pouco mais detalhadamente as ideias empregadas. O projeto envolvia a previsão do placar dos jogos da primeira fase da Copa do Mundo de Futebol Masculino de 2022.

Os datasets foram construídos de forma que dispusessem dados referentes as copas de 1994 - 2018. Considerei que um passado muito distante a este horizonte já não reflete tão bem a dinâmica do futebol. Algumas discussões e inspirações deste trabalho foram retiradas do livro "Soccernomics" de Kuper e Szymanski.

## Dataset FIFA Ranking (./datasets/fifa_rakning_before_wc.csv)
Para construir este dataset, fiz um scrapper que verificava o último release de ranking oficial FIFA antes da copa. Com base nesta regra, associei um ranking FIFA a cada copa desde 1994 até 2022.

Fonte: https://www.fifa.com/fifa-world-ranking/men?dateId=id13792

## Dataset ELO Ratings (./datasets/elo_rating.csv)
Para construir este dataset, utilizei uma ideia similar ao dataset FIFA Ranking e scrapei o elo ratings anual para cada ano anterior ao da copa. Por exemplo, a copa de 1994 teve associada o rating do ano 1993, já a copa de 1998, teve o rating de 1997 associado. Esta abordagem foi necessária para compatibilizar os períodos em que ocorrem as copas com o calendário de release do rating.

Fonte: www.eloratings.net

## Dataset WorldBank (./datasets/WorldBankData_raw.csv)
A ideia deste dataset foi retirar variáveis econômicas dos países que possuem relação com o futebol. As variáveis foram população, PIB e renda per capta e a explicação para esta abordagem foi a regressão feita para o Handicap feita no livro do Soccernomics. Este dataset foi retirado do DataBank do World Bank.

Fonte: https://databank.worldbank.org

## Dataset para Qatar, Canada e Gales (./datasets/synth_data.csv)
Estas três seleções não possuem registros de partidas no período que analisei os dados, então utilizei um dataset que possuia uma coletânea de partidas internacionais. Na solução final, empreguei apenas partidas que valeram por copas do mundo, exceto para estes três países. Chamei este dataset de "sintético" 

## Datasets Kaggle
Utilizei alguns datasets do kaggle para compor o dataset final. O principal dataset (./datasets/WorldCupDatasets_raw.csv) possuia os dados necessários das copas 1993 até 2014. Para não perder este período mais recente, utilizei uma outra fonte que tinha os registros da copa de 2018 e possuia as mesmas informações das partidas (./datasets/2018_worldcup_v3.csv). E por fim, para criar o template da submissão, utilizei um csv com os dados das partidas da primeira fase da Copa de 2022 (./datasets/2022_world_cup_22.csv).

## Dataset Final
O dataset final está disponível na pasta ./datasets/final_dataset/

## Machine Learning
Utilizei uma estratégia de regressão para os scores dos dois times para cada partida, aplicando o algoritmo XGBRegressor. A Copa de 2018 serviu como validação e os resultados indicam uma precisão na previsão do vencedor de ˜50%. A ideia principal do desafio era a previsão do resultado em tremos de vitória ou empate, e o placar seria o critério de desempate. Testei uma regressão agnóstica em relação aos nomes das equipes, mas o resultado não foi muito diferente do obtido para a versão que utilizei one hot encoding para o nome dos times.

## Conclusões
Não considerei o desempenho tão bom, mas para o que possuia em mãos o prazo para solução, foi um bom exercício, além de ter aprendido muita coisa sobre as copas, países, culturas e história dos países. Eu entendi que o comportamento das seleções durante a Copa do Mundo é diferente dos demais torneios, e portanto optei por utilizar apenas os dados destes torneios, mas existem databases de diversas partidas entre seleções, que podem ser utilizadas para tentar melhorar o resultado final.
