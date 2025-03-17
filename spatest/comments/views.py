from typing import Any, Optional

from django.core.paginator import Paginator
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
        comments_list = Comment.objects.all().order_by("-id")
        paginator = Paginator(comments_list, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context.update({"form": CommentForm(), "comments": page_obj})
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        parent_id = kwargs.get("parent_id", None)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            user, _ = User.objects.get_or_create(
                email=form.cleaned_data["email"],
                defaults=dict(
                    username=form.cleaned_data["username"],
                    home_page=form.cleaned_data["home_page"],
                )
            )

            file = form.cleaned_data["file"]
            file_path: Optional[str] = None
            if file:
                file_upload = FileUpload(file=file)
                file_upload.save()
                file_path = file_upload.file.path

            if file_path:
                config = Config()
                manager: MediaManager | TextManager = MediaManager(config, file_path)
                if manager.allowed_type:
                    file_path = manager.save()
                else:
                    manager = TextManager(config, file_path)
                    if manager.allowed_type and manager.check_max_size():
                        file_path = manager.save()

                file_instance = File(file_path=file_path, hash_sum=manager.hash_sum)
                file_instance.save()

            comment = Comment(
                parent_id=parent_id,
                user=user,
                text=form.cleaned_data["text"],
            )
            comment.save()

            if file_instance:
                comment.files.add(file_instance)
            return HttpResponseRedirect(reverse_lazy("comments:index"))

        else:
            context.update({"form": form})
            return self.render_to_response(context)
