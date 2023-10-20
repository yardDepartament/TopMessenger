from django.db import models
from django.contrib.auth.models import User
from cryptography.hazmat.primitives import serialization
from .generate_rsa_pair import generate_rsa_key_pair


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key = models.TextField()
    
    def set_private_key(self, private_key):
        self.private_key = private_key

    def set_public_key(self, public_key):
        self.public_key = public_key

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key

    def generate_key_pair(self):
        private_key, public_key = generate_rsa_key_pair()
        self.set_private_key(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
        )
        self.set_public_key(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        )
    
    def __str__(self):
        return self.user.username
    
    
class Chat(models.Model):
    name = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    participants = models.ManyToManyField(UserProfile, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
