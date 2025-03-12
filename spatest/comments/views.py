from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from config import Config
from services import MediaManager, TextManager

from .forms import CommentForm
from .models import Comment, FileUpload, File, User

# Create your views here.


class CommentView(TemplateView):
    template_name = "comments/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all().order_by("-id")[:25]
        context.update({"form": CommentForm, "comments": comments})
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        parent_id = kwargs.get("parent_id", None)
        form = CommentForm(self.request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data("email")).first()
            if not user:
                user = User(
                    username=form.cleaned_data("username"),
                    email=form.cleaned_data("email"),
                    home_page=form.cleaned_data("home_page")
                )
                user.save()

            file = form.cleaned_data("file")
            if file:
                form.save(commit=False)
                latest_file = FileUpload.objects.latest('id')
                file_path = latest_file.get_file_path()
                config = Config()
                manager: MediaManager | TextManager = MediaManager(config, file_path)
                if manager.allowed_type:
                    file_path = manager.save()
                else:
                    manager = TextManager(config, file_path)
                    if manager.allowed_type and manager.check_max_size():
                        file_path = manager.save()

            file = File(file_path=file_path, hash_sum=manager.hash_sum)
            file.save()

            comment = Comment(
                parent_id=parent_id,
                user=user,
                text=form.cleaned_data("text"),
                file=file,
            )
            comment.save()
            return HttpResponseRedirect(reverse_lazy("/"))

        else:
            context.update({"form": form})
            return self.render_to_response(context)
