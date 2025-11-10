"""
Mock Order model for testing Payment model

This is a placeholder Order model that allows Payment model to be tested
independently. Replace this with actual Order model when available.
"""

from django.db import models


class Order(models.Model):
    """
    Placeholder Order model for Payment model relationships
    
    This model can be extended with actual order fields as needed.
    """
    # Placeholder fields - can be extended as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id}"
