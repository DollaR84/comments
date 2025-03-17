"""Comments forms

"""
import re
from typing import Any, Optional

from django import forms
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):
    username = forms.CharField(max_length=50, label="username", help_text="Enter your own username")
    email = forms.EmailField(label="email", help_text="Enter your own email")
    home_page = forms.UrlField(required=False, label="home page", help_text="Enter your own home page")
    text = forms.CharField(widget=forms.Textarea, label="text comment", help_text="Enter your own comment")
    file = forms.FileField(required=False, label="file", help_text="Enter your own file")

    def clean_username(self) -> str:
        data: str = self.cleaned_data['username']
        if not re.search(r"^[A-Za-z0-9]+$", data):
            ValidationError("invalid username")
        return data

    def clean_email(self) -> str:
        data: str = self.cleaned_data['email']
        return data

    def clean_home_page(self) -> Optional[str]:
        data: Optional[str] = self.cleaned_data['home_page']
        return data

    def clean_text(self) -> str:
        data: str = self.cleaned_data['text']
        closing_tag: Optional[str] = None
        for tag in re.findall(r"<[^>]*>", data):
            if closing_tag:
                if tag != closing_tag:
                    ValidationError(f"There is no closing tag: '{closing_tag}'")
                closing_tag = None

            elif tag == "<strong>":
                closing_tag = "</strong>"
            elif tag == "<i>":
                closing_tag = "</i>"
            elif tag == "<code>":
                closing_tag = "</code>"
            elif tag.startswith("<a "):
                if "title" not in tag:
                    ValidationError("attribute 'title' for tag '<a>' is needed")
                closing_tag = "</a>"
            else:
                ValidationError(f"tag '{tag}' is not valid")
        return data

    def clean_file(self) -> Any:
        data = self.cleaned_data['file']
        return data
