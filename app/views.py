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
    """
        Renders the home page with the URL form and list of stored URLs.
    """
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        """
        Adds URL form and stored data to context.

        Returns:
            dict: Context data including form and URLs.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = UrlsForm()
        context['data'] = Urls.objects.all()
        return context



class URLShortener(View):
    """
    Handles URL shortening and stores the shortened URL in the database.
    """
    form = UrlsForm()

    def post(self, request):
        """
        Shortens a URL, stores it, and returns the result.

        Args:
            request: The HTTP request with the full URL.

        Returns:
            HttpResponse: The rendered page with the shortened URL and data.
        """
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
    """
    Redirects to the original URL based on the shortened URL and tracks clicks.
    """

    def get_redirect_url(self, *args, **kwargs):
        """
        Redirects to the full URL and increments click count.

        Args:
            *args: Additional positional arguments.
            **kwargs: Shortened URL slug.

        Returns:
            str: The full URL or an error page URL.
        """
        short_url = kwargs.get('short_url')
        try:
            # Fetch the URL object from URLs model
            url_obj = Urls.objects.get(shortened_url=short_url)
            # Increment click by 1
            url_obj.clicks += 1
            url_obj.save()
            # Return the original url
            return url_obj.full_url
        except ObjectDoesNotExist:
            return reverse('error')

class ErrorView(TemplateView):
    """
    Renders an error page when a shortened URL does not exist.
    """
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        """
        Adds an error message to the context.

        Returns:
            dict: Context data with the error message.
        """
        context = super().get_context_data(**kwargs)
        # Pass the message for error page.
        context['message'] = 'The shortened URL does not exist or has expired.'
        return context

class DeleteURL(View):
    """
    Deletes a URL entry from the database.
    """
    form = UrlsForm()

    def post(self, request, short_url):
        """
        Deletes the URL entry by its shortened URL slug.

        Args:
            request: The HTTP request.
            short_url: The shortened URL slug to delete.

        Returns:
            HttpResponse: The rendered page with a success or error message.
        """
        try:
            # Fetch url object from URLs model
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
