from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.products.models import Product


@receiver(post_save, sender=Product)
def sync_transaction_on_collect(sender, instance, **kwargs):
    """When a product is marked collected, complete its pending transaction."""
    if instance.status == 'collected':
        from apps.transactions.models import Transaction
        Transaction.objects.filter(
            product=instance,
            status='pending'
        ).update(status='completed')
