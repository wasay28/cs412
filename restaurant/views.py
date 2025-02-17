from django.shortcuts import render
from django.utils.timezone import now, timedelta
import random

def main(request):
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    template_name = 'restaurant/order.html'
    
    
    context = {
        "daily_special": "Butter Chicken with Naan",
        "special_price": 18,
    }
    
    return render(request, template_name, context)

def confirmation(request):
    if request.method == "POST":
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        instructions = request.POST.get("instructions")
        items = request.POST.getlist("items")

        # Calculate total price
        prices = {
            "Chicken Biryani": 12,
            "Mutton Biryani": 15,
            "Vegetable Biryani": 10,
            "Daily Special": 18,
        }
        total_price = sum(prices[item] for item in items)

        
        ready_time = now() + timedelta(minutes=random.randint(30, 60))

        
        context = {
            "name": name,
            "email": email,
            "instructions": instructions,
            "items": items,
            "total_price": total_price,
            "ready_time": ready_time.strftime("%I:%M %p"),
        }

        template_name = 'restaurant/confirmation.html'
        return render(request, template_name, context)
    
    return render(request, 'restaurant/order.html')  
