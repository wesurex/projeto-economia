from django.core.management.base import BaseCommand
from economia.models import Receita
from faker import Faker
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Cria receitas falsas para testes"

    def handle(self, *args, **options):
        fake = Faker('pt_BR')
        Faker.seed(42)

        descricoes = [
            "Salário Mensal", "Venda Online", "Freelance", "Cashback", "Reembolso",
            "Rendimento de Poupança", "Venda no Mercado Livre", "Pix Recebido",
            "Investimento Retornado", "Comissão de Venda", "Rendimento Tesouro Direto"
        ]

        Receita.objects.all().delete()  # opcional: limpa as receitas antes

        total_criado = 0
        for _ in range(120):  # número de receitas fake
            descricao = random.choice(descricoes)
            valor = round(random.uniform(100, 5000), 2)

            # Gera datas aleatórias nos últimos 12 meses
            data = fake.date_between(start_date="-365d", end_date="today")

            Receita.objects.create(
                descricao=descricao,
                valor=valor,
                data=data
            )
            total_criado += 1

        self.stdout.write(self.style.SUCCESS(
            f"{total_criado} receitas criadas com sucesso!"))
