import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_telegram_message(message):
    """
    Отправка сообщения в Telegram
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    api_url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    try:
        response = requests.post(api_url, json={
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        })
        
        if response.status_code != 200:
            logger.error(f'Ошибка отправки в Telegram: {response.text}')
            return False
            
        return True
    except Exception as e:
        logger.error(f'Ошибка при отправке в Telegram: {str(e)}')
        return False

def format_contact_message(contact_request):
    """
    Форматирование сообщения для отправки
    """
    message = (
        f"📞 <b>Новая заявка с сайта!</b>\n\n"
        f"👤 Имя: {contact_request.name}\n"
        f"📱 Телефон: {contact_request.phone}\n"
    )
    
    if contact_request.product:
        message += f"🏭 Продукт: {contact_request.product.name}\n"
    
    message += f"\n⏰ Время заявки: {contact_request.created_at.strftime('%d.%m.%Y %H:%M')}"
    
    return message 