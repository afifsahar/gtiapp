from django import forms
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class choiceForm(forms.ModelForm):

    class Meta:
        model = wo_description
        fields = ['area', 'categoryService']

        # widgets = {
        #     'area': forms.SelectMultiple(attrs={'id': "area", 'name': 'area', 'label': 'Area', 'help text': 'Area', 'required': 'True', 'autocomplete': 'off', 'class': "form-control"}),
        #     'categoryService': forms.SelectMultiple(attrs={'id': "categoryService", 'name': 'categoryService', 'label': 'Category Service', 'help text': 'Category Service', 'required': 'True', 'autocomplete': 'off', 'class': "form-control"}),
        # }
    # = forms.ChoiceField(choices=grs, initial='jabatan',)

    # grs = [(gr.id, gr) for gr in User.objects.filter(groups__name='maker')]
    # grs.insert(0, ('', '--- Petugas OSP ---'))
    # woUser = forms.ChoiceField(choices=grs, initial='WO User',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields["area"].widget.attrs.update(
    #         {'type': "checkbox", 'id': "area", 'name': 'area', 'label': 'Area', 'help text': 'Area', 'required': 'True', 'autocomplete': 'off',})
    #     self.fields["categoryService"].widget.attrs.update(
    #         {'type': "checkbox",'id': "categoryService", 'name': 'categoryService', 'label': 'Category Service', 'help text': 'Category Service', 'required': 'True', 'autocomplete': 'off',})


class descriptionForm(forms.ModelForm):

    class Meta:
        model = wo_description
        fields = ['description', 'woUser']

    # grs = [(gr.id, gr) for gr in User.objects.filter(groups__name='maker')]
    # grs.insert(0, ('', '--- Petugas OSP ---'))
    # woUser = forms.ChoiceField(choices=grs, initial='WO User',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget.attrs.update(
            {'type': "text", 'id': "description", 'name': 'description', 'label': 'Description', 'help text': 'Description', 'required': 'True', 'autocomplete': 'off', 'height': "200", 'rows': '3'})
        self.fields["woUser"].widget.attrs.update(
            {'id': "woUser", 'name': 'woUser', 'label': 'Petugas OSP (Maker)', 'help text': 'Petugas OSP (Maker)', 'required': 'True', 'autocomplete': 'off', 'class': "form-control", })


class workorderForm(forms.ModelForm):

    class Meta:
        model = wo_workorder
        fields = ['workorder', 'duration', 'dueDate']
        widgets = {
            'dueDate': forms.DateInput(format=('%m/%d/%Y'), attrs={'type': "date", 'id': "dueDate", 'name': 'dueDate', 'required': 'True', 'autocomplete': 'off', 'label': 'Due Date', 'help text': 'Due Date', 'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["workorder"].widget.attrs.update(
            {'type': "text", 'id': "workorder", 'name': 'workorder', 'required': 'True', 'autocomplete': 'off', 'label': 'Work Order', 'help text': 'Work Order', 'height': "200", 'rows': '3'})
        self.fields["duration"].widget.attrs.update(
            {'type': "text", 'id': "duration", 'name': 'duration', 'required': 'True', 'autocomplete': 'off', 'label': 'Duration', 'help text': 'Duration'})
        # self.fields["dueDate"].widget.attrs.update(
        #     {})


class rincianForm(forms.ModelForm):

    class Meta:
        model = wo_rincian
        fields = ['date',  'status', 'information']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["date"].widget.attrs.update(
            {'type': "date", 'id': "date", 'name': 'date', 'required': 'True', 'autocomplete': 'off', 'label': 'Date', 'help text': 'Date'})
        self.fields["status"].widget.attrs.update(
            {'type': "text", 'id': "status", 'name': 'status', 'required': 'True', 'autocomplete': 'off', 'label': 'Status', 'help text': 'Status'})
        self.fields["information"].widget.attrs.update(
            {'type': "text", 'id': "information", 'name': 'information', 'required': 'True', 'autocomplete': 'off', 'label': 'Information', 'help text': 'Information'})
