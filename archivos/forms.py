from django import forms

MAX_MB = 20


class SubirForm(forms.Form):
    archivo = forms.FileField()

    def clean_archivo(self):
        f = self.cleaned_data['archivo']
        if f.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f'El archivo supera {MAX_MB} MB.')
        return f