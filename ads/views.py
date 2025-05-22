from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ad, Category, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm, AdSearchForm
from .serializers import (
    AdSerializer, CategorySerializer, ExchangeProposalSerializer,
    UserSerializer
)

# Web Views
class AdListView(ListView):
    """
    Представление для отображения списка объявлений.
    
    Attributes:
        model (Ad): Модель объявления
        template_name (str): Путь к шаблону
        context_object_name (str): Имя переменной контекста
        paginate_by (int): Количество объявлений на странице
    
    Methods:
        get_queryset: Возвращает отфильтрованный QuerySet объявлений
        get_context_data: Добавляет форму поиска в контекст
    """
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 12
    
    def get_queryset(self):
        """
        Фильтрует объявления на основе параметров поиска.
        
        Returns:
            QuerySet: Отфильтрованный список объявлений
        """
        queryset = Ad.objects.all()
        form = AdSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            condition = form.cleaned_data.get('condition')
            
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
            if category:
                queryset = queryset.filter(category=category)
            if condition:
                queryset = queryset.filter(condition=condition)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Добавляет форму поиска в контекст шаблона.
        
        Returns:
            dict: Контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context['search_form'] = AdSearchForm(self.request.GET)
        return context

class AdDetailView(DetailView):
    """
    Представление для отображения детальной информации об объявлении.
    
    Attributes:
        model (Ad): Модель объявления
        template_name (str): Путь к шаблону
        context_object_name (str): Имя переменной контекста
    
    Methods:
        get_context_data: Добавляет форму предложения обмена в контекст
    """
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
    
    def get_context_data(self, **kwargs):
        """
        Добавляет форму предложения обмена в контекст для авторизованных пользователей.
        
        Returns:
            dict: Контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['proposal_form'] = ExchangeProposalForm()
        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового объявления.
    
    Attributes:
        model (Ad): Модель объявления
        form_class (AdForm): Класс формы
        template_name (str): Путь к шаблону
        success_url (str): URL для перенаправления после успешного создания
    
    Methods:
        form_valid: Сохраняет объявление и добавляет сообщение об успехе
    """
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad-list')
    
    def form_valid(self, form):
        """
        Сохраняет объявление и устанавливает текущего пользователя как автора.
        
        Args:
            form (AdForm): Валидная форма объявления
        
        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        form.instance.user = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования объявления.
    
    Attributes:
        model (Ad): Модель объявления
        form_class (AdForm): Класс формы
        template_name (str): Путь к шаблону
    
    Methods:
        get_queryset: Возвращает только объявления текущего пользователя
        get_success_url: Возвращает URL для перенаправления после успешного обновления
        form_valid: Сохраняет изменения и добавляет сообщение об успехе
    """
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    
    def get_queryset(self):
        """
        Возвращает только объявления текущего пользователя.
        
        Returns:
            QuerySet: Объявления текущего пользователя
        """
        return Ad.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления.
        
        Returns:
            str: URL детальной страницы объявления
        """
        return reverse_lazy('ad-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """
        Сохраняет изменения и добавляет сообщение об успехе.
        
        Args:
            form (AdForm): Валидная форма объявления
        
        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        messages.success(self.request, 'Объявление успешно обновлено!')
        return super().form_valid(form)

class AdDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления объявления.
    
    Attributes:
        model (Ad): Модель объявления
        template_name (str): Путь к шаблону
        success_url (str): URL для перенаправления после успешного удаления
    
    Methods:
        get_queryset: Возвращает только объявления текущего пользователя
        delete: Удаляет объявление и добавляет сообщение об успехе
    """
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad-list')
    
    def get_queryset(self):
        """
        Возвращает только объявления текущего пользователя.
        
        Returns:
            QuerySet: Объявления текущего пользователя
        """
        return Ad.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """
        Удаляет объявление и добавляет сообщение об успехе.
        
        Args:
            request (HttpRequest): Запрос
            *args: Дополнительные аргументы
            **kwargs: Дополнительные именованные аргументы
        
        Returns:
            HttpResponse: Ответ с перенаправлением
        """
        messages.success(request, 'Объявление успешно удалено!')
        return super().delete(request, *args, **kwargs)

@login_required
def create_exchange_proposal(request, pk):
    """
    Представление для создания предложения обмена.
    
    Args:
        request (HttpRequest): Запрос
        pk (int): ID объявления
    
    Returns:
        HttpResponse: Ответ с перенаправлением
    """
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = request.user.ad_set.first()
            proposal.ad_receiver = ad
            proposal.save()
            messages.success(request, 'Предложение обмена успешно отправлено!')
            return redirect('ad-detail', pk=pk)
    return redirect('ad-detail', pk=pk)

# API Views
class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с объявлениями через API.
    
    Attributes:
        queryset (QuerySet): Набор объявлений
        serializer_class (AdSerializer): Класс сериализатора
        permission_classes (list): Список классов разрешений
        filter_backends (list): Список бэкендов фильтрации
        filterset_fields (list): Поля для фильтрации
        search_fields (list): Поля для поиска
        ordering_fields (list): Поля для сортировки
    
    Methods:
        perform_create: Сохраняет объявление и устанавливает текущего пользователя как автора
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'condition']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    
    def perform_create(self, serializer):
        """
        Сохраняет объявление и устанавливает текущего пользователя как автора.
        
        Args:
            serializer (AdSerializer): Сериализатор объявления
        """
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с категориями через API.
    
    Attributes:
        queryset (QuerySet): Набор категорий
        serializer_class (CategorySerializer): Класс сериализатора
        permission_classes (list): Список классов разрешений
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с предложениями обмена через API.
    
    Attributes:
        serializer_class (ExchangeProposalSerializer): Класс сериализатора
        permission_classes (list): Список классов разрешений
    
    Methods:
        get_queryset: Возвращает предложения обмена текущего пользователя
        accept: Принимает предложение обмена
        reject: Отклоняет предложение обмена
    """
    serializer_class = ExchangeProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Возвращает предложения обмена текущего пользователя.
        
        Returns:
            QuerySet: Предложения обмена текущего пользователя
        """
        user = self.request.user
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        )
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Принимает предложение обмена.
        
        Args:
            request (HttpRequest): Запрос
            pk (int): ID предложения обмена
        
        Returns:
            Response: Ответ с результатом операции
        """
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response({'error': 'Недостаточно прав'}, status=403)
        proposal.status = 'accepted'
        proposal.save()
        return Response({'status': 'accepted'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Отклоняет предложение обмена.
        
        Args:
            request (HttpRequest): Запрос
            pk (int): ID предложения обмена
        
        Returns:
            Response: Ответ с результатом операции
        """
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response({'error': 'Недостаточно прав'}, status=403)
        proposal.status = 'rejected'
        proposal.save()
        return Response({'status': 'rejected'})
