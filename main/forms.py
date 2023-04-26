from django import forms
from .models import Task


class AddTaskForm(forms.Form):
    title = forms.CharField(max_length=269)
    description =  forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    def save(self, user):
        obj = Task.objects.create(title= self.cleaned_data['title'], 
                                description= self.cleaned_data['description'], 
                                user= user)
        obj.save()

        return obj

class EditTaskForm(forms.Form):
    title = forms.CharField(max_length=269)
    description =  forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    def save(self, obj):
        obj.title = self.cleaned_data['title']
        obj.description = self.cleaned_data['description']
        obj.save()

        return obj