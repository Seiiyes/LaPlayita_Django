from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from .models import Pqrs, PqrsHistorial
from .forms import PqrsForm, PqrsUpdateForm
from clients.models import Cliente
from users.decorators import check_user_role


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pqrs_list(request):
    if request.method == 'POST':
        form = PqrsForm(request.POST)
        if form.is_valid():
            pqrs = form.save(commit=False)
            cliente_id = request.POST.get('cliente')
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                pqrs.cliente = cliente
                pqrs.usuario = request.user
                pqrs.fecha_creacion = timezone.now()
                pqrs.save()
                messages.success(request, 'PQRS creado exitosamente.')
                return redirect(reverse('pqrs:pqrs_list'))
            except Cliente.DoesNotExist:
                messages.error(request, f'No se encontró un cliente con el ID {cliente_id}.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = PqrsForm()

    pqrs_query = Pqrs.objects.select_related('cliente', 'usuario').order_by('-fecha_creacion')
    query = request.GET.get('q')
    if query:
        pqrs_query = pqrs_query.filter(            
            models.Q(cliente__nombres__icontains=query) |
            models.Q(cliente__apellidos__icontains=query) |
            models.Q(tipo__icontains=query) |
            models.Q(estado__icontains=query)
        )

    clientes = Cliente.objects.all()
    context = {
        'pqrs': pqrs_query,
        'form': form,
        'clientes': clientes,
    }
    return render(request, 'pqrs/pqrs_list.html', context)


@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pqrs_detail(request, pk):
    pqrs = get_object_or_404(Pqrs, pk=pk)
    historial = PqrsHistorial.objects.filter(pqrs=pqrs).order_by('-fecha_cambio')
    form = PqrsUpdateForm(instance=pqrs)
    context = {
        'pqrs': pqrs,
        'historial': historial,
        'form': form,
    }
    return render(request, 'pqrs/pqrs_detail.html', context)

@login_required
@check_user_role(allowed_roles=['Administrador', 'Vendedor'])
def pqrs_update(request, pk):
    pqrs = get_object_or_404(Pqrs, pk=pk)
    if request.method == 'POST':
        form = PqrsUpdateForm(request.POST, instance=pqrs)
        if form.is_valid():
            estado_anterior = pqrs.estado
            pqrs_actualizado = form.save()
            estado_nuevo = pqrs_actualizado.estado

            if estado_anterior != estado_nuevo:
                descripcion_cambio = form.cleaned_data.get('descripcion_cambio')
                if not descripcion_cambio:
                    messages.error(request, 'Debe proporcionar una observación para el cambio de estado.')
                    return redirect('pqrs:pqrs_detail', pk=pk)
                
                PqrsHistorial.objects.create(
                    pqrs=pqrs_actualizado,
                    usuario=request.user,
                    estado_anterior=estado_anterior,
                    estado_nuevo=estado_nuevo,
                    descripcion_cambio=descripcion_cambio,
                    fecha_cambio=timezone.now()
                )
            
            messages.success(request, 'PQRS actualizado exitosamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    return redirect(reverse('pqrs:pqrs_detail', kwargs={'pk': pk}))

@never_cache
@login_required
@require_POST
@check_user_role(allowed_roles=['Administrador'])
def pqrs_delete(request, pk):
    pqrs = get_object_or_404(Pqrs, pk=pk)
    pqrs.delete()
    return JsonResponse({'message': 'PQRS eliminado exitosamente.'})