from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SelectDateForm
from datetime import datetime
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import Procedure, Master, Record, VacantTimes, Message


def index(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
    procedure = Procedure.objects.all()
    return render(
        request,
        "index.html",
        {
            "procedures":
                procedure,
            "message": message
        }
    )


def vacant_dates(request, procedure_id):
    user1 = request.user.username
    vacant_dates_times = VacantTimes.objects.filter(procedure_id=procedure_id).order_by('vacant_date_time')[:5]
    procedure = Procedure.objects.get(pk=procedure_id)
    procedure_name = procedure.procedure_name
    procedure_master = procedure.master.fio
    procedure_price = procedure.price
    dateform = SelectDateForm()
    message = 'Ближайшие 5 окошек'
    if user1 != '':
        user = User.objects.get(username=user1)
        record_of_user = Record.objects.filter(user_id=user.id)
        return render(
            request,
            "vacant_dates.html",
            {
                "vacant_dates":
                    vacant_dates_times,
                "message": message,
                "procedure_name": procedure_name,
                "procedure_master": procedure_master,
                "procedure_price": procedure_price,
                "dateform": dateform,
                "latest_messages": Message.objects.filter(chat_id=procedure_id).order_by('-pub_date')[:5],
                "record_of_user": record_of_user,

            }
        )
    else:
        return render(
            request,
            "vacant_dates.html",
            {
                "vacant_dates":
                    vacant_dates_times,
                "message": message,
                "procedure_name": procedure_name,
                "procedure_master": procedure_master,
                "procedure_price": procedure_price,
                "dateform": dateform,
                "latest_messages": Message.objects.filter(chat_id=procedure_id).order_by('-pub_date')[:5],
            }
        )


def selected_date(request, procedure_id):
    user1 = request.user.username
    procedure = Procedure.objects.get(pk=procedure_id)
    procedure_name = procedure.procedure_name
    procedure_master = procedure.master.fio
    procedure_price = procedure.price
    dateform = SelectDateForm()
    new_date = request.GET.get("date", '29-08-2019')
    new_date1 = str(new_date)
    date1 = datetime.strptime(new_date1, '%d-%m-%Y')
    year = date1.year
    month = date1.month
    day = date1.day
    vacant_dates_times = VacantTimes.objects.filter(procedure_id=procedure_id,
                                                    vacant_date_time__year=year,
                                                    vacant_date_time__month=month,
                                                    vacant_date_time__day=day).order_by('vacant_date_time')
    if not vacant_dates_times:
        message = 'Свободных окошек на ' + new_date1 + ' нет'
    else:
        message = 'Свободные окошки на '+ new_date1
    if user1 != '':
        user = User.objects.get(username=user1)
        record_of_user = Record.objects.filter(user_id=user.id)
        return render(
            request,
            "vacant_dates.html",
            {
                "vacant_dates": vacant_dates_times,
                "procedure_name": procedure_name,
                "procedure_master": procedure_master,
                "procedure_price": procedure_price,
                "message1": message,
                "date": new_date1,
                "dateform": dateform,
                "latest_messages": Message.objects.filter(chat_id=procedure_id).order_by('-pub_date')[:5],
                "record_of_user": record_of_user,

            }
        )
    else:
        return render(
            request,
            "vacant_dates.html",
            {
                "vacant_dates": vacant_dates_times,
                "procedure_name": procedure_name,
                "procedure_master": procedure_master,
                "procedure_price": procedure_price,
                "message1": message,
                "date": new_date1,
                "dateform": dateform,
                "latest_messages": Message.objects.filter(chat_id=procedure_id).order_by('-pub_date')[:5],

            }
        )


def record(request, procedure_id, vacant_times_id):
    user1 = request.user.username
    user = User.objects.get(username=user1)
    vacant_time = VacantTimes.objects.get(pk=vacant_times_id)
    record_new = Record.objects.create(user_id=user.id,
                                       procedure_id=procedure_id,
                                       vacant_time=vacant_time.vacant_date_time)
    record_new.save()
    procedure = Procedure.objects.get(pk=procedure_id)
    procedure_name = procedure.procedure_name
    procedure_master = procedure.master.fio
    procedure_price = procedure.price
    vacant_times = VacantTimes.objects.get(pk=vacant_times_id)
    vacant_times.delete()
    message = 'ВЫ ЗАПИСАНЫ НА ПРОЦЕДУРУ'
    return render(
        request,
        "success_record.html",
        {
            "procedure_name": procedure_name,
            "procedure_master": procedure_master,
            "procedure_price": procedure_price,
            "date": vacant_time.vacant_date_time,
            "message": message,
        }
    )


def cancel_record(request, procedure_id, record_id):
    user1 = request.user.username
    user = User.objects.get(username=user1)
    canceled_record = Record.objects.get(pk=record_id)
    vacant_date_time = VacantTimes.objects.create(procedure_id=procedure_id,
                                                  vacant_date_time=canceled_record.vacant_time)
    vacant_date_time.save()
    procedure = Procedure.objects.get(pk=procedure_id)
    procedure_name = procedure.procedure_name
    procedure_master = procedure.master.fio
    procedure_price = procedure.price
    canceled_record.delete()
    message = 'ВАША ЗАПИСЬ ОТМЕНЕНА'
    return render(
        request,
        "success_record.html",
        {
            "procedure_name": procedure_name,
            "procedure_master": procedure_master,
            "procedure_price": procedure_price,
            "date": vacant_date_time.vacant_date_time,
            "message": message
        }
    )


app_url = "/pbs/"


def post(request, procedure_id):
    msg = Message()
    msg.author = request.user
    msg.chat = get_object_or_404(Procedure, pk=procedure_id)
    msg.message = request.POST['message']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url+'vacant_dates/'+str(procedure_id))


def msg_list(request, procedure_id):
    # выбираем список сообщений
    res = list(
            Message.objects
                # фильтруем по id загадки
                .filter(chat_id=procedure_id)
                # отбираем 5 самых свежих
                .order_by('-pub_date')[:5]
                # выбираем необходимые поля
                .values('author__username',
                        'pub_date',
                        'message'
                )
            )
    # конвертируем даты в строки - сами они не умеют
    for r in res:
        r['pub_date'] = \
            r['pub_date'].strftime(
                '%d.%m.%Y %H:%M:%S'
            )
    return JsonResponse(json.dumps(res), safe=False)


class RegisterFormView(FormView):
    # будем строить на основе
    # встроенной в django формы регистрации
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь
    # в случае успешной регистрации.
    # В данном случае указана ссылка на
    # страницу входа для зарегистрированных пользователей.
    success_url = app_url + "login/"
    # Шаблон, который будет использоваться
    # при отображении представления.
    template_name = "reg/register.html"

    def form_valid(self, form):
        # Создаём пользователя,
        # если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    # будем строить на основе
    # встроенной в django формы входа
    form_class = AuthenticationForm
    # Аналогично регистрации,
    # только используем шаблон аутентификации.
    template_name = "reg/login.html"
    # В случае успеха перенаправим на главную.
    success_url = app_url

    def form_valid(self, form):
        # Получаем объект пользователя
        # на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        # Выполняем выход для пользователя,
        # запросившего данное представление.
        logout(request)
        # После чего перенаправляем пользователя на
        # главную страницу.
        return HttpResponseRedirect(app_url)


class PasswordChangeView(FormView):
    # будем строить на основе
    # встроенной в django формы смены пароля
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    # после смены пароля нужно снова входить
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)
