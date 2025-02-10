from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

quotes = ["'Float like a butterfly, sting like a bee.'", 
          "'It's not bragging if you can back it up.'", 
          "'If you even dream of beating me you'd better wake up and apologize.'",
          "'I am the greatest, I said that even before I knew I was.'",
          "'I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'",
          "'I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.'",
          "'I should be a postage stamp. That's the only way I'll ever get licked.'",
          "'I'm not the greatest, I'm the double greatest.'"
          ]

images = ["https://cdn.britannica.com/86/192386-050-D7F3126D/Muhammad-Ali-American.jpg", 
          "https://neilleifer.com/cdn/shop/products/4015_1200x.jpg?v=1658846705", 
          "https://progressive.org/downloads/16443/download/Screen%20Shot%202021-09-17%20at%209.44.46%20AM.png?cb=649ba713f137c50508ff1666abafd9f8",
          "https://s.hdnux.com/photos/46/67/03/10186971/6/ratio1x1_1920.jpg",
          "https://sothebys-com.brightspotcdn.com/dims4/default/ee7b9c9/2147483647/strip/true/crop/450x665+0+0/resize/684x1011!/quality/90/?url=http%3A%2F%2Fsothebys-brightspot-migration.s3.amazonaws.com%2F04%2F05%2F9e%2Ff9a0f206dc58d4918953416f22a7829019d81961746bbb1ddca5df5074%2Fmuhammad-ali-1.jpg",
          "https://i.guim.co.uk/img/static/sys-images/Sport/Pix/pictures/2010/10/26/1288106969209/Muhammad-Ali-006.jpg?width=465&dpr=1&s=none&crop=none"
             
          
          ]

def main(request):
    template_name = 'quotes/quote.html'

    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    
    context = {
        'quote': random_quote,
        'image': random_image,
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def quote(request):
    
    template_name = 'quotes/quote.html'

    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    
    context = {
        'quote': random_quote,
        'image': random_image,
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def show_all(request):
    ''''Respond to the URL '', delegate work to a template.'''

    template_name = 'quotes/show_all.html'

    # dict of context variables
    context = {
        'quotes': quotes,
        'images': images,
        "time": time.ctime(),
    }
    return render(request, template_name, context)  

def about(request):
    ''''Respond to the URL '', delegate work to a template.'''

    template_name = 'quotes/about.html'
    # dict of context variables
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)  