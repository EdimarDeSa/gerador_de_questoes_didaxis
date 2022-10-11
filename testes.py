import encodings
import json
from os.path import abspath

xml = abspath('./configs/configs.json')
with open(xml, 'r', encoding = 'UTF-8') as arquivo_configuracoes:
    y: list = json.load(fp = arquivo_configuracoes)['Dificuldades']

print(y.)
