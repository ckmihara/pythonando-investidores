from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
from .utils import gerar_senha, analisar_senha

def cadastro(request):

    senha_sugerida = gerar_senha(10)

    if request.method == "GET":
        return render(request, 'cadastro.html', {'senha_sugerida': senha_sugerida})
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #
        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, 'Este usuário já está cadastrado')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})

        validacoes_senha = analisar_senha(senha, confirmar_senha)

        if not validacoes_senha['confirmar_senha']:
            messages.add_message(request, constants.ERROR, 'A senha e confirmar senha devem ser iguais')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['tamanho']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 8 dígitos')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['especial']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos um caracter especial')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['maiuscula']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos uma letra maiúscula')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['minuscula']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos uma letra minúscula')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['numeros']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos um número')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        user = User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('/usuarios/logar')
    
def logar(request):

    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/empresarios/cadastrar_empresa') 

        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return render(request, 'logar.html', {'form_data': form_data})
    
def sair(request):
    auth.logout(request)
    return redirect('/usuarios/logar')

def teste(request):
    print(request.META)
    return HttpResponse('Teste')
