from django.db import models
import os

# Create your models here.


from django.db import models

class ChattingModel(models.Model):
    sender_mail = models.EmailField()
    receiver_mail = models.EmailField()
    text = models.TextField()
    share_files = models.FileField(upload_to='sharedFiles/', null=True, blank=True)
    sender_chat_id = models.CharField(max_length=100, null=True)
    receiver_chat_id = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['timestamp']
        db_table = 'ChattingModel'

    def __str__(self):
        return f"Message from {self.sender_mail} to {self.receiver_mail} at {self.timestamp}"
