from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Ad, ExchangeProposal

class AdTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category'
        )
        self.ad = Ad.objects.create(
            title='Тестовое объявление',
            description='Описание тестового объявления',
            category=self.category,
            condition='new',
            user=self.user
        )
    
    def test_ad_list_view(self):
        response = self.client.get(reverse('ad-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_list.html')
        self.assertContains(response, 'Тестовое объявление')
    
    def test_ad_detail_view(self):
        response = self.client.get(reverse('ad-detail', args=[self.ad.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ad_detail.html')
        self.assertContains(response, 'Тестовое объявление')
    
    def test_ad_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('ad-create'), {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': self.category.pk,
            'condition': 'new'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Новое объявление').exists())
    
    def test_ad_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('ad-update', args=[self.ad.pk]), {
            'title': 'Обновленное объявление',
            'description': 'Обновленное описание',
            'category': self.category.pk,
            'condition': 'good'
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Обновленное объявление')
    
    def test_ad_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('ad-delete', args=[self.ad.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        self.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category'
        )
        self.ad1 = Ad.objects.create(
            title='Объявление 1',
            description='Описание 1',
            category=self.category,
            condition='new',
            user=self.user1
        )
        self.ad2 = Ad.objects.create(
            title='Объявление 2',
            description='Описание 2',
            category=self.category,
            condition='good',
            user=self.user2
        )
    
    def test_create_proposal(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('ad-propose', args=[self.ad2.pk]),
            {'comment': 'Предложение обмена'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ExchangeProposal.objects.filter(
                ad_sender=self.ad1,
                ad_receiver=self.ad2
            ).exists()
        )
    
    def test_proposal_status_update(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тестовое предложение'
        )
        
        # Тест принятия предложения
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('proposal-accept', args=[proposal.pk])
        )
        self.assertEqual(response.status_code, 200)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')
        
        # Тест отклонения предложения
        proposal.status = 'pending'
        proposal.save()
        response = self.client.post(
            reverse('proposal-reject', args=[proposal.pk])
        )
        self.assertEqual(response.status_code, 200)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'rejected')
