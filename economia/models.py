from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Receita(models.Model):
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f} em {self.data}"


class Investimento(models.Model):
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"


class Despesa(models.Model):
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    investimento = models.ForeignKey(
        Investimento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="despesas",
        verbose_name="Investimento relacionado"
    )

    def __str__(self):
        ref = f" (via {self.investimento.descricao})" if self.investimento else ""
        return f"{self.descricao} - R$ {self.valor:.2f}{ref}"


# --- Sinais automáticos para movimentação de investimentos ---
@receiver(post_save, sender=Despesa)
def debitar_investimento(sender, instance, created, **kwargs):
    if created and instance.investimento:
        inv = instance.investimento
        if inv.valor >= instance.valor:
            inv.valor -= instance.valor
            inv.save()
        else:
            raise ValueError(
                "Saldo insuficiente no investimento para essa despesa!")


@receiver(post_delete, sender=Despesa)
def estornar_investimento(sender, instance, **kwargs):
    if instance.investimento:
        inv = instance.investimento
        inv.valor += instance.valor
        inv.save()

class ContasPagar(models.Model):
    descricao = models.CharField(max_length=200, verbose_name="Descrição", help_text="Descrição da conta a pagar")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor", help_text="Valor da conta a pagar")
    vencimento = models.DateField(verbose_name="Vencimento", help_text="Data de vencimento da conta a pagar")
    pago = models.BooleanField(default=False, verbose_name="Pago", help_text="Status de pagamento da conta a pagar")
    recorrente = models.BooleanField(default=False, verbose_name="Recorrente", help_text="Indica se a conta é recorrente")

    def __str__(self):
        status = "Pago" if self.pago else "Pendente"
        rec = "🔁" if self.recorrente else ""
        return f"{rec} {self.descricao} - R$ {self.valor:.2f} ({status})"
    
    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"

