from django.shortcuts import render

# Create your views here.


def main(request):
    
    template_name = 'restaurant/main.html'
    
    context = {

    }

    return render(request, template_name, context)

def order(request):
    ''''Respond to the URL '', delegate work to a template.'''

    template_name = 'restaurant/order.html'

    # dict of context variables
    context = {

    }
    return render(request, template_name, context)  

def confirmation(request):
    ''''Respond to the URL '', delegate work to a template.'''

    template_name = 'restaurant/confirmation.html'
    # dict of context variables
    context = {

    }
    return render(request, template_name, context) 
