from datetime import date, datetime, timedelta
from django.forms import ValidationError
from core.models import Customer
from payment.models import Article, Payment
from django.utils import timezone


def validate_payment(customer_id, article_id):

    today = timezone.now()
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        raise ValidationError('Customer Does not exist')
    
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise ValidationError('Article does not exist')
    
    payment = Payment.objects.filter(article_id=article.id)

    customer_start_payment = (
            Payment.objects.filter(customer = customer)
            .order_by('-end_date').first()
        )
    
    customer_end_payment = (
            Payment.objects.filter(customer = customer)
            .order_by('-start_date').first()
        )
    
    
    if customer_start_payment is None or customer_end_payment is None:
        return {
            'status': 'failed',
            'reason': 'Your first time payment should be in person'
        }
    MONTH = 9
    DAY = 5
    
    
    start_date = customer_end_payment.end_date
    # end_date = customer_end_payment.end_date
    final_start_date = start_date

    final_end_date = start_date + timedelta(days=article.duration)
    
    this_year = date(final_end_date.year, MONTH, DAY)
    print(final_start_date)
    print(final_end_date)    #end_date
    remaining_months = (this_year.year - start_date.year) * 12 + (this_year.month - start_date.month)

    
    print(this_year)
    print(final_end_date)
    if final_end_date > this_year and article.duration!=365:
        return {
            'status': 'failed',
            'reason': f'You should only pay {remaining_months} to include the month Puagume'
        }

    elif final_end_date == this_year:
        final_end_date += timedelta(days=5)
        print('inside local elif', final_end_date) 
    
    else:
        final_end_date = (start_date + timedelta(days=article.duration))
    
    
    print('outside fuction', final_end_date)
    

    
    
    
    
   
    
    
    # if final_end_date == this_year:
    #     final_end_date += timedelta(days=5)

    #     {
    #     'amount': article.unit_price,
    #     'currency': 'ETB',
    #     'phone_number':customer.phone_number,
    #     'first_name': customer.first_name,
    #     'last_name': customer.last_name,
    #     'status': 'success',
    #     'start_date': start_date,
    #     'end_date': end_date,
    #     'duration': article.duration,
    #     'article': article,
    #     'customer': customer,
    #     'n_start_date': final_start_date,
    #     'n_end_date': final_end_date,
    # }

    

    return {
        'amount': article.unit_price,
        'currency': 'ETB',
        'phone_number':customer.phone_number,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'status': 'success',
        # 'start_date': start_date,
        # 'end_date': end_date,
        'duration': article.duration,
        'article': article,
        'customer': customer,
        'n_start_date': final_start_date,
        'n_end_date': final_end_date,
    }


    
    