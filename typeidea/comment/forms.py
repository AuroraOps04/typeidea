import mistune
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    email = forms.CharField(
        label='EMail',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'},
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'},
        )
    )
    content = forms.CharField(
        label='内容',

        widget=CKEditorWidget(),
        required=True,
    )

    def clean_content(self):
        content = self.cleaned_data.get("content")

        if len(content) < 10:
            raise forms.ValidationError("内容长度怎么能这么短呢.")
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']


class PostForm(forms.ModelForm):
    content = forms.CharField(
        label="正文",
        required=True,
        widget=CKEditorWidget(),
    )