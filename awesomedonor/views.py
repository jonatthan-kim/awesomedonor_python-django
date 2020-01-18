from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class Intro1TV(TemplateView):
    template_name = 'intro1.html'

class Intro2TV(TemplateView):
    template_name = 'intro2.html'