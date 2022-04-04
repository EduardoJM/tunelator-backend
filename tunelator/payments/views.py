from rest_framework import views, response
from django.shortcuts import render

class MercadoPagoWebHook(views.APIView):
    permission_classes = []
    
    def post(self, request):
        print(request.data)
        return response.Response()

def test(request):
    return render(request, 'demo/demo.html')
