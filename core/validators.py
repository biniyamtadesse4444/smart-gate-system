from django.utils import timezone
from core.models import Card, Reader
from payment.models import Payment


_card_cooldown = {}

SCAN_COOLSOWN_SECONDS = 15

def validate_card(card_id, reader_id):
    now = timezone.now()   

    
    try:
        card = Card.objects.select_related('customer').get(id=card_id)                 
    except Card.DoesNotExist:
        return {
            'time': now,
            'card': card_id,
            'customer': '-',
            'granted': False,
            'event': 'Invalid card',
            'status': '-',
            'reader': None,
            'door': None
        }
    
    
    
    reader = Reader.objects.get(pk=reader_id)
    
    
    
    customer = card.customer
    customer_name = f'{customer.first_name} {customer.last_name}' if customer else '-'
    
    result = {
        'time': now,
        'card': card.id,
        'customer': customer_name,
        'status': card.card_status,
        'event': 'Access Granted',
        'model': card.card_model,
        'type': card.card_type, 
        'granted': False,
        'reader': reader.pk,
        'door': reader.door.door                  
    }

    last_scan_time = _card_cooldown.get(card_id)

    if last_scan_time and (now - last_scan_time).total_seconds() < SCAN_COOLSOWN_SECONDS:
        result['event'] = 'Cooldown'
        return result
        
    if card.card_status == 'L':
        result['event'] = 'Lost Card'
        return result

    if card.card_status == 'I':
        result['event'] = 'Inactive Card'
        return result
    
    if not customer.is_active:
        result['event'] = 'Inactive customer'
        return result
    
    if card.card_type != "M":
        latest_payment = (
            Payment.objects.filter(customer = customer)
            .order_by('-end_date').first()
        )

        if not(latest_payment) or latest_payment.end_date < now.date():
            result['event'] = 'Not paid'
            return result
    
    
    _card_cooldown[card_id] = now
    result['granted'] = True
    return result

        
    
    
        