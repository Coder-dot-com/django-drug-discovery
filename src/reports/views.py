from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report
from django.shortcuts import render, HttpResponse, get_object_or_404

# Create your views here.
@login_required
def list_of_reports(request):
    
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()
    
    context = {
        'reports': reports,
    }
    
    return render(request, "list_of_reports.html", context=context)


@login_required
def view_report(request, uuid):
    report = get_object_or_404(Report, user=request.user, uuid=uuid)
    
    molecules = report.molecules.all()
    molecule_count = molecules.count()
    
    

    context = {
        'report': report,
        'molecules': molecules,
        'molecule_count': molecule_count,
        
    }
    
    return render(request, 'view_report.html', context=context)