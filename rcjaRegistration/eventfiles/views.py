from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# from .forms import 

from .models import MentorEventFileUpload
from events.models import BaseEventAttendance

from events.views import mentorEventAttendanceAccessPermissions

from .forms import MentorEventFileUploadForm

import datetime


class MentorEventFileUploadView(LoginRequiredMixin, View):
    def fileTypeEditAllowed(self, event, fileType):
        return event.eventavailablefiletype_set.filter(uploadDeadline__gte=datetime.datetime.today(), fileType=fileType).exists()

    def editPermissions(self, request, uploadedFile):
        # Check event is published
        if not uploadedFile.eventAttendance.event.published():
            raise PermissionDenied("Event is not published")

        # Check administrator of eventAttendance for this file
        if not mentorEventAttendanceAccessPermissions(request, uploadedFile.eventAttendance):
            raise PermissionDenied("You are not an administrator of this team/ attendee")

        # Check upload deadline not passed
        if not self.fileTypeEditAllowed(uploadedFile.eventAttendance.event, uploadedFile.fileType):
            raise PermissionDenied("The upload deadline has passed for this file type for this event")
        
        # Check team - file upload currently not implemented for workshop attendees
        if not uploadedFile.eventAttendance.eventAttendanceType() == 'team':
           raise PermissionDenied("File upload is only supported for teams") 

    def uploadPermissions(self, request, eventAttendance):
        # Check event is published
        if not eventAttendance.event.published():
            raise PermissionDenied("Event is not published")

        # Check administrator of this eventAttendance
        if not mentorEventAttendanceAccessPermissions(request, eventAttendance):
            raise PermissionDenied("You are not an administrator of this team/ attendee")

        # Check at least one available file type
        if not eventAttendance.event.eventavailablefiletype_set.filter(uploadDeadline__gte=datetime.datetime.today()).exists():
            raise PermissionDenied("File upload not available")

        # Check team - file upload currently not implemented for workshop attendees
        if not eventAttendance.eventAttendanceType() == 'team':
           raise PermissionDenied("File upload is only supported for teams") 

    def get_post_common(self, request, eventAttendanceID, uploadedFileID):
        # This page currently does not support viewing or editing existing files, so deny access if is not None
        # Can't edit uploaded files, so deny access if post with uploadedFileID
        if uploadedFileID is not None:
            raise PermissionDenied("Can't edit existing files")

        # Get eventAttendance object
        eventAttendance = get_object_or_404(BaseEventAttendance, pk=eventAttendanceID)

        # Check upload permissions
        self.uploadPermissions(request, eventAttendance)

        return eventAttendance


    def get(self, request, eventAttendanceID=None, uploadedFileID=None):
        eventAttendance = self.get_post_common(request, eventAttendanceID, uploadedFileID)

        context = {
            "eventAttendance": eventAttendance,
            "availableFileUploadTypes": eventAttendance.event.eventavailablefiletype_set.filter(uploadDeadline__gte=datetime.datetime.today()),
            "form": MentorEventFileUploadForm(eventAttendance=eventAttendance),
        }

        return render(request, 'eventfiles/uploadMentorEventFile.html', context)

    def post(self, request, eventAttendanceID=None, uploadedFileID=None):
        eventAttendance = self.get_post_common(request, eventAttendanceID, uploadedFileID)

        # Get form and check if valid
        form = MentorEventFileUploadForm(request.POST, request.FILES, eventAttendance=eventAttendance)

        if form.is_valid():
            # Create team object but don't save so can set foreign keys
            uploadedFile = form.save(commit=False)
            uploadedFile.eventAttendance = eventAttendance
            uploadedFile.uploadedBy = request.user

            # Save team
            uploadedFile.save()

            # Redirect to team details view
            return redirect(reverse('teams:details', kwargs = {"teamID": eventAttendance.id}))

        # Default to displaying the form again if form not valid
        context = {
            "eventAttendance": eventAttendance,
            "availableFileUploadTypes": eventAttendance.event.eventavailablefiletype_set.filter(uploadDeadline__gte=datetime.datetime.today()),
            "form": form,
        }

        return render(request, 'eventfiles/uploadMentorEventFile.html', context)

    def delete(self, request, eventAttendanceID=None, uploadedFileID=None):
        # This endpoint should never be called with eventAttendanceID
        if eventAttendanceID is not None:
            return HttpResponseForbidden()

        # Get uploadedFile object
        uploadedFile = get_object_or_404(MentorEventFileUpload, pk=uploadedFileID)

        # Check permissions
        self.editPermissions(request, uploadedFile)

        # Delete team
        uploadedFile.delete()
        return HttpResponse(status=204)
