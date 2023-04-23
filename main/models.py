from django.db import models
import uuid
import hashlib

def generate_pub_id():
    return hashlib.sha256(str(instance.id).encode()).hexdigest()

class User(models.Model):
    # an id for sequrity!
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    # an id for cookies!
    public_id = models.CharField(max_length=64, unique=True, editable=False)
    name = models.CharField(max_length=120)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # generate the cookie id
        if not self.public_id:
            data = f'{self.id}:{self.name}:{self.date_joined}'
            self.public_id = hashlib.sha256(data.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name.capitalize())


class Task(models.Model):
    STATES = [(True, 'Done'), (False, 'In progress')]

    title = models.CharField(max_length=260)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.BooleanField(choices=STATES, default=False)

    def __str__(self):
        return str(self.title)
