import pytz
from datetime import datetime
import json
import requests
from authAUO import Licenc
from tqdm import tqdm
from func_sec import ret_grupo


def att_banco():

  try:
    
    r = requests.get('https://'+ Licenc.domain +'.freshdesk.com/api/v2/tickets?order_by=updated_at', auth = (Licenc.ch_leonardo, Licenc.password))
    if r.status_code == 200:
      print (5*'=====')
      vem_json = json.loads(r.content)

      return vem_json
    else:
      print ("Falha em lê tickets")
      response = json.loads(r.content)
      print (response["errors"])
      print ("Status Code : " + str(r.status_code))
  
  except Exception as ex:
    print ('Erro >> ', ex)

def busca_completa():
    try:
        a = True
        cont = 1
        lista = []
        while a :
          r = requests.get('https://'+ Licenc.domain +'.freshdesk.com/api/v2/tickets?updated_since=2018-01-11T00:00:00Z&page={}&per_page=100'.format(cont), auth = (Licenc.ch_leonardo, Licenc.password))
          if r.status_code == 200:
              print (5*'=====')
              vem_json = json.loads(r.content)
              print ('Pagina {} tamanho {}'.format(cont, len(vem_json)))
              
              if len(vem_json) > 0:
                lista.append(vem_json)
                cont += 1
              else:
                a = False
          else:
              print ("Falha em lê tickets")
              response = json.loads(r.content)
              print (response["errors"])
              print ("Status Code : " + str(r.status_code))
              a = False
    except Exception as ex:
        print ('Erro >> ', ex)

    return lista

def clr_hora(string: str) -> datetime:
  UTC = pytz.utc
  BRTZ = pytz.timezone('America/Sao_Paulo')
  
  datetime_utf = datetime.strptime(
        string, '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=UTC)
        
  x = datetime_utf.astimezone(BRTZ)  
  return x.strftime('%H:%M:%S %d-%m-%Y')
  
def name_co(codigo):
  try:                                                                                                                                    
    var = requests.get("https://"+ Licenc.domain +".freshdesk.com/api/v2/companies/{}".format(codigo), auth = (Licenc.ch_leonardo, Licenc.password))
    var = var.content
    var = json.loads(var)
    return var['name']
  except Exception as e:
    print(e)
    return 'NAN'

def name_contato(codigo):
  try:
    cont = requests.get("https://"+ Licenc.domain +".freshdesk.com/api/v2/contacts/{}".format(codigo), auth = (Licenc.ch_leonardo, Licenc.password))
    cont = cont.content
    cont = json.loads(cont)
    return cont['name']
  except Exception as e:
    print(e)
    return 'NAN'

def agentes_auo(codigo):
  try:
    agent = requests.get("https://"+ Licenc.domain +".freshdesk.com/api/v2/agents/{}".format(codigo), auth = (Licenc.ch_vincente, Licenc.password))
    agent = agent.content
    agent = json.loads(agent)
    return agent['contact']['name']
  except:
    return 'Analista não definido'

def sts_code(codigo, source, priority):
    sts_dict = {2:'Aberto', 3: 'Pendente', 4: 'Resolvido', 5:  'Fechado'}
    src_dict = {1:'E-mail', 2:'Portal', 3: 'Telefone', 7 : 'Chat', 9: 'Feedback widget', 10 : 'E-mail saida'}
    priority_dict = {1:'Baixa', 2:'Média', 3:'Alta', 4:'Urgente'}
    
    status = sts_dict.get(codigo)
    source = src_dict.get(source)
    priority = priority_dict.get(priority)

    return (status, source, priority)

def popula_banco():
    abc = busca_completa()
    tickets = []

    print('REQUISIÇÕES CONCLUIDAS!\n')
    print('LIMPANDO OS DADOS!\n')

    for y in tqdm(abc):
      for a in tqdm(y):
          x = sts_code(a['status'], a['source'], a['priority'])
          tickets.append({'id': a['id'], 'assunto' : a['subject'], 'tipo': a['type'], 'status': x[0], 'origem': x[1], 'prioridade': x[2], 'hora_abert': clr_hora(a['created_at']), 'prz_resp_1': clr_hora(a['fr_due_by']),
                      'prz_final': clr_hora(a['due_by']), 'grupo': ret_grupo(a['group_id']), 'analista': agentes_auo(a['responder_id']), 'ultima_at': clr_hora(a['updated_at']), 'empresa': name_co(a['company_id']), 'contato': name_contato(a['requester_id'])})
    return tickets

def atualiza_banco():
    abc = att_banco()
    tickets = []

    print('REQUISIÇÕES CONCLUIDAS!\n')
    print('LIMPEZA DOS DADOS!\n')

    for a in tqdm(abc):
        x = sts_code(a['status'], a['source'], a['priority'])
        tickets.append({'id': a['id'], 'assunto' : a['subject'], 'tipo': a['type'], 'status': x[0], 'origem': x[1], 'prioridade': x[2], 'hora_abert': clr_hora(a['created_at']), 'prz_resp_1': clr_hora(a['fr_due_by']),
                    'prz_final': clr_hora(a['due_by']), 'grupo': ret_grupo(a['group_id']), 'analista': agentes_auo(a['responder_id']), 'ultima_at': clr_hora(a['updated_at']), 'empresa': name_co(a['company_id']), 'contato': name_contato(a['requester_id'])})
    
    return tickets