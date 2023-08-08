from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from bot.models import Question
from core.models import Region


class QuestionAdminForm(forms.ModelForm):
    """Form for Question model admin class."""

    regions = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all().order_by("region_name"),
        label="Регионы",
        required=True,
        widget=FilteredSelectMultiple("Регионы", is_stacked=False),
    )

    class Meta:
        """Meta class."""

        model = Question
        widgets = {
            "answer": forms.Textarea,
        }
        fields = "__all__"
