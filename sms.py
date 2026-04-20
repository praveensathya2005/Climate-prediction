from twilio.rest import Client

def send_sms(message, to_number):
    account_sid = "AC30d57b6edaf0cb376c65f45a12f69fe1"
    auth_token = "23d17836528a8e34110e4a7430162b9a"
    from_number = "+12293215605"

    # Remove emojis and special Unicode characters that Indian carriers block (DLT/Error 30044)
    clean_message = message.encode('ascii', 'ignore').decode('ascii').strip()

    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            body=clean_message,
            from_=from_number,
            to=to_number
        )
        return msg.sid
    except Exception as e:
        raise Exception(f"SMS failed to {to_number}: {str(e)}")