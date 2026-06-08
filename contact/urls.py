from django.urls import path
from .views import ContactListView, ContactView, test_smtp


urlpatterns = [

    path('contact/', ContactView.as_view(), name='contact'),
    path("contact/list/", ContactListView.as_view(), name="contacts"),
    path("smtp-test/", test_smtp),
]