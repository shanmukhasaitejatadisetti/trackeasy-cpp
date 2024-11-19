import requests
from datetime import datetime

def trigger_order_alert(order):
    """
    Trigger the Lambda API when a new order is created
    """
    api_url = "https://fnxq7zb0x1.execute-api.us-east-1.amazonaws.com/default/trackeasy-order-alert"
    
    # Format the delivery date to the required format (dd/mm/yyyy)
    delivery_date = order.preferred_delivery_date.strftime("%d/%m/%Y")
    
    payload = {
        "order_id": str(order.id),
        "username": order.user.username,
        "destination": order.destination,
        "goods_type": order.goods_type,
        "delivery_date": delivery_date
    }
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        return True, "Alert triggered successfully"
    except requests.exceptions.RequestException as e:
        return False, f"Failed to trigger alert: {str(e)}"