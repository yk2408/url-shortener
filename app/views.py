import random
import string
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, RedirectView

from .forms import UrlsForm
from .models import Urls
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UrlsForm()
        context['data'] = Urls.objects.all()
        return context



class URLShortener(View):
    form = UrlsForm()

    def post(self, request):

        # Fetch the full url
        url = request.POST.get("full_url")
        # Create a random string
        url_slug = ''.join(random.choice(string.ascii_letters)
                       for _ in range(10))
        # Create an entry in the database
        Urls.objects.create(full_url=url, shortened_url=url_slug)
        # Fetch all the available url data to render on the page
        data = Urls.objects.all()
        context={
            "form": self.form,
            "data": data,
            "shortened_url": url_slug
        }
        return render(request, "index.html", context=context)


class RedirectURLView(RedirectView):


    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs.get('short_url')
        try:
            url_obj = Urls.objects.get(shortened_url=short_url)
            url_obj.clicks += 1
            url_obj.save()
            return url_obj.full_url
        except ObjectDoesNotExist:
            return reverse('error')  # Replace with the URL for your error page

class ErrorView(TemplateView):
    template_name = 'error.html'

    # Optionally, you can pass custom context here if needed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'The shortened URL does not exist or has expired.'
        return context

class DeleteURL(View):
    form = UrlsForm()

    def post(self, request, short_url):
        try:
            url_obj = Urls.objects.get(shortened_url=short_url)
            url_obj.delete()  # Delete the URL object from the database
            message = f"URL with slug '{short_url}' has been deleted successfully."
        except ObjectDoesNotExist:
            message = f"URL with slug '{short_url}' does not exist."

        # Fetch updated data
        data = Urls.objects.all()

        # Render the page with a message and the updated data
        context = {
            "form": self.form,
            "data": data,
            "message": message
        }

        return render(request, "index.html", context=context)
