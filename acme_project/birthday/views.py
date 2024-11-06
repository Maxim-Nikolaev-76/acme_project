# from django.core.paginator import Paginator
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
    )
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404, redirect, render
from .forms import BirthdayForm
from .utils import calculate_birthday_countdown
from .models import Birthday
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# class BirthdayMixin:
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


# class BirthdayFormMixin:
#     form_class = BirthdayForm
#     # template_name = 'birthday/birthday.html'

@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    form_class = BirthdayForm
    model = Birthday
    # # fields = '__all__'
    # # Указываем имя формы:
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    form_class = BirthdayForm
    model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    # pass
    model = Birthday
    success_url = reverse_lazy('birthday:list')
    # Шаблон с именем birthday/birthday_confirm_delete.html
    # подключается автоматически, согласно правилу:
    # <<имя-модели_confirm_delete.html>>.


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday,
        )
        # Возвращаем словарь контекста.
        return context


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10
