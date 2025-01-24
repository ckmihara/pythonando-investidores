import requests

def validacao_cnpj(cnpj):
    """Função para validar o CNPJ.
       Retorna True ou False
    """

    # Remove caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se o CNPJ tem 12 dígitos (sem os verificadores)
    if len(cnpj) != 14:
        return False
    else :
        cnpj_calculado = cnpj[:-2]

    # Cálculo do primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = 0
    for i in range(12):
        soma1 += int(cnpj_calculado[i]) * pesos1[i]
    digito1 = 11 - (soma1 % 11)
    digito1 = 0 if digito1 >= 10 else digito1

    # Cálculo do segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma2 = 0
    for i in range(13):
        soma2 += int(cnpj_calculado[i] if i < 12 else str(digito1)) * pesos2[i]
    digito2 = 11 - (soma2 % 11)
    digito2 = 0 if digito2 >= 10 else digito2
    
    if cnpj == cnpj_calculado + str(digito1) + str(digito2) :
        return True
    else :
        return False
    
def verificar_site(url):
    url = "https://" + url
    try:
        response = requests.get(url)
        # Verifica se o status code está na faixa de 200 (requisição bem-sucedida)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Captura qualquer exceção que ocorra durante a requisição
        return False



