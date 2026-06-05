import threading
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Contact
from .serializers import ContactSerializer


def send_contact_email(name, email, subject, message):
    email_body = f"""
Name: {name}
Email: {email}

Subject: {subject}

Message:
{message}
"""
    send_mail(
        subject=f"Portfolio Contact - {subject}",
        message=email_body,
        from_email=None,
        recipient_list=["amar7102k3@gmail.com"],
        fail_silently=True, 
    )


class ContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")

        if not all([name, email, subject, message]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        contact = Contact.objects.create(
            name=name, email=email, subject=subject, message=message
        )

        # Fire and forget — response returns immediately
        thread = threading.Thread(
            target=send_contact_email,
            args=(name, email, subject, message),
            daemon=True
        )
        thread.start()

        return Response(
            {"message": "Message sent successfully", "id": contact.id},
            status=status.HTTP_201_CREATED
        )

class ContactListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.all().order_by("-created_at")
        serializer = ContactSerializer(contacts, many=True)

        return Response(
            {
                "count": contacts.count(),
                "contacts": serializer.data
            },
            status=status.HTTP_200_OK
        )