import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import warnings

warnings.filterwarnings("ignore")

corpus = [
    'Gostaria de ver o cardápio por favor',   # Cardapio
    'Cardápio por favor',                     # Cardapio
    'Quais comidas são servidas?',            # Cardapio
    'Me passa o cardápio',                    # Cardapio
    'Quais as opções de comida?',             # Cardapio
    'Quais bebidas tem?',                     # Cardapio
    'Quais pratos tem?',                      # Cardapio
    'Quero um Rodízio',                       # Pedido
    'Quero dois Rodízios',                    # Pedido
    'Quero Isca de Peixe',                    # Pedido
    'Vou querer Isca de Peixe',               # Pedido
    'Vou ficar com um Peixe à Urucum',        # Pedido
    'Quero um Peixe à Camponesa',             # Pedido
    'Faz um Supremo de Peixe por favor',      # Pedido
    'Faz um Peixe Frito fazendo o favor',     # Pedido
    'Vou querer uma Costela de Pacu Frito',   # Pedido
    'Faz um Peixe Suplício',                  # Pedido
    'Gostaria de um Peixe com Legumes',       # Pedido
    'Me vê um Peixe a Moda da Casa',          # Pedido
    'Quero um Peixe à Milanesa',              # Pedido
    'Vou querer um Peixe ao Purê',            # Pedido
    'Quero uma Moqueca de Peixe',             # Pedido
    'Vou querer um Peixe à Baiana',           # Pedido
    'Hoje eu quero um Peixe à Escabeche',     # Pedido
    'Vou ficar com um Peixe a Karague',       # Pedido
    'Quero um Pintado ao Molho Oriental',     # Pedido
    'Vou querer um Camarão Frito à Milanesa', # Pedido
    'Quero um Salmão Grelhado',               # Pedido
    'Manda pra mim um Salmão Grelhado',       # Pedido
    'Manda um Bolinho de Bacalhau',           # Pedido
    'Quero um Sashimi de Salmão',             # Pedido
    'Hoje vou querer Filé a Cavalo',          # Pedido
    'Vou querer um Filé à Francesa',          # Pedido
    'Quero um Filé a Suplício',               # Pedido
    'Gostaria de pedir um Frango à Milanesa', # Pedido
    'Quero pedir um Frango a Mato Grosso',    # Pedido
    'Quero um Frango à Califórnia',           # Pedido
    'Gostaria de um Frango a Passarinho',     # Pedido
    'Vou querer uma Água Tônica',             # Pedido
    'Vou beber uma Água Mineral',             # Pedido
    'Quero tomar um Guaraná',                 # Pedido
    'Quero tomar uma Soda Limonada',          # Pedido
    'Vê pra mim uma Coca bem gelada',         # Pedido
    'Me traz uma Coca diet',                  # Pedido
    'Vou tomar uma Fanta',                    # Pedido
    'Vou beber uma Citrus',                   # Pedido
    'Vou tomar uma H2O e duas cocas',         # Pedido
    'Quero 2 Cervejas',                       # Pedido
    'Quero uma Cerveja Long Neck',            # Pedido
    'Vou beber uma Caipira Vodka',            # Pedido
    'Vou beber uma Caipira Pinga',            # Pedido
    'Quero beber uma Caipira Steinhager',     # Pedido
    'Quero tomar Vodka e Pinga',              # Pedido
    'Me traz uma Pinga',                      # Pedido
    'Vou beber Salinas',                      # Pedido
    'Vou querer tomar uma Seleta',            # Pedido
    'Vou tomar uma Ypioca',                   # Pedido
    'Quero uma Campari',                      # Pedido
    'Vou beber uma San Raphael',              # Pedido
    'Vou tomar uma San Francisco',            # Pedido
    'Me traz um Martini Seco',                # Pedido
    'Quero beber um Martini Doce',            # Pedido
    'Quero tomar duas Steinhager',            # Pedido
    'Quero experimentar um Natu Mobilis',     # Pedido
    'Hoje to afim de beber um Jonny Walker Red', #Pedido
    'Hoje vou tomar um Jonny Walker Black',   # Pedido
    'Vou tomar um Conhaque Domeq',            # Pedido
    'Me traz um Licor Cointreau',             # Pedido
    'Pode trazer a conta por favor',          # Conta
    'Gostaria de pagar a conta',              # Conta
    'Me ve a conta por favor',                # Conta
    'Traz a conta por favor',                 # Conta
    'Vou querer a conta por favor',           # Conta
    'Pode trazer a conta',                    # Conta
    'Terminei por hoje, me traz a conta',     # Conta
    'ver a conta',                            # Conta
    'Bom dia, tudo bem?',                     # Saudação
    'Boa tarde, como vai você?',               # Saudação
    'Boa noite, queria fazer um pedido',      # Saudação
    'Bom dia, como vai você?',                # Saudação
    'Eae beleza?',                            # Saudação
    'eae, tranquilo?',                        # Saudação
    'Ola, Como você está?',                   # Saudação
    'Olá, como vai você?',                    # Saudação
    'Oi, como você ta?',                      # Saudação
    'eae como vc ta?',                        # Saudação
    'Salve, tranquilidade?',                  # Saudação
    'Eae mano, suave na nave?',               # Saudação
    'Oi, bão?',                               # saudação
    'oi, tudo bem?',                          # Saudação
    'Boa tarde, gostaria de fazer um pedido', # Saudação
    'Boa tarde tudo bem?',                    # Saudação
    'Ola',                                    # Saudação
    'Somente isso',                           # Despedida
    'vlw flw',                                # Despedida
    'Tchau',                                  # Despedida
    'fica com deus',                          # Depedida
    'Flw',                                    # Despedida
    'Até logo',                               # Despedida
    'Até mais',                               # Despedida
    'tchau',                                  # Despedida
    'Adiós',                                  # Despedida
    'Adeus',                                  # Despedida
    'Bye bye',                                # Despedida
]

classes = [
    'cardapio', 
    'cardapio', 
    'cardapio', 
    'cardapio', 
    'cardapio', 
    'cardapio', 
    'cardapio',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'pedido',
    'conta',
    'conta',
    'conta',
    'conta',
    'conta',
    'conta',
    'conta',
    'conta',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'saudacao',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida',
    'despedida'
]



def treinar_knn():
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,strip_accents='unicode')

    model = KNeighborsClassifier(n_neighbors=1, weights='uniform')

    X = np.array(corpus)
    Y = np.array(classes)
    X = vectorizer.fit_transform(X)
    model.fit(X,Y)

    return model, vectorizer