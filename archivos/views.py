import uuid
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SubirForm
from .models import Archivo


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('lista')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required
def lista(request):
    if request.method == 'POST':
        form = SubirForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['archivo']
            Archivo.objects.create(propietario=request.user, nombre=f.name, archivo=f, tamano=f.size)
            messages.success(request, 'Archivo subido.')
            return redirect('lista')
    else:
        form = SubirForm()
    archivos = request.user.archivos.order_by('-subido')
    return render(request, 'archivos/lista.html', {'form': form, 'archivos': archivos})


def _enviar(a):
    try:
        return FileResponse(a.archivo.open('rb'), as_attachment=True, filename=a.nombre)
    except FileNotFoundError:
        raise Http404


@login_required
def descargar(request, pk):
    return _enviar(get_object_or_404(Archivo, pk=pk, propietario=request.user))


def publico(request, token):
    return _enviar(get_object_or_404(Archivo, token=token, compartido=True))


@login_required
@require_POST
def compartir(request, pk):
    a = get_object_or_404(Archivo, pk=pk, propietario=request.user)
    a.compartido = not a.compartido
    if a.compartido:
        a.token = uuid.uuid4()  # enlace nuevo cada vez que se activa
    a.save(update_fields=['compartido', 'token'])
    return redirect('lista')


@login_required
@require_POST
def eliminar(request, pk):
    a = get_object_or_404(Archivo, pk=pk, propietario=request.user)
    a.archivo.delete(save=False)
    a.delete()
    return redirect('lista')
