from django import forms
from .tasks import send_feedback_email_task


class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )

    def send_email(self):
        send_feedback_email_task.apply_async(args=[
            self.cleaned_data["email"], self.cleaned_data["message"]
        ]
        )
