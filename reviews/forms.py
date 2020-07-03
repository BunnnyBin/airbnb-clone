from django import forms
from . import models

class CreateReviewForm(forms.ModelForm):
    #ModelForm에서 일반 Form처럼 field를 설정(세부설정)
    accuracy = forms.IntegerField(max_value=5, min_value=1) #form validation
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False) # database에 저장x
        return review