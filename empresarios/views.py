from django.shortcuts import render, redirect
from .models import Empresas, Documento, Metricas
from investidores.models import PropostaInvestimento
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from .utils import validacao_cnpj, verificar_site
from datetime import date, datetime
from django.core.exceptions import ValidationError
import tempfile
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay
from django.db.models import Count, Sum



def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices })
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        cnpj = ''.join(filter(str.isdigit, cnpj))
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        # TODO

        # Validar se o site existe  ???
        # Validar se o pitch e o logo são válidos

        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #
        # print(f'form_data {form_data}')

        if not nome :
            messages.add_message(request, constants.ERROR, 'Nome da empresa obrigatório')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not validacao_cnpj(cnpj):
            messages.add_message(request, constants.ERROR, 'CNPJ inválido')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            cnpj = ''.join(filter(str.isdigit, cnpj))
            empresas = Empresas.objects.filter(cnpj=cnpj)
            if empresas.exists():
                messages.add_message(request, constants.ERROR, 'CNPJ já existe')
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not site:
            messages.add_message(request, constants.ERROR, 'Informação de site é obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            url = verificar_site(site)
            if not url:
                messages.add_message(request, constants.ERROR, 'Este site não existe')
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not tempo_existencia:
            messages.add_message(request, constants.ERROR, 'Informação de tempo de existência obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            existencia_choices = [choice[0] for choice in Empresas.tempo_existencia_choices]
            if tempo_existencia not in existencia_choices:
                messages.add_message(request, constants.ERROR, "Opção inválida para o tempo de existência.")
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not descricao:
            messages.add_message(request, constants.ERROR, 'Descrição obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not data_final:
            messages.add_message(request, constants.ERROR, 'Data final para captação obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        data_formatada = datetime.strptime(data_final, '%Y-%m-%d').date()
        if date.today() > data_formatada:
            messages.add_message(request, constants.ERROR, 'É necessário que a data final para captação seja maior que a data de hoje')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not percentual_equity:
            messages.add_message(request, constants.ERROR, 'O percentual de contrapartida é obrigatório')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if  not estagio  :
            messages.add_message(request, constants.ERROR, 'Informação de estágio obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            estagios_choices = [choice[0] for choice in Empresas.estagio_choices]
            if estagio not in estagios_choices:
                messages.add_message(request, constants.ERROR, "Opção de estágio inválida.")
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not area:
            messages.add_message(request, constants.ERROR, 'In formação de área é obrigatória')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            areas_choices = [choice[0] for choice in Empresas.area_choices]
            if area not in areas_choices:
                messages.add_message(request, constants.ERROR, "Opção de área inválida.")
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not publico_alvo  :
            messages.add_message(request, constants.ERROR, 'Informação de público alvo é obrigatório')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        else :
            publicos_alvo_choices = ['B2B', 'B2C']
            if publico_alvo not in publicos_alvo_choices:
                messages.add_message(request, constants.ERROR, "Público alvo inválido.")
                return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
            
        if not valor:
            messages.add_message(request, constants.ERROR, 'O valor a captar é obrigatório')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        if not pitch:
            messages.add_message(request, constants.ERROR, 'É necessário anexar um arquivo de apresentação')
            return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        # else :
        #     my_model_instance = Empresas(pitch=pitch)
        #     try:
        #         my_model_instance.clean()  # Valida os tamanhos dos arquivos
        #         # my_model_instance.save()
        #         # return HttpResponse("Arquivos enviados com sucesso!")
        #     except ValidationError as e:
        #         uploaded_files = {}
        #         tempo_dir = tempfile.mkdtemp()
        #         temp_path = f"{tempo_dir}/{pitch.name}"
        #         with open(temp_path, 'wb+') as temp_file:
        #             for chunk in pitch.chunks():
        #                 temp_file.write(chunk)

        #         uploaded_files['pitch'] = temp_path

        #         messages.add_message(request, constants.ERROR, 'O arquivo deve ser menor que 500KB')
        #         return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices, 'uploaded_files': uploaded_files})
        
            


        # messages.add_message(request, constants.ERROR, 'Teste de validação ')
        # return render(request, 'cadastrar_empresa.html', {'form_data': form_data, 'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices})
        
        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
            empresa.save()
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/empresarios/cadastrar_empresa')
        
        messages.add_message(request, constants.SUCCESS, 'Empresa criada com sucesso')
        return redirect('/empresarios/cadastrar_empresa')    
    
def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    
    if request.method == "GET":
        nome_empresa = request.GET.get('empresa', '')
        if nome_empresa:
            empresas = Empresas.objects.filter(nome__icontains=nome_empresa).filter(user=request.user)
        else:
            empresas = Empresas.objects.all().filter(user=request.user)
        
        return render(request, 'listar_empresas.html', {'empresas': empresas, 'nome_empresa': nome_empresa})
    
def empresa(request, id):

    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')

    empresa = Empresas.objects.get(id=id)

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Esta empresa não é sua')
        return redirect(f'/empresarios/emprlistar_empresas')
   
    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
        proposta_investimentos_enviada = proposta_investimentos.filter(status='PE')

        percentual_vendido = 0
        for pi in proposta_investimentos:
            if pi.status == 'PA':
                percentual_vendido += pi.percentual

        total_captado = sum(proposta_investimentos.filter(status='PA').values_list('valor', flat=True))

        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0
        percentual_ser_vendido = int((100 * float(valuation_atual)) / float(empresa.valuation) if empresa.valuation != 0 else 0)

        percentual_vendido = int(percentual_vendido)

        return render(request, 'empresa.html', {'empresa': empresa, 'documentos': documentos, 'proposta_investimentos_enviada': proposta_investimentos_enviada, 'percentual_vendido': percentual_vendido, 'total_captado': total_captado, 'valuation_atual':valuation_atual, 'percentual_ser_vendido': percentual_ser_vendido})


def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Esta empresa não é sua')
        return redirect(f'/empresarios/listar_empresas')

    if request.method == "POST":     
        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #
        # print(f'form_data {form_data}')

        if not titulo:
            messages.add_message(request, constants.ERROR, "Título obrigatório")
            print(f'empresa {empresa}')
            print(f'form_data {form_data}')
            return render(request, 'empresa.html', {'empresa': empresa, 'form_data': form_data})
            
        if not arquivo:
            messages.add_message(request, constants.ERROR, "Envie um arquivo")
            return render(request, 'empresa.html', {'empresa': empresa, 'form_data': form_data})
            
        extensao = arquivo.name.split('.')[-1]

        if extensao != 'pdf':
            messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
            return redirect(f'/empresarios/empresa/{empresa.id}')
        
        documento = Documento(
            empresa=empresa,
            titulo=titulo,
            arquivo=arquivo
        )
        documento.save()
        messages.add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
    
    return redirect(f'/empresarios/empresa/{empresa.id}')        

def excluir_dc(request, id):

    documento = Documento.objects.get(id=id)

    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Esse documento não é seu")
        return redirect(f'/empresarios/empresa/{documento.empresa.id}')

    documento.delete()
    messages.add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
    return redirect(f'/empresarios/empresa/{documento.empresa.id}')

def add_metrica(request, id):

    if request.method == "POST":     
        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #
        # print(f'form_data {form_data}')

        empresa = Empresas.objects.get(id=id)
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')

        proposta_investimentos_enviada = PropostaInvestimento.objects.filter(empresa=empresa).filter(status='PE')
        # proposta_investimentos = PropostaInvestimento.objects.filter(empresa=empresa).filter(status='PE')
        # proposta_investimentos_enviada = proposta_investimentos.filter(status='PE')
        
        if not descricao:
            messages.add_message(request, constants.ERROR, "Descrição obrigatória")
            return render(request, 'empresa.html', {'empresa': empresa, 'form_data': form_data, 'proposta_investimentos_enviada': proposta_investimentos_enviada})
            
        if not valor:
            messages.add_message(request, constants.ERROR, "Valor obrigatório")
            return render(request, 'empresa.html', {'empresa': empresa, 'form_data': form_data, 'proposta_investimentos_enviada': proposta_investimentos_enviada})
        
        metrica = Metricas(
            empresa=empresa,
            titulo=descricao,
            valor=valor
        )
        metrica.save()

        messages.add_message(request, constants.SUCCESS, "Métrica cadastrada com sucesso")
        # return render(request, 'empresa.html', {'empresa': empresa})
        return redirect(f'/empresarios/empresa/{empresa.id}')

def dashboard2(request, id):
    empresa = Empresas.objects.get(id=id)
    today = timezone.now().date()
                  
    seven_days_ago = today - timedelta(days=6)

    propostas_por_dia = {}

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)

        propostas = PropostaInvestimento.objects.filter(
            empresa=empresa,
            status='PA',
            data=day
            )
        
        total_dia = 0
        for proposta in propostas :
            total_dia += proposta.valor

        propostas_por_dia[day.strftime('%d/%m/%Y')] = int(total_dia)
    
    return render(request, 'dashboard.html', {
        'labels': list(propostas_por_dia.keys()), 
        'values': list(propostas_por_dia.values())
        })

def dashboard(request, id):
    empresa = Empresas.objects.get(id=id)
    today = timezone.now().date()
                  
    seven_days_ago = today - timedelta(days=6)

    # Cria um dicionário com todos os dias no intervalo e valores padrão como 0
    propostas_por_dia = { (seven_days_ago + timedelta(days=i)).strftime('%d/%m/%Y'): 0 for i in range(7) }

    # Recupera as propostas reais e atualiza o dicionário
    propostas = (
        PropostaInvestimento.objects.filter(
            empresa=empresa,
            status='PA',
            data__range=[seven_days_ago, today]
            )
            .annotate(date=TruncDay('data'))
            .values('date')
            .annotate(total=Sum('valor'))
            .order_by('date')
    )

    for proposta in propostas:
        date_str = proposta['date'].strftime('%d/%m/%Y')
        propostas_por_dia[date_str] = float(proposta['total'])

    labels = list(propostas_por_dia.keys())
    values = list(propostas_por_dia.values())

    return render(request, 'dashboard.html', {
        'labels': labels,
        'values': values
    })
