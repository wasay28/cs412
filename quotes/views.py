from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

quotes = ["Float like a butterfly, sting like a bee.", "It's not bragging if you can back it up.", "If you even dream of beating me you'd better wake up and apologize."]
images = ["https://cdn.britannica.com/86/192386-050-D7F3126D/Muhammad-Ali-American.jpg", "https://neilleifer.com/cdn/shop/products/4015_1200x.jpg?v=1658846705", "https://progressive.org/downloads/16443/download/Screen%20Shot%202021-09-17%20at%209.44.46%20AM.png?cb=649ba713f137c50508ff1666abafd9f8"]
