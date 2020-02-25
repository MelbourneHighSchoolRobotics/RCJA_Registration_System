from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.urls import reverse

from django.http import JsonResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
import datetime

from .models import *
from events.models import Division, Event

@login_required
def summary(request):
    invoices = Invoice.objects.filter(Q(invoiceToUser=request.user) | Q(school__schooladministrator__user=request.user)).distinct()

    context = {
        'user': request.user,
        'invoices': invoices,
    }

    return render(request, 'invoices/invoiceSummary.html', context)

@login_required
def detail(request, invoiceID):
    # Get invoice
    invoice = get_object_or_404(Invoice, pk=invoiceID)
    invoiceSettings = get_object_or_404(InvoiceGlobalSettings)

    # Check permissions
    if not (request.user.schooladministrator_set.filter(school=invoice.school).exists() or invoice.invoiceToUser == request.user):
        raise PermissionDenied("You do not have permission to view this invoice")

    # Set invoiced date
    if invoice.invoicedDate is None:
        invoice.invoicedDate = datetime.datetime.today()
        invoice.save()

    # Division details
    teams = invoice.teamsQueryset()
    enteredDivisions = Division.objects.filter(team__in=teams).distinct()

    invoiceItems = []
    overallTotalExclGST = 0
    overallTotalGST = 0
    overallTotalInclGST = 0

    for division in enteredDivisions:
        # Calculate values
        numberTeams = teams.filter(division=division).count()
        unitCost = invoice.event.entryFee
        totalExclGST = numberTeams * unitCost
        gst = 0.1 * totalExclGST
        totalInclGST = totalExclGST + gst

        # Update totals
        overallTotalExclGST += totalExclGST
        overallTotalGST += gst
        overallTotalInclGST += totalInclGST

        invoiceItems.append({
            'name': division.name,
            'numberTeams': numberTeams,
            'unitCost': unitCost,
            'totalExclGST': totalExclGST,
            'gst': gst,
            'totalInclGST': totalInclGST,
        })

    context = {
        'invoice': invoice,
        'invoiceSettings': invoiceSettings,
        'invoiceItems': invoiceItems,
        'overallTotalExclGST': overallTotalExclGST,
        'overallTotalGST': overallTotalGST,
        'overallTotalInclGST': overallTotalInclGST,
        'currentDate': datetime.datetime.today().date,
    }

    return render(request, 'invoices/invoiceDetail.html', context)

@login_required
def setInvoiceTo(request, invoiceID):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=invoiceID)

        # Check permissions
        if not (request.user.schooladministrator_set.filter(school=invoice.school).exists() or invoice.invoiceToUser == request.user):
            raise PermissionDenied("You do not have permission to view this invoice")
        
        invoice.invoiceToUser = request.user
        invoice.save(update_fields=['invoiceToUser'])

        return JsonResponse({'id':invoiceID, 'invoiceTo':request.user.fullname_or_email(), 'success':True})
    else:
        return HttpResponseForbidden()

@login_required
def setCampusInvoice(request, invoiceID):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=invoiceID)

        # Check permissions
        if not (request.user.schooladministrator_set.filter(school=invoice.school).exists() or invoice.invoiceToUser == request.user):
            raise PermissionDenied("You do not have permission to view this invoice")

        # Check campus invoicing available
        if not invoice.campusInvoicingAvailable():
            return HttpResponseForbidden("Campus invoicing not available for this event")

        # Create campus invoices for campuses that have teams entered in this event
        # This invoice object remains for teams without a campus
        from schools.models import Campus
        for campus in Campus.objects.filter(school=invoice.school, team__event=invoice.event):
            Invoice.objects.create(
                event=invoice.event,
                invoiceToUser=invoice.invoiceToUser,
                school=invoice.school,
                campus=campus,
            )

        return JsonResponse({'id':invoiceID, 'success':True})
    else:
        return HttpResponseForbidden()

@login_required
def editInvoicePOAJAX(request, invoiceID):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=invoiceID)

        # Check permissions
        if not (request.user.schooladministrator_set.filter(school=invoice.school).exists() or invoice.invoiceToUser == request.user):
            raise PermissionDenied("You do not have permission to view this invoice")

        # Update invoice
        try:
            invoice.purchaseOrderNumber = request.POST["PONumber"]
            invoice.save()
        except KeyError:
            return HttpResponseBadRequest()

        return JsonResponse({'id':invoiceID,'number':request.POST["PONumber"], 'success':True})
        #IF PO NUMBERS NEED AN ERROR RESPONSE
        """
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors.items())
            },status=400)
        """
    else:
        return HttpResponseForbidden()
