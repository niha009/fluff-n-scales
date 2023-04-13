from .models import Pet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.generic import RedirectView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index(request):
    return render(request, 'catalog/index.html')


class PetDetail(DetailView):
    model = Pet
    template_name = 'catalog/pet_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        total_likes = obj.get_total_likes()
        total_dislikes = obj.get_total_dislikes()
        context['total_likes'] = total_likes
        context['total_dislikes'] = total_dislikes
        context['liked'] = False
        context['disliked'] = False
        if self.request.user.is_authenticated:
            if obj.likes.filter(id=self.request.user.id).exists():
                context['liked'] = True
            if obj.dislikes.filter(id=self.request.user.id).exists():
                context['disliked'] = True
        return context


@method_decorator(login_required, name='dispatch')
class LikePet(LoginRequiredMixin, CreateView):
    model = Pet
    fields = []
    template_name = 'catalog/pet_like.html'

    def post(self, request, pk, *args, **kwargs):
        pet = get_object_or_404(Pet, pk=pk)
        if pet.likes.filter(id=request.user.id).exists():
            pet.likes.remove(request.user)
        else:
            pet.likes.add(request.user)
            pet.dislikes.remove(request.user)
        return redirect('pet_image_list')


@method_decorator(login_required, name='dispatch')
class DislikePet(LoginRequiredMixin, CreateView):
    model = Pet
    fields = []
    template_name = 'catalog/pet_dislike.html'

    def post(self, request, pk, *args, **kwargs):
        pet = get_object_or_404(Pet, pk=pk)
        if pet.dislikes.filter(id=request.user.id).exists():
            pet.dislikes.remove(request.user)
        else:
            pet.dislikes.add(request.user)
            pet.likes.remove(request.user)
        return redirect('pet_image_list')


class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['pet_name', 'pet_image', 'description']
    success_url = reverse_lazy('pet_image_list')

    def form_valid(self, form):
        # Set the uploaded_user field to the first name of the logged-in user
        form.instance.uploaded_user = self.request.user.username
        return super().form_valid(form)


class PetUpdate(UpdateView):
    model = Pet
    fields = ['pet_name', 'pet_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('pet_list'))


def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    pet.delete()
    messages.success(request, (pet.pet_name + " has been deleted"))
    return redirect('pet_list')


def pet_image_list(request):
    pets = Pet.objects.exclude(pet_image='').order_by('pet_name')
    return render(request, 'catalog/pet_image_list.html', {'pets': pets})


class PetListView(LoginRequiredMixin, generic.ListView):
    model = Pet
    template_name = 'catalog/pet_list.html'
    login_url = 'login'

    def get_queryset(self):
        return Pet.objects.filter(user=self.request.user)


