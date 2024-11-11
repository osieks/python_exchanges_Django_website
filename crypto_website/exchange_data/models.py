from django.db import models

# Create your models here.
class BinanceData(models.Model):
    #datapoint_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    timestamp = models.BigIntegerField(db_index=True)  # Storing Unix timestamp as an integer
    
    def __str__(self):
        return f"{self.symbol} - {self.price} at {self.timestamp}"
    
    class Meta:
        unique_together = ['symbol', 'timestamp']
        indexes = [
            models.Index(fields=['symbol', 'timestamp'])
        ]