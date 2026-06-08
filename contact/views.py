import threading
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Contact
from .serializers import ContactSerializer
import resend
from django.conf import settings

def send_contact_email(name, email, subject, message):
    try:
        resend.api_key = settings.RESEND_API_KEY

        response = resend.Emails.send({
            "from": "PortfolioContact@resend.dev",
            "to": ["amar.dash989@gmail.com"],
            "subject": f"Portfolio Contact - {subject}",
            "text": f"""
Name: {name}
Email: {email}

Subject: {subject}

Message:
{message}
"""
        })

        print("RESEND RESPONSE:", response)

    except Exception as e:
        print("RESEND ERROR:", str(e))
        raise

import socket
from django.http import JsonResponse

def test_smtp(request):
    try:
        socket.create_connection(("smtp.gmail.com", 587), timeout=10)
        return JsonResponse({"status": "connected"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

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