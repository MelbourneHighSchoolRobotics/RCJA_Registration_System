from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.core.exceptions import ValidationError

from invoices.models import InvoiceGlobalSettings, Invoice, InvoicePayment
from users.models import User
from regions.models import State, Region
from schools.models import School, SchoolAdministrator, Campus
from events.models import Event, Year, Division, AvailableDivision
from coordination.models import Coordinator
from .models import Team, Student

import datetime
# Create your tests here.

def commonSetUp(obj): #copied from events, todo refactor
    obj.username = 'user@user.com'
    obj.password = 'password'
    obj.user = user = User.objects.create_user(email=obj.username, password=obj.password)
    obj.newState = State.objects.create(
        treasurer=obj.user,
        name='Victoria',
        abbreviation='VIC'
    )
    obj.newRegion = Region.objects.create(
        name='Test Region',
        description='test desc'
    )
    obj.newSchool = School.objects.create(
        name='Melbourne High',
        abbreviation='MHS',
        state=obj.newState,
        region=obj.newRegion
    )
    obj.schoolAdministrator = SchoolAdministrator.objects.create(
        school=obj.newSchool,
        user=obj.user
    )
    obj.year = Year.objects.create(year=2019)
    obj.division = Division.objects.create(name='test')

    obj.oldEvent = Event.objects.create(
        year=obj.year,
        state=obj.newState,
        name='test old not reg',
        maxMembersPerTeam=5,
        event_defaultEntryFee = 4,
        startDate=(datetime.datetime.now() + datetime.timedelta(days=-1)).date(),
        endDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).date(),
        registrationsOpenDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).date(),
        registrationsCloseDate = (datetime.datetime.now() + datetime.timedelta(days=-1)).date(),
        directEnquiriesTo = obj.user     
    )
    obj.oldEvent.divisions.add(obj.division)

    obj.newEvent = Event.objects.create(
        year=obj.year,
        state=obj.newState,
        name='test new not reg',
        maxMembersPerTeam=5,
        event_defaultEntryFee = 4,
        startDate=(datetime.datetime.now() + datetime.timedelta(days=3)).date(),
        endDate = (datetime.datetime.now() + datetime.timedelta(days=4)).date(),
        registrationsOpenDate = (datetime.datetime.now() + datetime.timedelta(days=-2)).date(),
        registrationsCloseDate = (datetime.datetime.now() + datetime.timedelta(days=+2)).date(),
        directEnquiriesTo = obj.user     
    )
    obj.newEvent.divisions.add(obj.division)

    obj.oldEventWithTeams = Event.objects.create(
        year=obj.year,
        state=obj.newState,
        name='test old yes reg',
        maxMembersPerTeam=5,
        event_defaultEntryFee = 4,
        startDate=(datetime.datetime.now() + datetime.timedelta(days=-3)).date(),
        endDate = (datetime.datetime.now() + datetime.timedelta(days=-4)).date(),
        registrationsOpenDate = (datetime.datetime.now() + datetime.timedelta(days=-6)).date(),
        registrationsCloseDate = (datetime.datetime.now() + datetime.timedelta(days=-5)).date(),
        directEnquiriesTo = obj.user     
    )
    obj.oldEventWithTeams.divisions.add(obj.division)
    obj.oldEventTeam = Team.objects.create(event=obj.oldEventWithTeams, division=obj.division, school=obj.newSchool, mentorUser=obj.user, name='test')
    obj.oldTeamStudent = Student(team=obj.oldEventTeam,firstName='test',lastName='old',yearLevel=1,gender='Male',birthday=datetime.datetime.now().date())
    
    obj.newEventTeam = Team.objects.create(event=obj.newEvent, division=obj.division, school=obj.newSchool, mentorUser=obj.user, name='test new team')
    obj.newTeamStudent = Student(team=obj.newEventTeam,firstName='test',lastName='thisisastringfortesting',yearLevel=1,gender='Male',birthday=datetime.datetime.now().date())

    login = obj.client.login(request=HttpRequest(), username=obj.username, password=obj.password) 

