from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, ListView, TemplateView, View


class Home(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)
