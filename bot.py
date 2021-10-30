from knn import treinar_knn
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
from random import randrange

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "9999999999:AAAAAAAAAAbbbbbbbbbbCCCCCCCCCCeeeee"
MODEL, VECTORIZER = treinar_knn()

CARDAPIO = {
    'bebida':[
        {'nome':'suco de laranja', 'preco': 'R$   8,00'},
        {'nome':'suco de acerola', 'preco': 'R$   8,00'},
        {'nome':'suco de abacaxi', 'preco': 'R$   8,00'},
        {'nome':'suco de goiaba', 'preco': 'R$   8,00'},
        {'nome':'suco de cajú', 'preco': 'R$   8,00'},
        {'nome':'suco de maracujá', 'preco': 'R$   8,00'},
        {'nome':'suco de uva', 'preco': 'R$   8,00'},
        {'nome':'suco de morango', 'preco': 'R$   8,00'},
        {'nome':'suco de limão', 'preco': 'R$   8,00'},
        {'nome':'água mineral', 'preco': 'R$   5,80'},
        {'nome':'água tônica', 'preco': 'R$   5,80'},
        {'nome':'guaraná', 'preco': 'R$   5,80'},
        {'nome':'soda limonada', 'preco': 'R$   5,80'},
        {'nome':'coca-cola', 'preco': 'R$   5,80'},
        {'nome':'fanta', 'preco': 'R$   5,80'},
        {'nome':'h2o', 'preco': 'R$   5,80'},
        {'nome':'citrus', 'preco': 'R$   5,80'},
        {'nome':'cerveja', 'preco': 'R$  13,90'}
    ],

    'prato':[
        {'nome': 'rodízio de peixe', 'preco': 'R$  95,90'},
        {'nome': 'isca de peixe', 'preco':'R$ 103,10'},
        {'nome': 'peixe à urucum', 'preco':'R$ 103,10'},
        {'nome': 'peixe à camponesa', 'preco':'R$ 103,10'},
        {'nome': 'supremo de peixe', 'preco':'R$ 103,10'},
        {'nome': 'peixe frito', 'preco':'R$ 103,10'},
        {'nome': 'peixe suplício', 'preco':'R$ 103,10'},
        {'nome': 'peixe com legumes', 'preco':'R$ 103,10'},
        {'nome': 'peixe à milanesa', 'preco':'R$ 103,10'},
        {'nome': 'peixe ao purê', 'preco':'R$ 103,10'},
        {'nome': 'moqueca de peixe', 'preco':'R$ 103,10'},
        {'nome': 'peixe à baiana', 'preco':'R$ 103,10'},
        {'nome': 'peixe à escabeche', 'preco':'R$ 103,10'},
        {'nome': 'peixe a karague', 'preco':'R$ 103,10'},
        {'nome': 'sashimi de salmão', 'preco':'R$ 103,10'},
        {'nome': 'salmão grelhado', 'preco':'R$ 103,10'},
        {'nome': 'camarão frito', 'preco':'R$ 103,10'}
    ]
}