class TestAddTeam(TestCase): #TODO more comprehensive tests
    
    def setUp(self):
        commonSetUp(self)
        
    def testOpenRegoDoesLoad(self):
        response = self.client.get(reverse('teams:create',kwargs={'eventID':self.newEvent.id}))
        self.assertEqual(200, response.status_code)

    def testClosedRegoReturnsError(self):
        response = self.client.get(reverse('teams:create',kwargs={'eventID':self.oldEvent.id}))
        self.assertEqual(403, response.status_code)

    def testMaxSubmissionNumber(self):
        response = self.client.get(reverse('teams:create',kwargs={'eventID':self.newEvent.id}))
        self.assertContains(response,'First name', self.newEvent.maxMembersPerTeam)

    def testWorkingTeamCreate(self):
        payload = {
            'student_set-TOTAL_FORMS':1,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.newEvent.maxMembersPerTeam,
            "name":"test+team",
            "division":self.division.id,
            "school":self.newSchool.id,
            "student_set-0-firstName":"test",
            "student_set-0-lastName":"test",
            "student_set-0-yearLevel":"1",
            "student_set-0-birthday":"1111-11-11",
            "student_set-0-gender":"male"
        }
        response = self.client.post(reverse('teams:create',kwargs={'eventID':self.newEvent.id}),data=payload,follow=False)
        self.assertEqual(302,response.status_code)

    def testInvalidTeamCreate(self):
        payload = {
            'student_set-TOTAL_FORMS':1,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.newEvent.maxMembersPerTeam,
            "name":"test+team",
            "division":self.division.id,
            "student_set-0-firstName":"test",
            "student_set-0-lastName":"test",
            "student_set-0-yearLevel":"test",
            "student_set-0-birthday":"1111-11-11",
            "student_set-0-gender":"male"
        }
        response = self.client.post(reverse('teams:create',kwargs={'eventID':self.newEvent.id}),data=payload)
        self.assertEqual(200,response.status_code)
        """TODO this tests fails for some reason 

    def testTeamIsDeleted(self):
        payload = {'teamID':self.newEventTeam.id}
        response = self.client.post(reverse('teams:delete'),data=payload)
        print(self.newEventTeam.id)
        self.assertEqual(200,response.status_code)
        self.assertEqual(self.newEventTeam,None)
        """

class TestEditTeam(TestCase):
    def setUp(self):
        commonSetUp(self)

    def testOpenEditDoesLoad(self):
        response = self.client.get(reverse('teams:edit',kwargs={'teamID':self.newEventTeam.id}))
        self.assertEqual(200, response.status_code)
  
    def testClosedEditReturnsError(self):
        response = self.client.get(reverse('teams:edit',kwargs={'teamID':self.oldEventTeam.id}))
        self.assertEqual(403, response.status_code)    
        """
        def testEditLoadsPreviousData(self):
            response = self.client.get(reverse('teams:edit',kwargs={'teamID':self.newEventTeam.id}))
            #print(response)
        self.assertEqual(response.context['form'].initial['student_set-0-lastName'], 'thisisastringfortesting')   """

    def testEditStudentSucceeds(self):
        payload = {
            'student_set-TOTAL_FORMS':1,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.newEvent.maxMembersPerTeam,
            "name":"test+team",
            "division":self.division.id,
            "school":self.newSchool.id,
            "student_set-0-firstName":"teststringhere",
            "student_set-0-lastName":"test",
            "student_set-0-yearLevel":"1",
            "student_set-0-birthday":"1111-11-11",
            "student_set-0-gender":"male"
        }
        response = self.client.post(reverse('teams:edit',kwargs={'teamID':self.newEventTeam.id}),data=payload)

        self.assertEquals(Student.objects.get(firstName="teststringhere").firstName,"teststringhere")
        self.assertEquals(302,response.status_code)

    def testEditStudentWithInvalidFails(self):
        payload = {
            'student_set-TOTAL_FORMS':1,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.newEvent.maxMembersPerTeam,
            "name":"test+team",
            "division":self.division.id,
            "student_set-0-firstName":"test2",
            "student_set-0-lastName":"test",
            "student_set-0-yearLevel":"test",
            "student_set-0-birthday":"1111-11-11",
            "student_set-0-gender":"male"
        }
        response = self.client.post(reverse('teams:edit',kwargs={'teamID':self.newEventTeam.id}),data=payload)
        self.assertEqual(200,response.status_code)

