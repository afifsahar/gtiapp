from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class areaForm(forms.ModelForm):

    class Meta:
        model = mendc_area
        fields = ['namaArea']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["namaArea"].widget.attrs.update(
            {'type': "text", 'id': "namaArea", 'name': 'area', 'label': 'Nama Area', 'help text': 'Nama Area'})


class subareaForm(forms.ModelForm):

    class Meta:
        model = mendc_subarea
        fields = ['namaSubarea']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["namaSubarea"].widget.attrs.update(
            {'type': "text", 'id': "namaSubarea", 'class': "formset-field", 'name': 'subarea'})


class dailyForm(forms.ModelForm):

    class Meta:
        model = mendc_daily
        fields = ['kondisi',  'hasilTemuan', 'keterangan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["kondisi"].widget.attrs.update(
            {'id': "kondisi", 'name': 'kondisi', 'class': 'custom-select',
                'label': 'kondisi', 'help text': 'kondisi', 'placeholder': 'Kondisi'})
        self.fields["keterangan"].widget.attrs.update(
            {'id': "keterangan", 'name': 'keterangan',
                'label': 'keterangan', 'help text': 'keterangan', 'height': "200", 'placeholder': 'Keterangan', 'rows': '3'})
        self.fields["hasilTemuan"].widget.attrs.update(
            {'id': "hasilTemuan", 'name': 'hasilTemuan', 'label': 'Hasil Temuan', 'help text': 'Hasil Temuan', 'placeholder': 'Hasil Temuan', 'rows': '3'})


class defaultForm(forms.ModelForm):

    class Meta:
        model = mendc_default
        fields = ['defaultKondisi',  'defaultHasilTemuan', 'defaultKeterangan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["defaultKondisi"].widget.attrs.update(
            {'id': "kondisi", 'name': 'kondisi', 'class': 'custom-select',
                'label': 'kondisi', 'help text': 'kondisi', 'placeholder': 'Kondisi'})
        self.fields["defaultKeterangan"].widget.attrs.update(
            {'id': "keterangan", 'name': 'keterangan',
                'label': 'keterangan', 'help text': 'keterangan', 'height': "200", 'placeholder': 'Keterangan', 'rows': '3'})
        self.fields["defaultHasilTemuan"].widget.attrs.update(
            {'id': "hasilTemuan", 'name': 'hasilTemuan', 'label': 'Hasil Temuan', 'help text': 'Hasil Temuan', 'placeholder': 'Hasil Temuan', 'rows': '3'})
