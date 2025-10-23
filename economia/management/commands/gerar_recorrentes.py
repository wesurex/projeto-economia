from django.core.management.base import BaseCommand
from economia.models import ContasPagar
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = "Gera automaticamente novas faturas para contas recorrentes a cada mês"

    def handle(self, *args, **options):
        hoje = date.today()
        ultimo_dia_mes = date(hoje.year, hoje.month + 1, 1) - \
            timedelta(days=1) if hoje.month < 12 else date(hoje.year, 12, 31)
        faltam_dias = (ultimo_dia_mes - hoje).days

        if faltam_dias > 10:
            self.stdout.write(
                "Ainda não está no período de geração (faltam mais de 10 dias para o fim do mês).")
            return

        recorrentes = ContasPagar.objects.filter(recorrente=True)

        criadas = 0
        for conta in recorrentes:
            proximo_vencimento = conta.vencimento + timedelta(days=30)

            # Evita duplicar se já existe uma fatura futura igual
            existe = ContasPagar.objects.filter(
                descricao=conta.descricao,
                valor=conta.valor,
                vencimento=proximo_vencimento
            ).exists()

            if not existe:
                nova = ContasPagar.objects.create(
                    descricao=conta.descricao,
                    valor=conta.valor,
                    vencimento=proximo_vencimento,
                    pago=False,
                    recorrente=True
                )
                criadas += 1
                self.stdout.write(
                    f"Nova conta criada: {nova.descricao} - {nova.vencimento}")

        if criadas == 0:
            self.stdout.write(self.style.WARNING(
                "Nenhuma nova conta recorrente foi gerada."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"{criadas} contas recorrentes foram criadas."))
