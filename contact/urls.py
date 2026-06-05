from django.urls import path
from .views import ContactListView, ContactView


urlpatterns = [

    path('contact/', ContactView.as_view(), name='contact'),
    path("contact/list/", ContactListView.as_view(), name="contacts"),
]