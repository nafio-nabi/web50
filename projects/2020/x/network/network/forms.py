from django import forms

class NewPostForm(forms.Form):
    post =  forms.CharField(label="New Post", required=True, max_length=320, widget=forms.Textarea(attrs={"placeholder": "Write your post here.", "class": "form-control", "rows": 5}))