def newCommonSetUp(self):
        self.user1 = User.objects.create_user(email=self.email1, password=self.password)
        self.user2 = User.objects.create_user(email=self.email2, password=self.password)
        self.user3 = User.objects.create_user(email=self.email3, password=self.password)
        self.superUser = User.objects.create_user(email=self.email_superUser, password=self.password, is_superuser=True)

        self.state1 = State.objects.create(treasurer=self.user1, name='Victoria', abbreviation='VIC')
        self.state2 = State.objects.create(treasurer=self.user1, name='NSW', abbreviation='NSW')
        self.region1 = Region.objects.create(name='Test Region', description='test desc')

        self.school1 = School.objects.create(name='School 1', abbreviation='sch1', state=self.state1, region=self.region1)
        self.school2 = School.objects.create(name='School 2', abbreviation='sch2', state=self.state1, region=self.region1)
        self.school3 = School.objects.create(name='School 3', abbreviation='sch3', state=self.state1, region=self.region1)

        self.campus1 = Campus.objects.create(school=self.school1, name='Campus 1')
        self.campus2 = Campus.objects.create(school=self.school1, name='Campus 2')

        self.year = Year.objects.create(year=2020)
        self.event = Event.objects.create(
            year=self.year,
            state=self.state1,
            name='Test event 1',
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

        self.invoiceSettings = InvoiceGlobalSettings.objects.create(
            invoiceFromName='From Name',
            invoiceFromDetails='Test Details Text',
            invoiceFooterMessage='Test Footer Text',
        )

class TestTeamClean(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'

    def setUp(self):
        newCommonSetUp(self)
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.team2 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school2, name='Team 2', division=self.division1)

    def testNoCampus(self):
        self.assertEqual(self.team1.clean(), None)

    def testCampusValid(self):
        self.team1.campus = self.campus1

        self.assertEqual(self.team1.clean(), None)

    def testCampusWrongSchool(self):
        self.team2.campus = self.campus1

        self.assertRaises(ValidationError, self.team2.clean)

class TestInvoiceMethods(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'

    def setUp(self):
        newCommonSetUp(self)

    def testCampusInvoicingDisabled_noSchool(self):
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.assertEqual(self.team1.campusInvoicingEnabled(), False)

    def testCampusInvoicingDisabled(self):
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.assertEqual(self.team1.campusInvoicingEnabled(), False)

    def testCampusInvoicingEnabled(self):
        self.invoice1 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus1)
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.assertEqual(self.team1.campusInvoicingEnabled(), True)

    def testSave_NoSchool_NoExistingInvoice(self):
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=None).count(), 0)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=None).count(), 1)

    def testSave_NoSchool_ExistingInvoice(self):
        self.invoice1 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=None)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=None).count(), 1)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=None).count(), 1)

    def testSave_CampusInvoicingDisabled_NoExistingInvoice(self):
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1).count(), 0)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1).count(), 1)

    def testSave_CampusInvoicingDisabled_ExistingInvoice(self):
        self.invoice1 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=self.school1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1).count(), 1)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1).count(), 1)

    def testSave_CampusInvoicingEnabled_NoExistingInvoice(self):
        self.invoice1 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus1)

        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus2).count(), 0)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, campus=self.campus2, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus2).count(), 1)

    def testSave_CampusInvoicingEnabled_ExistingInvoice(self):
        self.invoice1 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus1)
        self.invoice2 = Invoice.objects.create(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus2)

        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus2).count(), 1)

        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, campus=self.campus2, name='Team 1', division=self.division1)
        self.assertEqual(Invoice.objects.filter(event=self.event, invoiceToUser=self.user1, school=self.school1, campus=self.campus2).count(), 1)

class TestTeamMethods(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'

    def setUp(self):
        newCommonSetUp(self)

    def testGetState(self):
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.assertEqual(self.team1.getState(), self.state1)

class TestTeamCreationFormValidation_School(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'

    def setUp(self):
        newCommonSetUp(self)
        self.availableDivision = AvailableDivision.objects.create(division=self.division1, event=self.event)
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, school=self.school1, name='Team 1', division=self.division1)
        self.team2 = Team.objects.create(event=self.event, mentorUser=self.user2, school=self.school2, name='Team 2', division=self.division1)
        self.admin1 = SchoolAdministrator.objects.create(school=self.school1, user=self.user1)
        login = self.client.login(request=HttpRequest(), username=self.email1, password=self.password) 

    def testValidCreate(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+8",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 2)

    def testInValidCreate_schoolEventMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        self.event.event_maxTeamsPerSchool = 1
        self.event.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for school for this event exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_overallEventMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        self.event.event_maxTeamsForEvent = 2
        self.event.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for this event exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_schoolDivisionMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        self.availableDivision.division_maxTeamsPerSchool = 1
        self.availableDivision.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for school for this event division exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_overallDivisionMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        self.availableDivision.division_maxTeamsForDivision = 2
        self.availableDivision.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for this event division exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_division(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division2.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Division: Select a valid choice. That choice is not one of the available choices.")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)

    def testInValidCreate_divisionMissing(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Required field is missing")
        self.assertEqual(Team.objects.filter(school=self.school1).count(), 1)

class TestTeamCreationFormValidation_Independent(TestCase):
    email1 = 'user1@user.com'
    email2 = 'user2@user.com'
    email3 = 'user3@user.com'
    email_superUser = 'user4@user.com'
    password = 'chdj48958DJFHJGKDFNM'

    def setUp(self):
        newCommonSetUp(self)
        self.availableDivision = AvailableDivision.objects.create(division=self.division1, event=self.event)
        self.team1 = Team.objects.create(event=self.event, mentorUser=self.user1, name='Team 1', division=self.division1)
        self.team2 = Team.objects.create(event=self.event, mentorUser=self.user2, school=self.school2, name='Team 2', division=self.division1)
        login = self.client.login(request=HttpRequest(), username=self.email1, password=self.password) 

    def testValidCreate(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+8",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 2)

    def testInValidCreate_schoolEventMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        self.event.event_maxTeamsPerSchool = 1
        self.event.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for school for this event exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_overallEventMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        self.event.event_maxTeamsForEvent = 2
        self.event.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for this event exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_schoolDivisionMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        self.availableDivision.division_maxTeamsPerSchool = 1
        self.availableDivision.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for school for this event division exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_overallDivisionMax(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        self.availableDivision.division_maxTeamsForDivision = 2
        self.availableDivision.save()

        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division1.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max teams for this event division exceeded. Contact the organiser.")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)
        self.assertEqual(Team.objects.filter(event=self.event).count(), 2)

    def testInValidCreate_division(self):
        self.assertEqual(self.user1.currentlySelectedSchool, None)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
            "division":self.division2.id,
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Division: Select a valid choice. That choice is not one of the available choices.")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)

    def testInValidCreate_divisionMissing(self):
        self.assertEqual(self.user1.currentlySelectedSchool, self.school1)
        payload = {
            'student_set-TOTAL_FORMS':0,
            "student_set-INITIAL_FORMS":0,
            "student_set-MIN_NUM_FORMS":0,
            "student_set-MAX_NUM_FORMS":self.event.maxMembersPerTeam,
            "name":"Team+3",
        }
        response = self.client.post(reverse('teams:create', kwargs={'eventID':self.event.id}), data=payload, follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Required field is missing")
        self.assertEqual(Team.objects.filter(school=None, mentorUser=self.user1).count(), 1)
