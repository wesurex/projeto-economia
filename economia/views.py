from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.db.models import Sum
from decimal import Decimal
from datetime import date
from .models import Receita, Despesa, Investimento, ContasPagar


from datetime import date, timedelta
from django.db.models import Sum
from django.shortcuts import render
from .models import Receita, Despesa, Investimento, ContasPagar


def home_view(request):
    # === AUTO-GERADOR DE CONTAS RECORRENTES ===
    hoje = date.today()
    recorrentes = ContasPagar.objects.filter(recorrente=True)

    criadas = 0
    for conta in recorrentes:
        dias_para_vencimento = (conta.vencimento - hoje).days

        # Se faltar 10 dias ou menos pro vencimento atual
        if dias_para_vencimento <= 10:
            proximo_vencimento = conta.vencimento + timedelta(days=30)

            # Evita duplicar se já existir uma conta igual pro próximo mês
            existe = ContasPagar.objects.filter(
                descricao=conta.descricao,
                valor=conta.valor,
                vencimento=proximo_vencimento,
                recorrente=True
            ).exists()

            if not existe:
                ContasPagar.objects.create(
                    descricao=conta.descricao,
                    valor=conta.valor,
                    vencimento=proximo_vencimento,
                    pago=False,
                    recorrente=True
                )
                criadas += 1

    if criadas > 0:
        print(
            f"[AUTO] {criadas} contas recorrentes foram geradas automaticamente em {hoje.strftime('%d/%m/%Y')}.")

    else:
        print(
            f"[AUTO] Nenhuma conta recorrente precisava ser gerada ({hoje.strftime('%d/%m/%Y')}).")

    # === TOTALIZADORES ORIGINAIS ===
    mes = int(request.GET.get("mes", date.today().month))
    ano = int(request.GET.get("ano", date.today().year))

    # ---- TOTALIZADORES GERAIS ----
    total_receitas_geral = Receita.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_despesas_geral = Despesa.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_investimentos_geral = Investimento.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0

    total_liquido = total_receitas_geral - total_despesas_geral
    patrimonio_total = total_liquido + total_investimentos_geral

    # ---- CONTAS A PAGAR ----
    total_contas = ContasPagar.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_contas_pagas = ContasPagar.objects.filter(
        pago=True).aggregate(Sum("valor"))["valor__sum"] or 0
    total_contas_pendentes = ContasPagar.objects.filter(
        pago=False).aggregate(Sum("valor"))["valor__sum"] or 0
    qtd_pendentes = ContasPagar.objects.filter(pago=False).count()

    # ---- TOTALIZADORES MENSAL ----
    receitas_mes = Receita.objects.filter(data__month=mes, data__year=ano)
    despesas_mes = Despesa.objects.filter(data__month=mes, data__year=ano)
    investimentos_mes = Investimento.objects.filter(
        data__month=mes, data__year=ano)
    contas_mes = ContasPagar.objects.filter(
        vencimento__month=mes, vencimento__year=ano)

    total_receitas_mes = receitas_mes.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_despesas_mes = despesas_mes.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_investimentos_mes = investimentos_mes.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_contas_mes_pendentes = contas_mes.filter(
        pago=False).aggregate(Sum("valor"))["valor__sum"] or 0

    saldo_mes = total_receitas_mes - total_despesas_mes

    contexto = {
        # --- GERAIS ---
        "total_liquido": f"R$ {total_liquido:,.2f}",
        "total_investimentos": f"R$ {total_investimentos_geral:,.2f}",
        "patrimonio_total": f"R$ {patrimonio_total:,.2f}",

        # --- CONTAS ---
        "total_contas": f"R$ {total_contas:,.2f}",
        "total_contas_pagas": f"R$ {total_contas_pagas:,.2f}",
        "total_contas_pendentes": f"R$ {total_contas_pendentes:,.2f}",
        "qtd_pendentes": qtd_pendentes,

        # --- MENSAL ---
        "mes": mes,
        "ano": ano,
        "total_receitas_mes": f"R$ {total_receitas_mes:,.2f}",
        "total_despesas_mes": f"R$ {total_despesas_mes:,.2f}",
        "total_investimentos_mes": f"R$ {total_investimentos_mes:,.2f}",
        "total_contas_mes_pendentes": f"R$ {total_contas_mes_pendentes:,.2f}",
        "saldo_mes": f"R$ {saldo_mes:,.2f}",
    }

    return render(request, "home.html", contexto)



