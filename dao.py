from peewee import *

db = SqliteDatabase('tkts.db')

class BaseModel(Model):
    class Meta:
        database = db

class Tickets(BaseModel):
    id = IntegerField()
    assunto = CharField()
    tipo = CharField()
    status = CharField()
    origem = CharField()
    prioridade = CharField()
    hora_abert = DateTimeField()
    prz_resp_1 = DateTimeField()
    prz_final = DateTimeField()
    ultima_at = DateTimeField(primary_key=True)
    grupo = CharField()
    analista = CharField()
    empresa = CharField()
    contato = CharField()

def insert_data(self,lista):
    try:
        a = self.create(
                id = lista['id'],
                assunto = lista['assunto'],
                tipo = lista['tipo'],
                status = lista['status'],
                origem = lista['origem'],
                prioridade = lista['prioridade'],
                hora_abert = lista['hora_abert'],
                prz_resp_1 = lista['prz_resp_1'],
                prz_final = lista['prz_final'],
                ultima_at = lista['ultima_at'],
                grupo = lista['grupo'],
                analista = lista['analista'],
                empresa = lista['empresa'],
                contato = lista['contato'],
        )
    except:
        pass
        #print('Falha na inserção do registro > - > ', lista['id'])



'''
if __name__ == '__main__':
    try:
        Tickets.create_table()
        print('!! tabela criada !!')
    except OperationalError:
        print('!! tabela ja existe !!')
'''
