import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin.messaging import (
    Message,
    Notification,
    _MessagingService
)

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PVT_KEY_ID"),
    "private_key": os.getenv("PVT_KEY").replace(r'\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLNT_EMAIL_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("CERT_URL"),
    "universe_domain": "googleapis.com"
})

default_app = firebase_admin.initialize_app(cred)


def send_push_notification(title=None, body=None, fcm_tokens=None, notification_type=None, product_id=None):
    """
    Function for send push notification on a user device.
    """
    try:
        tokens = [fcm_tokens[i:i + 500] for i in range(0, len(fcm_tokens), 500)]

        for token_list in tokens:
            messages_list = [
                Message(
                    notification=Notification(
                        title=title,
                        body=body,
                    ),
                    token=user_token,
                    data={
                        "notification_type": notification_type,
                        "product_id": str(product_id)
                    }
                ) for user_token in token_list
            ]

            _MessagingService(default_app).send_all(
                messages=messages_list,
                dry_run=False
            )

    except BaseException as e:
        print("Push notification error ", str(e))

