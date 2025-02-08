from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator
from .models import Product, Category, ContactRequest
from .forms import ContactRequestForm
from django.shortcuts import redirect
from django.contrib import messages
from .utils import send_telegram_message, format_contact_message

# Create your views here.

class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()[:3]  # Получаем 3 последних продукта
        context['contact_form'] = ContactRequestForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = form.save()
            
            # Форматируем и отправляем сообщение в Telegram
            message = format_contact_message(contact_request)
            if send_telegram_message(message):
                messages.success(request, 'Ваша заявка успешно отправлена!')
            else:
                messages.success(request, 'Ваша заявка принята, но возникли проблемы с уведомлением.')
                
        return redirect('home')

class CatalogListView(ListView):
    model = Product
    template_name = 'main/catalog.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactRequestForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            contact_request.product = self.get_object()
            contact_request.save()
            
            # Форматируем и отправляем сообщение в Telegram
            message = format_contact_message(contact_request)
            if send_telegram_message(message):
                messages.success(request, 'Ваша заявка успешно отправлена!')
            else:
                messages.success(request, 'Ваша заявка принята, но возникли проблемы с уведомлением.')
                
        return redirect('product_detail', pk=self.get_object().pk)
