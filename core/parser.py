import yaml
from core.test_case import TestCase

def carregar_casos_teste(caminho_yaml):
    with open(caminho_yaml, 'r', encoding='utf-8') as f:
        dados = yaml.safe_load(f)

    casos = []
    for item in dados['casos']:
        caso = TestCase(
            name=item['nome'],
            input_path=item['entrada'],
            expected_path=item['esperado']
        )
        # Adiciona atributo extra ao objeto
        caso.espera_erros = item.get('esperaErros', False)
        casos.append(caso)

    return casos
