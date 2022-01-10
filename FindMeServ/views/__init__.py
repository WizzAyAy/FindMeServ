from .addServer import *
from .serverList import *


def home(request):
    return render(request, '../templates/base.html')
