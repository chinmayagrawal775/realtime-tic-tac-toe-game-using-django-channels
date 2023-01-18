from django import forms

class PlayerForm(forms.Form):
    player_name = forms.CharField(
        label='Your name',
        max_length=25,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    i_have_game_code = forms.BooleanField(
        widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    
    game_code = forms.CharField(
        label='Game Code',
        max_length=6,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )