from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from django.core.files.storage import FileSystemStorage

from invoices.models import InvoiceGlobalSettings
from users.models import User
from regions.models import State, Region
from schools.models import School, SchoolAdministrator, Campus
from events.models import Event, Year, Division, AvailableDivision
from coordination.models import Coordinator
from teams.models import Team, Student, HardwarePlatform, SoftwarePlatform

from .models import MentorEventFileType, MentorEventFileUpload, EventAvailableFileType

import datetime

def newCommonSetUp(self):
        self.state1 = State.objects.create(typeRegistration=True, name='Victoria', abbreviation='VIC')
        self.state2 = State.objects.create(typeRegistration=True, name='NSW', abbreviation='NSW')
        self.region1 = Region.objects.create(name='Test Region', description='test desc')

        self.user1 = User.objects.create_user(email=self.email1, password=self.password, homeState=self.state1)
        self.user2 = User.objects.create_user(email=self.email2, password=self.password, homeState=self.state1)
        self.user3 = User.objects.create_user(email=self.email3, password=self.password, homeState=self.state2)
        self.superUser = User.objects.create_user(email=self.email_superUser, password=self.password, is_superuser=True, is_staff=True, homeState=self.state1)

        self.school1 = School.objects.create(name='School 1', abbreviation='sch1', state=self.state1, region=self.region1)
        self.school2 = School.objects.create(name='School 2', abbreviation='sch2', state=self.state1, region=self.region1)
        self.school3 = School.objects.create(name='School 3', abbreviation='sch3', state=self.state2, region=self.region1)

        self.year = Year.objects.create(year=2020)
        self.event = Event.objects.create(
            year=self.year,
            state=self.state1,
            name='Test event 1',
            eventType='competition',
            status='published',
            maxMembersPerTeam=5,
            entryFeeIncludesGST=True,
            event_billingType='team',
            event_defaultEntryFee = 50,
            startDate=(datetime.datetime.now() + datetime.timedelta(days=5)).date(),
            endDate = (datetime.datetime.now() + datetime.timedelta(days=5)).date(),
            registrationsOpenDate = (datetime.datetime.now() + datetime.timedelta(days=-10)).date(),
            registrationsCloseDate = (datetime.datetime.now() + datetime.timedelta(days=1)).date(),
            directEnquiriesTo = self.user1,
        )
        self.division1 = Division.objects.create(name='Division 1')
        self.division2 = Division.objects.create(name='Division 2')
        self.division3 = Division.objects.create(name='Division 3')
        self.division4 = Division.objects.create(name='Division 4', state=self.state2)

        self.invoiceSettings = InvoiceGlobalSettings.objects.create(
            invoiceFromName='From Name',
            invoiceFromDetails='Test Details Text',
            invoiceFooterMessage='Test Footer Text',
        )

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.team2 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 2', division=self.division1)

class Base_Test_MentorEventFileUploadView(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'
    
    def url(self, objID):
        pass

    def setUp(self):
        newCommonSetUp(self)

        self.docFile = SimpleUploadedFile("doc.doc", b"file_content", content_type="application/msword")
        self.pdfFile = SimpleUploadedFile("pdf.pdf", b"file_content", content_type="application/pdf")
        self.jpegFile = SimpleUploadedFile("jpeg.jpeg", b"file_content", content_type="	image/jpeg")

        self.fileType1 = MentorEventFileType.objects.create(name="File Type 1")

        self.availableFileType1 = EventAvailableFileType.objects.create(event=self.event, fileType=self.fileType1, uploadDeadline=(datetime.datetime.now() + datetime.timedelta(days=5)).date())

    def createFile(self):
        return MentorEventFileUpload.objects.create(eventAttendance=self.team1, fileType=self.fileType1, fileUpload=self.docFile, originalFilename="doc.doc", uploadedBy=self.user2)

class Test_MentorEventFileUploadView_LoginRequired(Base_Test_MentorEventFileUploadView):
    def testNewFileGet(self):
        response = self.client.get(reverse('eventfiles:uploadFile', kwargs={'eventAttendanceID':self.team1.id}))
        self.assertEqual(response.url, f"/accounts/login/?next=/teams/{self.team1.id}/uploadFile")
        self.assertEqual(response.status_code, 302)

    @patch('storages.backends.s3boto3.S3Boto3Storage.save', return_value='string')
    def testExistingFileGet(self, mock_save):
        self.uploadedFile1 = self.createFile()

        response = self.client.get(reverse('eventfiles:edit', kwargs={'uploadedFileID':self.uploadedFile1.id}))
        self.assertEqual(response.url, f"/accounts/login/?next=/eventfiles/{self.uploadedFile1.id}/edit")
        self.assertEqual(response.status_code, 302)
