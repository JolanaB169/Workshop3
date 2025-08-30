from django.http import HttpRequest
from django.shortcuts import render


"""
View function for the home page of the website.

Args:
    request (HttpRequest): The HTTP request object sent by the browser.

Returns:
    HttpResponse: Rendered HTML response using the 'home.html' template.
"""


# Renders the 'home.html' template with no additional context
def home_page_view(request: HttpRequest):
    return render(request, 'home.html')