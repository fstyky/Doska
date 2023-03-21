from django import forms
from .models import Post, Replay


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'title': forms.TextInput(attrs={'size': '64'})}
        fields = ('category', 'title', 'text',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Категория:"
        self.fields['title'].label = "Заголовок"
        self.fields['text'].label = "Текст объявления:"


class ReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(ReplayForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Отклик:"


class ReplayFilterForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ReplayFilterForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.ModelChoiceField(
            label='Объявление',
            queryset=Post.objects.filter(author_id=user.id).order_by('-dateCreation').values_list('title', flat=True),
            empty_label="Все",
            required=False
        )