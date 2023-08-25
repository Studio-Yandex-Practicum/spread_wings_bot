from django import forms

from bot.models import FundProgram, Question


class QuestionAdminForm(forms.ModelForm):
    """Form for Question model admin class."""

    class Meta:
        """Meta class."""

        model = Question
        widgets = {
            "answer": forms.Textarea(attrs={"rows": 10, "cols": 80}),
            "regions": forms.CheckboxSelectMultiple,
        }
        fields = "__all__"


class FundProgramForm(forms.ModelForm):
    """Form for FundProgram model admin class."""

    class Meta:
        """Meta class."""

        models = FundProgram
        widgets = {
            "regions": forms.CheckboxSelectMultiple,
        }
        fields = "__all__"
