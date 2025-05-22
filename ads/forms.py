from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'condition', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class AdSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию или описанию'})
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Ad.objects.none(),
        label='Категория'
    )
    condition = forms.ChoiceField(
        required=False,
        choices=[('', 'Все')] + Ad.CONDITION_CHOICES,
        label='Состояние'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all() 