ETIQUETAS = {
    'bebida': [
        {'nome': 'suco de laranja', 'valor': 'suco de laranja'},
        {'nome': 'suco laranja', 'valor': 'suco de laranja'},
        {'nome': 'suco de laraja', 'valor': 'suco de laranja'},
        {'nome': 'suco d laranja', 'valor': 'suco de laranja'},
        {'nome': 'suco d Laranja', 'valor': 'suco de laranja'},
        {'nome': 'SUCO DE LARANJA', 'valor': 'suco de laranja'},
        {'nome': 'SUCO D LARANA', 'valor': 'suco de laranja'},
        {'nome': 'Suco de Laranja', 'valor': 'suco de laranja'},
        {'nome': 'suco de Laranja', 'valor': 'suco de laranja'},
        {'nome': 'sucos de laranja', 'valor': 'suco de laranja'},
        {'nome': 'Sucos de laranja', 'valor': 'suco de laranja'},
        {'nome': 'sucod e laranja', 'valor': 'suco de laranja'},
        {'nome': 'suco de raranja', 'valor': 'suco de laranja'},
        {'nome': 'Suco de Raranja', 'valor': 'suco de laranja'},
        {'nome': 'suco de Laran ja', 'valor': 'suco de laranja'},
        {'nome': 'sucos de lalanja', 'valor': 'suco de laranja'},
        {'nome': 'sucos de lalanj', 'valor': 'suco de laranja'},
        {'nome': 'sucos de laranj', 'valor': 'suco de laranja'},
        {'nome': 'suco de laranj', 'valor': 'suco de laranja'},
        {'nome': 'suco d elaranja', 'valor': 'suco de laranja'},
        {'nome': 'suco de acerola', 'valor': 'suco de acerola'},
        {'nome': 'suco acerola', 'valor': 'suco de acerola'},
        {'nome': 'SUCO DE ACEROLA', 'valor': 'suco de acerola'},
        {'nome': 'SUCO D ACEROLA', 'valor': 'suco de acerola'},
        {'nome': 'suco d acerola', 'valor': 'suco de acerola'},
        {'nome': 'Suco de Acerola', 'valor': 'suco de acerola'},
        {'nome': 'suco de Acerola', 'valor': 'suco de acerola'},
        {'nome': 'sucos de acerolas', 'valor': 'suco de acerola'},
        {'nome': 'sucos de acerola', 'valor': 'suco de acerola'},
        {'nome': 'SUCOS DE ACEROLA', 'valor': 'suco de acerola'},
        {'nome': 'SUCOS DE CEROLA', 'valor': 'suco de acerola'},
        {'nome': 'sucos de cerola', 'valor': 'suco de acerola'},
        {'nome': 'Sucos de acerola', 'valor': 'suco de acerola'},
        {'nome': 'Sucos de Acerolas', 'valor': 'suco de acerola'},
        {'nome': 'sucod de acerola', 'valor': 'suco de acerola'},
        {'nome': 'suco d eacerola', 'valor': 'suco de acerola'},
        {'nome': 'suco de arecola', 'valor': 'suco de acerola'},
        {'nome': 'suco de Acecola', 'valor': 'suco de acerola'},
        {'nome': 'suco de acorela', 'valor': 'suco de acerola'},
        {'nome': 'suco de cerola', 'valor': 'suco de acerola'},
        {'nome': 'suco de abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'SUCO DE ABACAXI', 'valor': 'suco de abacaxi'},
        {'nome': 'SUDO D ABACAXI', 'valor': 'suco de abacaxi'},
        {'nome': 'SUCO D ABACAXI', 'valor': 'suco de abacaxi'},
        {'nome': 'SUCOS DE ABACAXI', 'valor': 'suco de abacaxi'},
        {'nome': 'suco d abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'Suco de Abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco de Abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'sucos de abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'Sucos de abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'sucod e abacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco d eabacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco de abavaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'Suco de Abaxaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco de Acabaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'sucos de avacaxi', 'valor': 'suco de abacaxi'},
        {'nome': 'suco de uva', 'valor': 'suco de uva'},
        {'nome': 'suco uva', 'valor': 'suco de uva'},
        {'nome': 'SUCO D UVA', 'valor': 'suco de uva'},
        {'nome': 'SUCO DE UVA', 'valor': 'suco de uva'},
        {'nome': 'suco d uva', 'valor': 'suco de uva'},
        {'nome': 'Suco de Uva', 'valor': 'suco de uva'},
        {'nome': 'suco de Uva', 'valor': 'suco de uva'},
        {'nome': 'sucos de uva', 'valor': 'suco de uva'},
        {'nome': 'Sucos de uva', 'valor': 'suco de uva'},
        {'nome': 'sucod e uva', 'valor': 'suco de uva'},
        {'nome': 'suco d euva', 'valor': 'suco de uva'},
        {'nome': 'suco de vau', 'valor': 'suco de uva'},
        {'nome': 'suco de uba', 'valor': 'suco de uva'},
        {'nome': 'SUCOS DE UVA', 'valor': 'suco de abacaxi'},
        {'nome': 'suco de goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'suco goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'SUCO DE GOIAVA', 'valor': 'suco de goiaba'},
        {'nome': 'SUCO DE GOIABA', 'valor': 'suco de goiaba'},
        {'nome': 'SUCO D GOIAVA', 'valor': 'suco de goiaba'},
        {'nome': 'SUCO D GOIABA', 'valor': 'suco de goiaba'},
        {'nome': 'suco d goiava', 'valor': 'suco de goiaba'},
        {'nome': 'suco d goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'Suco de Goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'suco de Goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'sucos de goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'Sucos de goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'sucod e goiaba', 'valor': 'suco de goiaba'},
        {'nome': 'suco d egoiaba', 'valor': 'suco de goiaba'},
        {'nome': 'suco de  gaioba', 'valor': 'suco de goiaba'},
        {'nome': 'suco de gobaia', 'valor': 'suco de goiaba'},
        {'nome': 'suco de gobia', 'valor': 'suco de goiaba'},
        {'nome': 'suco de gobiai', 'valor': 'suco de goiaba'},
        {'nome': 'suco de maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'suco maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'SUCO DE MARACUJA', 'valor': 'suco de maracujá'},
        {'nome': 'SUCO D MARACUJA', 'valor': 'suco de maracujá'},
        {'nome': 'SUCO DE MARACUJÁ', 'valor': 'suco de maracujá'},
        {'nome': 'SUCO D MARACUJÁ', 'valor': 'suco de maracujá'},
        {'nome': 'suco d maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'suco d macurajá', 'valor': 'suco de maracujá'},
        {'nome': 'Suco de Maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'suco de Maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'sucos de maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'Sucos de maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'sucod e maracuja', 'valor': 'suco de maracujá'},
        {'nome': 'suco d emaracuja', 'valor': 'suco de maracujá'},
        {'nome': 'suco de maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'Suco de Maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'suco de Maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'sucos de maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'Sucos de maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'sucod e maracujá', 'valor': 'suco de maracujá'},
        {'nome': 'suco d emaracujá', 'valor': 'suco de maracujá'},
        {'nome': 'suco de macuraja', 'valor': 'suco de maracujá'},
        {'nome': 'suco de caju', 'valor': 'suco de cajú'},
        {'nome': 'suco caju', 'valor': 'suco de cajú'},
        {'nome': 'SUCO DE CAJU', 'valor': 'suco de cajú'},
        {'nome': 'SUCO D CAJU', 'valor': 'suco de cajú'},
        {'nome': 'SUCO DE CAJÚ', 'valor': 'suco de cajú'},
        {'nome': 'SUCO D CAJÚ', 'valor': 'suco de cajú'},
        {'nome': 'suco d cajú', 'valor': 'suco de cajú'},
        {'nome': 'Suco de Caju', 'valor': 'suco de cajú'},
        {'nome': 'suco de Caju', 'valor': 'suco de cajú'},
        {'nome': 'sucos de caju', 'valor': 'suco de cajú'},
        {'nome': 'Sucos de caju', 'valor': 'suco de cajú'},
        {'nome': 'sucod e caju', 'valor': 'suco de cajú'},
        {'nome': 'suco d ecaju', 'valor': 'suco de cajú'},
        {'nome': 'suco de juca', 'valor': 'suco de cajú'},
        {'nome': 'Suco de Cjau', 'valor': 'suco de cajú'},
        {'nome': 'suco de Cajú', 'valor': 'suco de cajú'},
        {'nome': 'sucos de cajú', 'valor': 'suco de cajú'},
        {'nome': 'Sucos de cají', 'valor': 'suco de cajú'},
        {'nome': 'sucod e cajó', 'valor': 'suco de cajú'},
        {'nome': 'suco d ecajú', 'valor': 'suco de cajú'},
        {'nome': 'suco de morango', 'valor': 'suco de morango'},
        {'nome': 'suco morango', 'valor': 'suco de morango'},
        {'nome': 'SUCO DE MORANGO', 'valor': 'suco de morango'},
        {'nome': 'SUCO D MORANGO', 'valor': 'suco de morango'},
        {'nome': 'suco d morango', 'valor': 'suco de morango'},
        {'nome': 'Suco de Morango', 'valor': 'suco de morango'},
        {'nome': 'suco de Morango', 'valor': 'suco de morango'},
        {'nome': 'sucos de morango', 'valor': 'suco de morango'},
        {'nome': 'Sucos de morango', 'valor': 'suco de morango'},
        {'nome': 'sucod e morango', 'valor': 'suco de morango'},
        {'nome': 'suco de ramongo', 'valor': 'suco de morango'},
        {'nome': 'suco de mogango', 'valor': 'suco de morango'},
        {'nome': 'suco de momango', 'valor': 'suco de morango'},
        {'nome': 'suco de morangu', 'valor': 'suco de morango'},
        {'nome': 'suco de limão', 'valor': 'suco de limão'},
        {'nome': 'suco limão', 'valor': 'suco de limão'},
        {'nome': 'suco limao', 'valor': 'suco de limão'},
        {'nome': 'SUCO DE LIMAO', 'valor': 'suco de limão'},
        {'nome': 'SUCO D LIMAO', 'valor': 'suco de limão'},
        {'nome': 'SUCO DE LIMÃO', 'valor': 'suco de limão'},
        {'nome': 'SUCO DE LIMOA', 'valor': 'suco de limão'},
        {'nome': 'suco de limoa', 'valor': 'suco de limão'},
        {'nome': 'SUCO D LIMÃO', 'valor': 'suco de limão'},
        {'nome': 'suco d limão', 'valor': 'suco de limão'},
        {'nome': 'Suco de Limão', 'valor': 'suco de limão'},
        {'nome': 'suco de Limão', 'valor': 'suco de limão'},
        {'nome': 'sucos de limão', 'valor': 'suco de limão'},
        {'nome': 'Sucos de limão', 'valor': 'suco de limão'},
        {'nome': 'sucod e limão', 'valor': 'suco de limão'},
        {'nome': 'suco d elimão', 'valor': 'suco de limão'},
        {'nome': 'suco de limao', 'valor': 'suco de limão'},
        {'nome': 'Suco de Limao', 'valor': 'suco de limão'},
        {'nome': 'suco de Limao', 'valor': 'suco de limão'},
        {'nome': 'sucos de limao', 'valor': 'suco de limão'},
        {'nome': 'Sucos de limao', 'valor': 'suco de limão'},
        {'nome': 'sucod e limao', 'valor': 'suco de limão'},
        {'nome': 'suco d elimao', 'valor': 'suco de limão'},
        {'nome': 'água tônica', 'valor': 'água tônica'},
        {'nome': 'AGUA TONICA', 'valor': 'água tônica'},
        {'nome': 'ÁGUA TÔNICA', 'valor': 'água tônica'},
        {'nome': 'agua tonica', 'valor': 'água tônica'},
        {'nome': 'agua tônica', 'valor': 'água tônica'},
        {'nome': 'Agua tonica', 'valor': 'água tônica'},
        {'nome': 'Agua tônica', 'valor': 'água tônica'},
        {'nome': 'Água tnica', 'valor': 'água tônica'},
        {'nome': 'agua tnica', 'valor': 'água tônica'},
        {'nome': 'agua t^nica', 'valor': 'água tônica'},
        {'nome': 'aga tonica', 'valor': 'água tônica'},
        {'nome': 'tonica', 'valor': 'água tônica'},
        {'nome': 'tônica', 'valor': 'água tônica'},
        {'nome': 'agua mineral', 'valor': 'água mineral'},
        {'nome': 'aga mineral', 'valor': 'água mineral'},
        {'nome': 'mineral', 'valor': 'água mineral'},
        {'nome': 'aguar minerar', 'valor': 'água mineral'},
        {'nome': 'miner', 'valor': 'água mineral'},
        {'nome': 'moneral', 'valor': 'água mineral'},
        {'nome': 'agua moneral', 'valor': 'água mineral'},
        {'nome': 'guaraná', 'valor': 'guaraná'},
        {'nome': 'guarana', 'valor': 'guaraná'},
        {'nome': 'guaranás', 'valor': 'guaraná'},
        {'nome': 'guaranas', 'valor': 'guaraná'},
        {'nome': 'GUARANÁ', 'valor': 'guaraná'},
        {'nome': 'GUARANÁS', 'valor': 'guaraná'},
        {'nome': 'garaná', 'valor': 'guaraná'},
        {'nome': 'garana', 'valor': 'guaraná'},
        {'nome': 'garanás', 'valor': 'guaraná'},
        {'nome': 'garanas', 'valor': 'guaraná'},
        {'nome': 'soda limonada', 'valor': 'soda limonada'},
        {'nome': 'sodas limonada', 'valor': 'soda limonada'},
        {'nome': 'SODA LIMONADA', 'valor': 'soda limonada'},
        {'nome': 'SODAS LIMONADA', 'valor': 'soda limonada'},
        {'nome': 'coca-cola', 'valor': 'coca-cola'},
        {'nome': 'COCA-COLA', 'valor': 'coca-cola'},
        {'nome': 'coquinha', 'valor': 'coca-cola'},
        {'nome': 'COQUINHA', 'valor': 'coca-cola'},
        {'nome': 'coca', 'valor': 'coca-cola'},
        {'nome': 'Coca-cola', 'valor': 'coca-cola'},
        {'nome': 'Coca-colas', 'valor': 'coca-cola'},
        {'nome': 'Coca-Cola', 'valor': 'coca-cola'},
        {'nome': 'Coca-Colas', 'valor': 'coca-cola'},
        {'nome': 'Cocas', 'valor': 'coca-cola'},
        {'nome': 'Coca', 'valor': 'coca-cola'},
        {'nome': 'cocas', 'valor': 'coca-cola'},
        {'nome': 'COCA', 'valor': 'coca-cola'},
        {'nome': 'COCAS', 'valor': 'coca-cola'},
        {'nome': 'coca-colas', 'valor': 'coca-cola'},
        {'nome': 'COCA-COLAS', 'valor': 'coca-cola'},
        {'nome': 'fanta', 'valor': 'fanta'},
        {'nome': 'fantas', 'valor': 'fanta'},
        {'nome': 'FANTA', 'valor': 'fanta'},
        {'nome': 'FANTAS', 'valor': 'fanta'},
        {'nome': 'fant', 'valor': 'fanta'},
        {'nome': 'Fanta', 'valor': 'fanta'},
        {'nome': 'citrus', 'valor': 'citrus'},
        {'nome': 'citros', 'valor': 'citrus'},
        {'nome': 'Citrus', 'valor': 'citrus'},
        {'nome': 'CITRUS', 'valor': 'citrus'},
        {'nome': 'ctrus', 'valor': 'citrus'},
        {'nome': 'citrs', 'valor': 'citrus'},
        {'nome': 'citurs', 'valor': 'citrus'},
        {'nome': 'citru', 'valor': 'citrus'},
        {'nome': 'citro', 'valor': 'citrus'},
        {'nome': 'h2o', 'valor': 'h2o'},
        {'nome': 'H2O', 'valor': 'h2o'},
        {'nome': 'h2', 'valor': 'h2o'},
        {'nome': 'H2', 'valor': 'h2o'},
        {'nome': 'h20', 'valor': 'h2o'},
        {'nome': 'cerveja', 'valor': 'cerveja'},
        {'nome': 'Cerveja', 'valor': 'cerveja'},
        {'nome': 'ceveja', 'valor': 'cerveja'},
        {'nome': 'cevecinha', 'valor': 'cerveja'},
        {'nome': 'CERVEJA', 'valor': 'cerveja'},
        {'nome': 'cervejas', 'valor': 'cerveja'},
        {'nome': 'Cervejas', 'valor': 'cerveja'},
        {'nome': 'CERVEJAS', 'valor': 'cerveja'},
    ],

    'prato': [
        {'nome': 'rodizio', 'valor': 'rodízio de peixe'},
        {'nome': 'rodixio', 'valor': 'rodízio de peixe'},
        {'nome': 'rodisio', 'valor': 'rodízio de peixe'},
        {'nome': 'rodísio', 'valor': 'rodízio de peixe'},
        {'nome': 'rodízio', 'valor': 'rodízio de peixe'},
        {'nome': 'RODIZIO', 'valor': 'rodízio de peixe'},
        {'nome': 'RODÍZIO', 'valor': 'rodízio de peixe'},
        {'nome': 'RODÍZIOS', 'valor': 'rodízio de peixe'},
        {'nome': 'RODIZIOS', 'valor': 'rodízio de peixe'},
        {'nome': 'rodízios', 'valor': 'rodízio de peixe'},
        {'nome': 'rodizios', 'valor': 'rodízio de peixe'},
        {'nome': 'rodízio de peixe', 'valor': 'rodízio de peixe'},
        {'nome': 'rodizio de peixe', 'valor': 'rodízio de peixe'},
        {'nome': 'rodisio de peixe', 'valor': 'rodízio de peixe'},
        {'nome': 'RODÍZIO DE PEIXE', 'valor': 'rodízio de peixe'},
        {'nome': 'Rodízio de Peixe', 'valor': 'rodízio de peixe'}, 
        {'nome': 'rodízio de peixes','valor': 'rodízio de peixe'},
        {'nome': 'RODISIO de PEixes','valor': 'rodízio de peixe'},
        {'nome': 'rodiizio de pexe', 'valor': 'rodízio de peixe'},
        {'nome': 'isca de peixe', 'valor': 'isca de peixe'},
        {'nome': 'isca de pexe', 'valor': 'isca de peixe'},
        {'nome': 'iscas de pexe', 'valor': 'isca de peixe'},
        {'nome': 'Isca de pexe', 'valor': 'isca de peixe'},
        {'nome': 'Iscas de pexe', 'valor': 'isca de peixe'},
        {'nome': 'iscas de peixe', 'valor': 'isca de peixe'},
        {'nome': 'Isca de Peixe', 'valor': 'isca de peixe'},
        {'nome': 'Iscas de peixe', 'valor': 'isca de peixe'},
        {'nome': 'ISCA DE PEIXE', 'valor': 'isca de peixe'},
        {'nome': 'IscA de Pexe', 'valor': 'isca de peixe'},
        {'nome': 'ixca de peixe', 'valor': 'isca de peixe'},
        {'nome': 'ISCA De Peixe', 'valor': 'isca de peixe'},
        {'nome': 'Isca De Peixe', 'valor': 'isca de peixe'},
        {'nome': 'isca', 'valor': 'isca de peixe'},
        {'nome': 'iscas', 'valor': 'isca de peixe'},
        {'nome': 'peixe à urucum', 'valor': 'peixe à urucum'},
        {'nome': 'Pexe à urucum', 'valor': 'peixe à urucum'},
        {'nome': 'Pexe a urucum', 'valor': 'peixe à urucum'},
        {'nome': 'pexe a urucum', 'valor': 'peixe à urucum'},
        {'nome': 'pexe à urucum', 'valor': 'peixe à urucum'},
        {'nome': 'peixe a urucum', 'valor': 'peixe à urucum'},
        {'nome': 'peixe a urucun', 'valor': 'peixe à urucum'},
        {'nome': 'Peixe à Urucum', 'valor': 'peixe à urucum'},
        {'nome': 'PEIXE à uruCum', 'valor': 'peixe à urucum'},
        {'nome': 'Pexe a urucum', 'valor': 'peixe à urucum'},
        {'nome': 'peixe À Urucum', 'valor': 'peixe à urucum'},
        {'nome': 'PEixe à uRucum', 'valor': 'peixe à urucum'},
        {'nome': 'urucum', 'valor': 'peixe à urucum'},
        {'nome': 'urucun', 'valor': 'peixe à urucum'},
        {'nome': 'pexe à canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'Pexe à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixe à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'pexe à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'pexe a camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'Peixe a camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixe a canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixes a canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixes a camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixes à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'PEIXES a canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'PEIXES à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixe a canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'peixe à canponeza', 'valor': 'peixe à camponesa'},
        {'nome': 'PeiXe à camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'Pexe a canponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'PEIXE À CAMPONESA', 'valor': 'peixe à camponesa'},
        {'nome': 'peixe à CamPOnesa', 'valor': 'peixe à camponesa'},
        {'nome': 'camponesa', 'valor': 'peixe à camponesa'},
        {'nome': 'camponeaa', 'valor': 'peixe à camponesa'},
        {'nome': 'supremo de peixe', 'valor': 'supremo de peixe'},
        {'nome': 'supremo de pexe', 'valor': 'supremo de peixe'},
        {'nome': 'Supremo de pexe', 'valor': 'supremo de peixe'},
        {'nome': 'supremos de peixe', 'valor': 'supremo de peixe'},
        {'nome': 'SUPREMOS', 'valor': 'supremo de peixe'},
        {'nome': 'Supremo De Peixe', 'valor': 'supremo de peixe'},
        {'nome': 'SUPREMO DE PEIXE', 'valor': 'supremo de peixe'},
        {'nome': 'supremo De peiXe', 'valor': 'supremo de peixe'},
        {'nome': 'SUPREMO de peixe', 'valor': 'supremo de peixe'},
        {'nome': 'supremo de Peixe', 'valor': 'supremo de peixe'},
        {'nome': 'supemo de peixe', 'valor': 'supremo de peixe'},
        {'nome': 'Supreemo de peixe', 'valor': 'supremo de peixe'},
        {'nome': 'supremo', 'valor': 'supremo de peixe'},
        {'nome': 'suprema', 'valor': 'supremo de peixe'},
        {'nome': 'peixe frito', 'valor': 'peixe frito'},
        {'nome': 'pexe frito', 'valor': 'peixe frito'},
        {'nome': 'Pexe frito', 'valor': 'peixe frito'},
        {'nome': 'Pexes frito', 'valor': 'peixe frito'},
        {'nome': 'Pexes fritos', 'valor': 'peixe frito'},
        {'nome': 'peixes fritos', 'valor': 'peixe frito'},
        {'nome': 'PEIXES FRITOS', 'valor': 'peixe frito'},
        {'nome': 'Peixe Frito', 'valor': 'peixe frito'},
        {'nome': 'peixe fito', 'valor': 'peixe frito'},
        {'nome': 'PEIXE FRITO', 'valor': 'peixe frito'},
        {'nome': 'pEixe frito', 'valor': 'peixe frito'},
        {'nome': 'peixe frIto', 'valor': 'peixe frito'},
        {'nome': 'pWIxe frit0', 'valor': 'peixe frito'},
        {'nome': 'peix frito', 'valor': 'peixe frito'},
        {'nome': 'peixe com legumes','valor':'peixe com legumes'},
        {'nome': 'pexe c legume','valor':'peixe com legumes'},
        {'nome': 'pexe com legume','valor':'peixe com legumes'},
        {'nome': 'Pexe com legumes','valor':'peixe com legumes'},
        {'nome': 'Pexe c legume','valor':'peixe com legumes'},
        {'nome': 'pexe c legumes','valor':'peixe com legumes'},
        {'nome': 'pexe com legumes','valor':'peixe com legumes'},
        {'nome': 'peixes com legumes','valor':'peixe com legumes'},
        {'nome': 'peixe con legume', 'valor':'peixe com legumes'},
        {'nome': 'peix com legume','valor':'peixe com legumes'},
        {'nome': 'PEIXE COM LEGUMES','valor':'peixe com legumes'},
        {'nome': 'peixe COM legumes', 'valor':'peixe com legumes'},
        {'nome': 'PEIxe com Legumes', 'valor':'peixe com legumes'},
        {'nome': 'peixe CoM Legumes', 'valor':'peixe com legumes'},
        {'nome': 'peixe com legume', 'valor':'peixe com legumes'},
        {'nome': 'peixe suplício', 'valor': 'peixe suplício'},
        {'nome': 'pexe suplicio', 'valor': 'peixe suplício'},
        {'nome': 'pexe sup', 'valor': 'peixe suplício'},
        {'nome': 'pexe suplício', 'valor': 'peixe suplício'},
        {'nome': 'Pexe suplício', 'valor': 'peixe suplício'},
        {'nome': 'peixes suplicio', 'valor': 'peixe suplício'},
        {'nome': 'peixe suplicios', 'valor': 'peixe suplício'},
        {'nome': 'Peixe Suplicio', 'valor': 'peixe suplício'},
        {'nome': 'PEIXE SUPLÍCIO', 'valor': 'peixe suplício'},
        {'nome': 'peize Suplicio',  'valor': 'peixe suplício'},
        {'nome': 'peixe c0m suplicio',  'valor': 'peixe suplício'},
        {'nome': 'PeIxe CoM Suplicio',  'valor': 'peixe suplício'},
        {'nome': 'suplício', 'valor': 'peixe suplício'},
        {'nome': 'suplicio', 'valor': 'peixe suplício'},
        {'nome': 'SUPLÍCIO', 'valor': 'peixe suplício'},
        {'nome': 'SUPLICIO', 'valor': 'peixe suplício'},
        {'nome': 'peixe suplício', 'valor': 'peixe suplício'},
        {'nome': 'peixe suplício', 'valor': 'peixe suplício'},
        {'nome': 'peixe à milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'pexe à milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'Pexe a milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'Pexe à milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'pexe milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'pexe a milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'peixe a milaneza', 'valor': 'peixe à milanesa'},
        {'nome': 'peixe á Milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'peixes a milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'PEIXE à milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'peixe a mILAnesa', 'valor': 'peixe à milanesa'},
        {'nome': 'peixe a milanesas', 'valor': 'peixe à milanesa'},
        {'nome': 'PEIXE À MILANESA', 'valor': 'peixe à milanesa'},
        {'nome': 'milanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'amilanesa', 'valor': 'peixe à milanesa'},
        {'nome': 'peixe ao purê', 'valor': 'peixe ao purê'},
        {'nome': 'Pexe ao pure', 'valor': 'peixe ao purê'},
        {'nome': 'pexe ao pure', 'valor': 'peixe ao purê'},
        {'nome': 'Pexe ao purê', 'valor': 'peixe ao purê'},
        {'nome': 'pexe ao purê', 'valor': 'peixe ao purê'},
        {'nome': 'peixe ao pure', 'valor': 'peixe ao purê'},
        {'nome': 'peixe no puré', 'valor': 'peixe ao purê'},
        {'nome': 'PEIxe ao purê', 'valor': 'peixe ao purê'},
        {'nome': 'peixe com purê', 'valor': 'peixe ao purê'},
        {'nome': 'peixe e purê', 'valor': 'peixe ao purê'},
        {'nome': 'peixe a purê', 'valor': 'peixe ao purê'},
        {'nome': 'peix ao pure', 'valor': 'peixe ao purê'},
        {'nome': 'peixe a pure', 'valor': 'peixe ao purê'},
        {'nome': 'peixe a purê', 'valor': 'peixe ao purê'},
        {'nome': 'pexe a purê', 'valor': 'peixe ao purê'},
        {'nome': 'pexe a pure', 'valor': 'peixe ao purê'},
        {'nome': 'peixe com pure', 'valor': 'peixe ao purê'},
        {'nome': 'peixe com purê', 'valor': 'peixe ao purê'},
        {'nome': 'moqueca de peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca d pexe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca de pexe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca d peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca de peixes', 'valor': 'moqueca de peixe'},
        {'nome': 'moqeca de peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'Moqueca de peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'Moqueca d Peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueCaa de peix', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca di peixe', 'valor': 'moqueca de peixe'},
        {'nome': 'moqueca', 'valor': 'moqueca de peixe'},
        {'nome': 'Moqueca', 'valor': 'moqueca de peixe'},
        {'nome': 'muqueca', 'valor': 'moqueca de peixe'},
        {'nome': 'peixe à baiana', 'valor': 'peixe à baiana'},
        {'nome': 'Pexe a baiana', 'valor': 'peixe à baiana'},
        {'nome': 'Pexe à baiana', 'valor': 'peixe à baiana'},
        {'nome': 'pexe a baiana', 'valor': 'peixe à baiana'},
        {'nome': 'pexe à baiana', 'valor': 'peixe à baiana'},
        {'nome': 'peixe a baiana', 'valor': 'peixe à baiana'},
        {'nome': 'peixe a bahiana', 'valor': 'peixe à baiana'},
        {'nome': 'Peixe á baiana', 'valor': 'peixe à baiana'},
        {'nome': 'PEIXE à Baiana', 'valor': 'peixe à baiana'},
        {'nome': 'peixe à baian', 'valor': 'peixe à baiana'},
        {'nome': 'peixes à baiana', 'valor': 'peixe à baiana'},
        {'nome': 'peixe à Baina', 'valor': 'peixe à baiana'},
        {'nome': 'baiana', 'valor': 'peixe à baiana'},
        {'nome': 'baiama', 'valor': 'peixe à baiana'},
        {'nome': 'peixe à escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'Pexe a escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'Pexe à escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'pexe a escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'pexe à escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe à escabexe', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe a escabexe', 'valor': 'peixe à escabeche'},
        {'nome': 'PeIXe á escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe à escabeches', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe à ecabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe escabexe', 'valor': 'peixe à escabeche'},
        {'nome': 'escabexe', 'valor': 'peixe à escabeche'},
        {'nome': 'escabeche', 'valor': 'peixe à escabeche'},
        {'nome': 'escabece', 'valor': 'peixe à escabeche'},
        {'nome': 'peixe à karague', 'valor': 'peixe a karague'},
        {'nome': 'pexe a karague', 'valor': 'peixe a karague'},
        {'nome': 'pexe à karague', 'valor': 'peixe a karague'},
        {'nome': 'pexe à carague', 'valor': 'peixe a karague'},
        {'nome': 'pexe a carague', 'valor': 'peixe a karague'},
        {'nome': 'pexe a Karague', 'valor': 'peixe a karague'},
        {'nome': 'pexe à Karague', 'valor': 'peixe a karague'},
        {'nome': 'peixe à Carague', 'valor': 'peixe a karague'},
        {'nome': 'peixe a karague', 'valor': 'peixe a karague'},
        {'nome': 'peixe á karague', 'valor': 'peixe a karague'},
        {'nome': 'peixe à karage', 'valor': 'peixe a karague'},
        {'nome': 'peixe Á karaQue', 'valor': 'peixe a karague'},
        {'nome': 'peixe à CARAGUE', 'valor': 'peixe a karague'},
        {'nome': 'PEIXE A KARAGUE', 'valor': 'peixe a karague'},
        {'nome': 'karague', 'valor': 'peixe a karague'},
        {'nome': 'karaague', 'valor': 'peixe a karague'},
        {'nome': 'Karaague', 'valor': 'peixe a karague'},
        {'nome': 'Karague', 'valor': 'peixe a karague'},
        {'nome': 'sashimi de salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimi d salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'sachimi de salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'sasimi de salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimi de salmao', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimi de salmã', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimi DE salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'Sashumi de salmão', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimi', 'valor': 'sashimi de salmão'},
        {'nome': 'sashimo', 'valor': 'sashimi de salmão'},
        {'nome': 'Sashimi', 'valor': 'sashimi de salmão'},
        {'nome': 'Sashimo', 'valor': 'sashimi de salmão'},
        {'nome': 'salmão grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'salmão grelado', 'valor': 'salmão grelhado'},
        {'nome': 'salmao grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'saumão grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'SAlmão grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'samão grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'salmão grelhad', 'valor': 'salmão grelhado'},
        {'nome': 'salmã grelhado', 'valor': 'salmão grelhado'},
        {'nome': 'camarão frito', 'valor': 'camarão frito'},
        {'nome': 'Camarão Frito', 'valor': 'camarão frito'},
        {'nome': 'camarao frito', 'valor': 'camarão frito'},
        {'nome': 'camara frit', 'valor': 'camarão frito'},
        {'nome': 'CAMARAO frito', 'valor': 'camarão frito'},
        {'nome': 'kamarão frito', 'valor': 'camarão frito'},
        {'nome': 'camarão fito', 'valor': 'camarão frito'},
        {'nome': 'camarão FRITO', 'valor': 'camarão frito'},
        {'nome': 'camarão', 'valor': 'camarão frito'},
        {'nome': 'camarao', 'valor': 'camarão frito'},
        {'nome': 'caramao', 'valor': 'camarão frito'},
        {'nome': 'caramão', 'valor': 'camarão frito'},
    ],

    'numero': [
        {'nome': '10', 'valor': '10'},
        {'nome': 'dez', 'valor': '10'},
        {'nome': 'Dez', 'valor': '10'},
        {'nome': '1', 'valor': '1'},
        {'nome': 'um', 'valor': '1'},
        {'nome': 'hum', 'valor': '1'},
        {'nome': '2', 'valor': '2'},
        {'nome': 'dois', 'valor': '2'},
        {'nome': 'doi', 'valor': '2'},
        {'nome': 'dos', 'valor': '2'},
        {'nome': 'duas', 'valor': '2'},
        {'nome': '3', 'valor': '3'},
        {'nome': 'tres', 'valor': '3'},
        {'nome': 'três', 'valor': '3'},
        {'nome': 'Tres', 'valor': '3'},
        {'nome': 'treis', 'valor': '3'},
        {'nome': 'trs', 'valor': '3'},
        {'nome': '4', 'valor': '4'},
        {'nome': 'quatro', 'valor': '4'},
        {'nome': 'Quatro', 'valor': '4'},
        {'nome': 'quato', 'valor': '4'},
        {'nome': 'qatro', 'valor': '4'},
        {'nome': 'cuatro', 'valor': '4'},
        {'nome': '5', 'valor': '5'},
        {'nome': 'cinco', 'valor': '5'},
        {'nome': 'Cinco', 'valor': '5'},
        {'nome': 'cinc', 'valor': '5'},
        {'nome': '6', 'valor': '6'},
        {'nome': 'seis', 'valor': '6'},
        {'nome': 'Seis', 'valor': '6'},
        {'nome': '7', 'valor': '7'},
        {'nome': 'Sete', 'valor': '7'},
        {'nome': 'sete', 'valor': '7'},
        {'nome': 'set', 'valor': '7'},
        {'nome': 'ete', 'valor': '7'},
        {'nome': '8', 'valor': '8'},
        {'nome': 'oito', 'valor': '8'},
        {'nome': 'Oito', 'valor': '8'},
        {'nome': 'oto', 'valor': '8'},
        {'nome': '9', 'valor': '9'},
        {'nome': 'nove', 'valor': '9'},
        {'nome': 'Nove', 'valor': '9'},
        {'nome': 'nov', 'valor': '9'},
        {'nome': 'ove', 'valor': '9'}
    ],

    'confirmacao': [
        {'nome': 'sim', 'valor': 'sim'},
        {'nome': 'som', 'valor': 'sim'},
        {'nome': 'sin', 'valor': 'sim'},
        {'nome': 'siim', 'valor': 'sim'},
        {'nome': 'siin', 'valor': 'sim'},
        {'nome': 'correto', 'valor': 'sim'},
        {'nome': 'certissimo', 'valor': 'sim'},
        {'nome': 'certíssimo', 'valor': 'sim'},
        {'nome': 'isso', 'valor': 'sim'},
        {'nome': 'isso mesmo', 'valor': 'sim'},
        {'nome': 'isso msm', 'valor': 'sim'},
        {'nome': 'é', 'valor': 'sim'},
        {'nome': 'é isso', 'valor': 'sim'},
        {'nome': 'sim, por gentileza', 'valor': 'sim'},
        {'nome': 'sim, por favor', 'valor': 'sim'},
        {'nome': 'óbvio', 'valor': 'sim'},
        {'nome': 'obvio', 'valor': 'sim'},
        {'nome': 'ta', 'valor': 'sim'},
        {'nome': 'tá', 'valor': 'sim'},
        {'nome': 'valeu', 'valor': 'sim'},
        {'nome': 'son', 'valor': 'sim'},
        {'nome': 's', 'valor': 'sim'},
        {'nome': 'si', 'valor': 'sim'},
        {'nome': 'yes', 'valor': 'sim'},
        {'nome': 'claro', 'valor': 'sim'},
        {'nome': 'certo', 'valor': 'sim'},
        {'nome': 'ok', 'valor': 'sim'},
        {'nome': 'beleza', 'valor': 'sim'},
        {'nome': 'blz', 'valor': 'sim'},
        {'nome': 'confirmo', 'valor': 'sim'},
        {'nome': 'confirmado', 'valor': 'sim'},
        {'nome': 'confirma', 'valor': 'sim'},
        {'nome': 'corrigir', 'valor': 'não'},
        {'nome': 'refazer', 'valor': 'não'},
        {'nome': '👎', 'valor': 'não'},
        {'nome': 'nao', 'valor': 'não'},
        {'nome': 'no', 'valor': 'não'},
        {'nome': 'não', 'valor': 'não'},
        {'nome': 'n', 'valor': 'não'},
        {'nome': 'cancela', 'valor': 'não'},
        {'nome': 'cancelado', 'valor': 'não'},
        {'nome': 'errado', 'valor': 'não'},
        {'nome': 'mudei de ideia', 'valor': 'não'},
        {'nome': 'desconfirma', 'valor': 'não'},
    ]
}

SESSOES = {}

#---------------------------------------------------------------------------------
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    resposta_do_bot = 'O que sou capaz de fazer?\n'
    resposta_do_bot += 'Ver o cardápio\n'
    resposta_do_bot += 'Fazer um pedido\n'
    resposta_do_bot += 'Ver a conta\n'

    update.message.reply_text(resposta_do_bot)

def help(update, context):
    """Send a message when the command /help is issued."""
    resposta_do_bot = 'O que sou capaz de fazer?\n'
    resposta_do_bot += 'Ver o cardápio\n'
    resposta_do_bot += 'Fazer um pedido\n'
    resposta_do_bot += 'Ver a conta\n'
    resposta_do_bot += '/commands\n'
    update.message.reply_text(resposta_do_bot)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def commands(update, context):
    """Send a message when the command /commands is issued."""
    update.message.reply_text('Comandos disponíveis: /start, /help, /commands, /sessions, /reset_session')

def sessions(update, context):
    """Send a message when the command /sessions is issued."""
    resposta_do_bot = 'Sessões ativas:\n\n'
    for sessao in SESSOES:
        resposta_do_bot += SESSOES[sessao]['nome'] + '\n'
        resposta_do_bot += str(SESSOES[sessao]['conta']) + '\n'
        resposta_do_bot += str(SESSOES[sessao]['pedidos_pendentes']) + '\n\n'
        
    update.message.reply_text(resposta_do_bot)

def reset_session(update, context):
    """Send a message when the command /reset_session is issued."""
    del SESSOES[update.message.chat_id]
    update.message.reply_text('Sessão resetada')

# ---------------------------------------------------------------------------------

def predict(update, context):
    mensagem_usuario = update.message.text

    usuario = get_or_create_usuario(update)                                                                                                 

    print('{} - {} => {}'.format(str(update.message.chat.id), update.message.chat.first_name, mensagem_usuario))
    pred = MODEL.predict(VECTORIZER.transform([update.message.text]))[0]

    if len(usuario['pedidos_pendentes']) > 0:
        print('Pedido pendente...\n')
        pedir_para_confirmar_pedido(update, mensagem_usuario)
        listar_pedidos_pendentes(update)

    elif pred == 'cardapio':
        print('Pegando Cardápio...\n')
        get_cardapio(update)

    elif pred == 'saudacao':
        print('Saudando...\n')
        saudar(update)

    elif pred == 'despedida':
        print('Despedindo...\n')
        despedir(update)
        clear_conta(update)

    elif pred == 'pedido':
        print('Fazendo pedido...\n')
        atender_pedido(update, mensagem_usuario)
    
    elif pred == 'conta':
        print('Verificando conta...\n')
        get_conta(update)
    
    else:
        print('Não entendi...\n')
        update.message.reply_text('Desculpe, não entendi o que você disse. Pode repetir por favor?\n')

def atender_pedido(update, mensagem_usuario):
    quantidade, produtos, etiquetas = identificar_pedido(mensagem_usuario.lower())
    if len(quantidade) == len(produtos) and len(quantidade) != 0:
        listar_itens_pedidos(update)
        resposta_bot = ''
        for i in range(len(quantidade)):
            resposta_bot += '{} - {}\n'.format(quantidade[i], produtos[i])
        resposta_bot += 'O pedido está correto?'
        add_pedido_pendente(update, quantidade, produtos, etiquetas)
        update.message.reply_text(resposta_bot)
    else:
        update.message.reply_text('Não entendi o que você pediu.\nTente pedir a quantidade seguida do prato. Assim: \nUm rodízio, 2 duas cocas')

def get_or_create_usuario(update):
    if update.message.chat.id in SESSOES:          # Se existe uma sessão para o usuário
        return SESSOES[update.message.chat.id]     # Retorna a sessão
    
    else:        
        SESSOES[update.message.chat.id] = {             # Cria uma nova sessão para o usuário
            'nome': update.message.chat.first_name, 
            'conta': [],
            'pedidos_pendentes': []
            }
        return SESSOES[update.message.chat.id]          # Retorna a sessão

def pedir_para_confirmar_pedido(update, mensagem_usuario):
    # O usuário precisa confirmar o pedido para poder pedir mais itens
    confirmacao = verifica_confirmacao(mensagem_usuario.lower())
    if confirmacao == 'sim':
        update.message.reply_text('Seu pedido foi confirmado e adicionado na sua conta.')
        add_conta(update)
        clear_pedidos_pendentes(update)
        return
    elif confirmacao == 'não':
        update.message.reply_text('Seu pedido foi cancelado.')
        clear_pedidos_pendentes(update)
        return
    else:
        update.message.reply_text('Você não confirmou seu pedido!')
        return

def listar_pedidos_pendentes(update):
    usuario = get_or_create_usuario(update)

    if len(usuario['pedidos_pendentes']) == 0:
        return

    resposta_do_bot = 'Pedidos pendentes:\n\n'
    for pedido in usuario['pedidos_pendentes']:
        resposta_do_bot += '{} - {}\n'.format(str(pedido['quantidade']), pedido['produto'])
    update.message.reply_text(resposta_do_bot)

def get_cardapio(update):
    update.message.reply_photo(open('./cardapio.jpeg', 'rb'))

def add_pedido_pendente(update, quantidade, produtos, etiquetas):
    # Adiciona um pedido pendente ao usuário
    usuario = get_or_create_usuario(update)

    for i in range(len(quantidade)):
        usuario['pedidos_pendentes'].append(
            {
                'quantidade': quantidade[i], 
                'produto': produtos[i],
                'etiqueta': etiquetas[i]
            })

def clear_pedidos_pendentes(update):
    # Limpa os pedidos pendentes do usuário
    usuario = get_or_create_usuario(update)
    usuario['pedidos_pendentes'].clear()

def add_conta(update):
    # Adiciona na conta do usuario, o pedido confirmado
    usuario = get_or_create_usuario(update)

    for pedido in usuario['pedidos_pendentes']:
        usuario['conta'].append(pedido)

def get_conta(update):
    # Retorna a conta do usuário
    usuario = get_or_create_usuario(update)

    if len(usuario['conta']) == 0:
        update.message.reply_text('Não há nada na sua conta!')
        return

    valor_total = 0
    resposta_bot = ''

    update.message.reply_text('Aqui está sua conta:')
    for item in usuario['conta']:
        for item_cardapio in CARDAPIO[item['etiqueta']]: # Percorre o cardápio
            if item['produto'] == item_cardapio['nome']:
                preco_unitario = item_cardapio['preco']  # Pega o preço do produto
                preco_unitario = preco_unitario.strip().replace('R$', '').replace(',','.').replace(' ', '') # Processo para transformar o preço de string para float
                preco_unitario = float(preco_unitario)

        quantidade = float(item['quantidade'])
        sub_total  = preco_unitario * quantidade # Preço unitário do produto * a quantidade pedida na sentença 'Quero duas cocas' => 5.80 * 2 
        valor_total = valor_total + sub_total    # Soma no valor da conta final
        resposta_bot += '{:<15}{:>20}R${:.2f}\n'.format(item['quantidade'] + ' - ' + item['produto'],'', sub_total)
    resposta_bot += '\nTotal: R${:.2f}'.format(valor_total)
    update.message.reply_text(resposta_bot)

def identificar_pedido(pedido):
    # Separa o pedido do usuário em palavras em uma lista
    # 'Quero uma coca e dois sobá' => ['Quero', 'uma', 'coca', 'e', 'dois', 'sobá']
    pedido = pedido.replace(',', '').replace('.', '')
    pedido_split = pedido.split()
    palavras = []
    quantidade = []
    produtos = []
    etiquetas = []

    # Concatena as palavras da lista criada usando split() até encontrar uma etiqueta adequada
    while len(pedido_split) > 0:
        palavras.append(pedido_split.pop(0))
        pedido_substring = ' '.join(palavras) # ['Quero', 'uma'] => 'Quero uma'
        etiqueta, valor =  encontrar_etiqueta(pedido_substring)
        if etiqueta is not None:
            if etiqueta == 'numero':
                quantidade.append(valor)
                palavras = [] # Resetar a lista de palavras para poder procurar pela próxima etiqueta
            elif etiqueta == 'bebida' or etiqueta == 'prato':
                produtos.append(valor)
                etiquetas.append(etiqueta)
                palavras = [] # Resetar a lista de palavras para poder procurar pela próxima etiqueta
    
    return quantidade, produtos, etiquetas

    

# Retorna a etiqueta e o valor dela
def encontrar_etiqueta(texto):
    bebidas = ETIQUETAS['bebida']
    pratos = ETIQUETAS['prato']
    numeros = ETIQUETAS['numero']

    for bebida in bebidas:                      
        if bebida['nome'] in texto:             # suco limao
            return 'bebida', bebida['valor']    # retorna 'bebida', 'suco de limão'

    for prato in pratos:
        if prato['nome'] in texto:              # escabeche
            return 'prato', prato['valor']      # retorna 'prato', 'peixe à escabeche'

    for numero in numeros:
        if numero['nome'] in texto:             # 'Quero duas'
            return 'numero', numero['valor']    # retorna 'numero', '2'

    return None, None

def verifica_confirmacao(texto):
    confirmacoes = ETIQUETAS['confirmacao']

    for confirmacao in confirmacoes:
        if confirmacao['nome'] == texto:        # 'sim'
            return confirmacao['valor'] # retorna 'confirmacao', 'sim'

    return None

def listar_itens_pedidos(update):
    usuario = get_or_create_usuario(update)

    if len(usuario['conta']) == 0:
        return

    resposta_bot = 'Sua conta até agora:'
    for item in usuario['conta']:
        resposta_bot += '\n{} - {}'.format(item['quantidade'], item['produto'])
    update.message.reply_text(resposta_bot)

def saudar(update):
    saudacoes_do_bot = [
        ', bem vindo(a) a casa do peixe! Pode fazer seu pedido.',
        ', eu sou o robô que irá atender seu pedido. Como posso ajudar hoje?',
        ', bem vindo(a) ao restaurante. O que vamos comer hoje?'
    ]
    random = randrange(len(saudacoes_do_bot)) # Pega uma saudação aleatória e imprime no console
    update.message.reply_text(update.message.chat.first_name + saudacoes_do_bot[random])


def despedir(update):
    despedidas_do_bot = [
        ', você será sempre bem vindo(a). Até mais!',
        ', foi bom ter você aqui. Até mais!',
        ', foi um prazer te atender. Volte sempre!',
        ', espero que tenha gostado. Volte sempre!'
    ]
    random = randrange(len(despedidas_do_bot)) # Pega uma despedida aleatória e imprime no console
    update.message.reply_text(update.message.chat.first_name +  despedidas_do_bot[random])

def clear_conta(update):
    usuario = get_or_create_usuario(update)
    usuario['conta'].clear()

def main():

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ajuda", help))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("sessions", sessions))
    dp.add_handler(CommandHandler("reset_session", reset_session))

    dp.add_handler(MessageHandler(Filters.text, predict))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
