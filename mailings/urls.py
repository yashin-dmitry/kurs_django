from django.urls import path
from .views import (
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    SendMailingView, HomeView, SendMailingFormView, MailingAttemptListView
)

urlpatterns = [
    # URL-адреса для клиентов
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    # URL-адреса для сообщений
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    # URL-адреса для рассылок
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/send/<int:pk>/', SendMailingView.as_view(), name='send_mailing'),
    path('mailings/send/', SendMailingFormView.as_view(), name='send_mailing_form'),
    path('mailings/attempts/<int:pk>/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),

    # URL-адрес для главной страницы
    path('', HomeView.as_view(), name='home'),
]