def receitas_view(request):
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        data_receita = request.POST.get("data")

        if descricao and valor and data_receita:
            Receita.objects.create(descricao=descricao,
                                   valor=valor, data=data_receita)
            return redirect("receitas")

    # Filtros de mês e ano
    mes = int(request.GET.get("mes", date.today().month))
    ano = int(request.GET.get("ano", date.today().year))

    receitas_queryset = Receita.objects.filter(
        data__month=mes, data__year=ano).order_by("-data")

    # === PAGINAÇÃO ===
    paginator = Paginator(receitas_queryset, 20)  # 20 por página
    page_number = request.GET.get("page")
    receitas = paginator.get_page(page_number)

    total_receitas = receitas_queryset.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_geral = Receita.objects.aggregate(Sum("valor"))["valor__sum"] or 0

    contexto = {
        "receitas": receitas,
        "paginator": paginator,
        "mes": mes,
        "ano": ano,
        "total_receitas": f"R$ {total_receitas:,.2f}",
        "total_geral": f"R$ {total_geral:,.2f}",
    }

    return render(request, "receitas.html", contexto)


def despesas_view(request):
    # --- Cadastro de nova despesa ---
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        valor = Decimal(request.POST.get("valor") or 0)
        data_despesa = request.POST.get("data")
        investimento_id = request.POST.get("investimento")

        investimento = Investimento.objects.filter(
            id=investimento_id).first() if investimento_id else None

        if descricao and valor and data_despesa:
            Despesa.objects.create(
                descricao=descricao,
                valor=valor,
                data=data_despesa,
                investimento=investimento
            )
            return redirect("despesas")

    # --- Filtros mensais ---
    mes = int(request.GET.get("mes", date.today().month))
    ano = int(request.GET.get("ano", date.today().year))

    despesas_queryset = Despesa.objects.filter(
        data__month=mes, data__year=ano).order_by("-data")

    # --- Paginação (20 por página) ---
    paginator = Paginator(despesas_queryset, 20)
    page_number = request.GET.get("page")
    despesas = paginator.get_page(page_number)

    # --- Totais ---
    total_despesas_mes = despesas_queryset.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_despesas_geral = Despesa.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0

    contexto = {
        "despesas": despesas,
        "paginator": paginator,
        "mes": mes,
        "ano": ano,
        "total_despesas_mes": f"R$ {total_despesas_mes:,.2f}",
        "total_despesas_geral": f"R$ {total_despesas_geral:,.2f}",
        "investimentos": Investimento.objects.all(),
    }

    return render(request, "despesas.html", contexto)


def investimentos_view(request):
    # --- Adicionar investimento ---
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        data_investimento = request.POST.get("data")

        if descricao and valor and data_investimento:
            Investimento.objects.create(
                descricao=descricao,
                valor=valor,
                data=data_investimento
            )
            return redirect("investimentos")

    # --- Filtro mensal ---
    mes = int(request.GET.get("mes", date.today().month))
    ano = int(request.GET.get("ano", date.today().year))

    investimentos_queryset = Investimento.objects.filter(
        data__month=mes, data__year=ano).order_by("-data")

    # --- Paginação ---
    paginator = Paginator(investimentos_queryset, 20)
    page_number = request.GET.get("page")
    investimentos = paginator.get_page(page_number)

    # --- Totais ---
    total_invest_mes = investimentos_queryset.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_invest_geral = Investimento.objects.aggregate(Sum("valor"))[
        "valor__sum"] or 0

    contexto = {
        "investimentos": investimentos,
        "paginator": paginator,
        "mes": mes,
        "ano": ano,
        "total_invest_mes": f"R$ {total_invest_mes:,.2f}",
        "total_invest_geral": f"R$ {total_invest_geral:,.2f}",
    }

    return render(request, "investimentos.html", contexto)


def contas_view(request):
    # --- Adicionar nova conta ---
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        valor = Decimal(request.POST.get("valor") or 0)
        vencimento = request.POST.get("vencimento")

        if descricao and valor and vencimento:
            ContasPagar.objects.create(
                descricao=descricao,
                valor=valor,
                vencimento=vencimento
            )
            return redirect("contas")

    # --- Filtros mensais ---
    mes = int(request.GET.get("mes", date.today().month))
    ano = int(request.GET.get("ano", date.today().year))

    contas_queryset = ContasPagar.objects.filter(
        vencimento__month=mes, vencimento__year=ano).order_by("vencimento")

    # --- Paginação ---
    paginator = Paginator(contas_queryset, 20)
    page_number = request.GET.get("page")
    contas = paginator.get_page(page_number)

    # --- Totais ---
    total_contas_mes = contas_queryset.aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_pagas = contas_queryset.filter(pago=True).aggregate(Sum("valor"))[
        "valor__sum"] or 0
    total_pendentes = contas_queryset.filter(
        pago=False).aggregate(Sum("valor"))["valor__sum"] or 0

    contexto = {
        "contas": contas,
        "paginator": paginator,
        "mes": mes,
        "ano": ano,
        "total_contas_mes": f"R$ {total_contas_mes:,.2f}",
        "total_pagas": f"R$ {total_pagas:,.2f}",
        "total_pendentes": f"R$ {total_pendentes:,.2f}",
    }

    return render(request, "contas.html", contexto)
