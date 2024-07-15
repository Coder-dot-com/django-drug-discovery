from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from generate_molecules.models import GenerationRequest

# Create your views here.

@login_required
def list_of_requests(request):
    
    generation_requests = GenerationRequest.objects.filter(user=request.user).order_by('datetime_created').reverse()
    
    context = {
        'generation_requests': generation_requests,
    }
    
    return render(request, "list_of_requests.html", context=context)


@login_required
def render_molecules(request, uuid):
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid)
    
    
    
    context = {
        'generation_request': generation_request,
    }
    
    return render(request, 'render_molecules.html', context=context)