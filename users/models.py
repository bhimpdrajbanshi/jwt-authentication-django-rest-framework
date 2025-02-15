import logging
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)

class User(AbstractUser):
    # Define membership types
    SILVER = 'Silver'
    GOLD = 'Gold'
    DIAMOND = 'Diamond'
    
    MEMBERSHIP_CHOICES = [
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (DIAMOND, 'Diamond'),
    ]
    
    # Additional fields
    username = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=10)
    membership_type = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_CHOICES,
        default=SILVER
    )
    membership_start_date = models.DateField(null=True, blank=True)
    membership_expiry_date = models.DateField(null=True, blank=True)
    
    REQUIRED_FIELDS = ['phone_number']
    
    def save(self, *args, **kwargs):
        logger.debug(f"Starting save for user {self.username}")
       
        # Automatically set the membership_start_date to today's date if not set
        if not self.membership_start_date:
            self.membership_start_date = timezone.now().date()
            logger.debug(f"Set membership_start_date for {self.username} to {self.membership_start_date}")
        
        # Set membership_expiry_date based on membership_type
        if not self.membership_expiry_date:
            if self.membership_type == self.SILVER:
                self.membership_expiry_date = self.membership_start_date + timedelta(days=365)  # 1 year
                logger.debug(f"Set membership_expiry_date for {self.username} to {self.membership_expiry_date} (Silver)")
            elif self.membership_type == self.GOLD:
                self.membership_expiry_date = self.membership_start_date + timedelta(days=365*2)  # 2 years
                logger.debug(f"Set membership_expiry_date for {self.username} to {self.membership_expiry_date} (Gold)")
            elif self.membership_type == self.DIAMOND:
                self.membership_expiry_date = self.membership_start_date + timedelta(days=365*5)  # 5 years
                logger.debug(f"Set membership_expiry_date for {self.username} to {self.membership_expiry_date} (Diamond)")


        super().save(*args, **kwargs)
        logger.debug(f"Successfully saved user {self.username}")
    def __str__(self):
        return "{}".format(self.username)
