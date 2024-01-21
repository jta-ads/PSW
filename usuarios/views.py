from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirmar_senha')

        if not senha == confirma_senha:
            messages.add_message(request, constants.ERROR, 'Senha e Confirma senha não Coincidem')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário Já Existe')
            return redirect('/usuarios/cadastro')
        try:
            User.objects.create_user(
                username = username,
                password= senha
            )
            return redirect('/usuarios/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do Servidor')
            return redirect('/usuario/cadastro')

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password = senha)

        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado com Sucesso')
            return redirect('/flashcard/novo_flashcard/')
        else: 
            messages.add_message(request, constants.ERROR, 'Username e Senha Invalido')
            return redirect('/usuarios/logar')

def logout(request):
    auth.logout(request)
    return redirect('/usuario/logar')