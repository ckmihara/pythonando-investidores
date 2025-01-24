import string
import random

def gerar_senha(tamanho):
    if tamanho < 9:
        print("O tamanho da senha deve ser de pelo menos 8")
    
    else: 
        senha = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]
        possibilidades = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation])
        senha.extend(random.choices(possibilidades, k=tamanho-4))

        random.shuffle(senha)
        return ''.join(senha)

# tamanho = int(input("Digite o comprimento da senha: "))
# print(gerar_senha(tamanho))

def analisar_senha(senha, confirmar_senha):
    """
    Analisa o conteúdo da senha:
        - A senha deve possuir no mínimo 8 dígitos
        - A senha deve possuir no mínimo um caracter especial
        - A senha deve possuir no mínimo 1 letra maiúscula
        - A senha deve possuir no mínimo 1 letra maiúscula minúscula        

    Parameters
    ----------
    senha : str
        senha a ser analisado

    Returns
    -------
    tuple
        Contagem de palavras, frequência de palavras e frequência de letras
    """
    validacao = {}
    
    # validação do tamanho da senha (mínimo 8 dígitos)
    
    tamanho = len(senha.translate(str.maketrans('', '')))

    if tamanho < 8 :
        validacao['tamanho'] = False
    else :
        validacao['tamanho'] = True

    # senha diferente do confirmar senha

    if not senha == confirmar_senha:
        validacao['confirmar_senha'] = False
    else :
        validacao['confirmar_senha'] = True
            
    
    # Remove a pontuação do senha
    tratamento = str.maketrans('', '', string.punctuation)
    senha_tratado = senha.translate(tratamento)
    original = senha.translate(str.maketrans('', ''))    
    
    if original == senha_tratado :
        validacao['especial'] = False
    else :
        validacao['especial'] = True

    # Remove letra maiúscula do senha
    tratamento = str.maketrans('', '', string.ascii_uppercase)
    senha_tratado = senha.translate(tratamento)
    original = senha.translate(str.maketrans('', ''))    
    
    if original == senha_tratado :
        validacao['maiuscula'] = False
    else :
        validacao['maiuscula'] = True
        
    # Remove letra minúscula do senha
    tratamento = str.maketrans('', '', string.ascii_lowercase)
    senha_tratado = senha.translate(tratamento)
    original = senha.translate(str.maketrans('', ''))    
    
    if original == senha_tratado :
        validacao['minuscula'] = False
    else :
        validacao['minuscula'] = True
        
    # Remove números do senha
    tratamento = str.maketrans('', '', string.digits)
    senha_tratado = senha.translate(tratamento)
    original = senha.translate(str.maketrans('', ''))    
    
    if original == senha_tratado :
        validacao['numeros'] = False
    else :
        validacao['numeros'] = True
        
    return validacao

