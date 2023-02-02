from genericpath import exists
from dao import Tickets, insert_data
from func_clr import atualiza_banco, busca_completa
from tqdm import tqdm

lista_de_tkts = []

if exists('tkts.db'):
    lista_de_tkts = atualiza_banco()
else:
    lista_de_tkts = busca_completa()

print(5*'-------')
print('\nGRAVANDO BANCO')

for x in tqdm(lista_de_tkts):
    insert_data(Tickets,x)



