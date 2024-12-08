from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm

# Контроллеры для CRUD-операций над моделью Client
class ClientListView(LoginRequiredMixin, View):
    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def get(self, request):
        clients = Client.objects.all()
        return render(request, 'mailings/client_list.html', {'clients': clients})

class ClientCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ClientForm()
        return render(request, 'mailings/client_form.html', {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'mailings/client_form.html', {'form': form})

class ClientUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(instance=client)
        return render(request, 'mailings/client_form.html', {'form': form})

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'mailings/client_form.html', {'form': form})

class ClientDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return redirect('client_list')

# Контроллеры для CRUD-операций над моделью Message
class MessageListView(LoginRequiredMixin, View):
    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def get(self, request):
        messages = Message.objects.all()
        return render(request, 'mailings/message_list.html', {'messages': messages})

class MessageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'mailings/message_form.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
        return render(request, 'mailings/message_form.html', {'form': form})

class MessageUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(instance=message)
        return render(request, 'mailings/message_form.html', {'form': form})

    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
        return render(request, 'mailings/message_form.html', {'form': form})

class MessageDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return redirect('message_list')

# Контроллеры для CRUD-операций над моделью Mailing
class MailingListView(LoginRequiredMixin, View):
    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def get(self, request):
        mailings = Mailing.objects.all()
        return render(request, 'mailings/mailing_list.html', {'mailings': mailings})

class MailingCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = MailingForm()
        return render(request, 'mailings/mailing_form.html', {'form': form})

    def post(self, request):
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            return redirect('mailing_list')
        return render(request, 'mailings/mailing_form.html', {'form': form})

class MailingUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(instance=mailing)
        return render(request, 'mailings/mailing_form.html', {'form': form})

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing_list')
        return render(request, 'mailings/mailing_form.html', {'form': form})

class MailingDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.delete()
        return redirect('mailing_list')

# Контроллер для отправки рассылки
class SendMailingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        for client in mailing.clients.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    'from@example.com',
                    [client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response='OK'
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e)
                )
        mailing.status = 'Запущена'
        mailing.save()
        return redirect('mailing_list')

# Контроллер для отображения формы отправки рассылки
class SendMailingFormView(LoginRequiredMixin, View):
    def get(self, request):
        mailings = Mailing.objects.filter(status='Создана')
        return render(request, 'mailings/send_mailing.html', {'mailings': mailings})

    def post(self, request):
        mailing_id = request.POST.get('mailing')
        mailing = get_object_or_404(Mailing, pk=mailing_id)
        for client in mailing.clients.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    'from@example.com',
                    [client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response='OK'
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e)
                )
        mailing.status = 'Запущена'
        mailing.save()
        return redirect('mailing_list')

# Контроллер для отображения попыток отправки рассылки
class MailingAttemptListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        attempts = MailingAttempt.objects.filter(mailing=mailing)
        return render(request, 'mailings/mailing_attempt_list.html', {'mailing': mailing, 'attempts': attempts})

# Контроллер для главной страницы
class HomeView(View):
    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Запущена').count()
        unique_clients = Client.objects.count()
        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
        }
        return render(request, 'mailings/home.html', context)
