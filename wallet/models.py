from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from userhome.models import NewUser


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.user.first_name} : {self.balance}"

    @receiver(post_save, sender=NewUser)
    def create_wallet(sender, instance, created, **kwargs):
        if created:
            Wallet.objects.create(user=instance)


class WalletTransaction(models.Model):
    TRANSACTION_TYPE = [
        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
        ("Payment", "Payment"),
        ("Refund", "Refund"),
        ("Referal", "Referal"),
        ("Cashback", "Cashback"),
    ]
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(choices=TRANSACTION_TYPE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Transaction: Amount {self.amount} on {self.date}"
