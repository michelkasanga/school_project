from .models import Contact

def contact_context(request):
    contacts = None
    try:
        contacts = Contact.objects.only('id', 'email', 'address').first()
    except Contact.DoesNotExist:
        contacts= None
        
    return {"contact":contacts}