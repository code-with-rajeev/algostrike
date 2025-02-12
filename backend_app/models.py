from django.db import models

# Create your models here.

class OHLC(models.Model):
    symbol = models.CharField(max_length=50, db_index=True)  # Index for filtering by symbol
    timeframe = models.CharField(max_length=10, db_index=True)  # Index for filtering by timeframe
    timestamp = models.DateTimeField(db_index=True)  # Index for sorting by time
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['symbol', 'timeframe', '-timestamp']),  # Composite index
        ]