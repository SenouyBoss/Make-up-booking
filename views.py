from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm, RegistrationForm, LoginForm, SelectionForm, DuesForm, NoDuesForm, StudentDetailsForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Student, Room, Hostel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def home(request):
    return render(request, 'CAPAPPv1/ALog/book/home.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('login/edit/')
                    #return render(request, 'CAPAPPv1/ALog/book/edit.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
        else:
            return HttpResponse('Form is not valid')
    else:
        form = UserForm()
        args = {'form': form}
        return render(request, 'CAPAPPv1/ALog/book/reg_form.html', args)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if user.is_warden:
                    return HttpResponse('Invalid Login')
                if user.is_active:
                    login(request, user)
                    student = request.user.student
                    return render(request, 'CAPAPPv1/ALog/book/profile.html', {'student': student})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'CAPAPPv1/ALog/book/login.html', {'form': form})


def warden_login(request):
    user = request.user
    if user is not None:
        try:
            if user.is_warden and user.is_active:
                login(request, user)
                # room_list = request.user.warden.hostel.room_set.all()
                # context = {'rooms': room_list}
                rooms = []
                rooms = rooms + list(Room.objects.all())
                context = {'rooms': rooms}
                return render(request, 'CAPAPPv1/ALog/book/warden.html', context)
        except BaseException:
            pass
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if not user.is_warden:
                    return HttpResponse('Invalid Login because of is warden')
                elif user.is_active:
                    login(request, user)
                    # room_list = request.user.warden.hostel.room_set.all()
                    # context = {'rooms': room_list}
                    rooms = []
                    rooms = rooms + list(Room.objects.all())
                    context = {'rooms': rooms}
                    return render(request, 'CAPAPPv1/ALog/book/warden.html', context)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'CAPAPPv1/ALog/book/login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            student = request.user.student
            return render(request, 'CAPAPPv1/ALog/book/profile.html', {'student': student})
    else:
        form = RegistrationForm(instance=request.user.student)
        return render(request, 'CAPAPPv1/ALog/book/edit.html', {'form': form})


@login_required
def select(request):
    if request.user.student.room:
        return HttpResponse('<h1>You have already selected room - ' + str(request.user.student.room) + '. Please contact your Hostel Caretaker or Warden</h1>')

    if request.method == 'POST':
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                room_id = request.user.student.room_id
                room = Room.objects.get(id=room_id)
                room.vacant = False
                room.save()
            form.save()
            student = request.user.student
            send_mail(
                'Make up notification',
                'you have a new reservation under ' + str(request.user.student.student_name) + ' with the following details: \n Room name: ' +
                str(request.user.student.room) + '\n for the following course: ' + str(request.user.student.course) + '\n And from \n' + request.user.student.reserved_start_date.strftime("%m/%d/%Y, %H:%M:%S") + '\n to \n'
                + request.user.student.reserved_end_date.strftime("%m/%d/%Y, %H:%M:%S") + '',
                'y.abouljid@aui.ma',
                ['registrarstest@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'CAPAPPv1/ALog/book/profile.html', {'student': student})
    else:
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender
        student_course = request.user.student.course
        student_room_type = request.user.student.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course)
        filtered_rooms = Room.objects.none()
        # if student_room_type == 'E':
        #     for i in range(len(hostel)):
        #         h_id = hostel[i].id
        #         filtered_room = Room.objects.filter(
        #             hostel_id=h_id, room_type=['H', 'B'], vacant=True)
        #         filtered_rooms = filtered_rooms | filtered_room
        # else:
        for i in range(len(hostel)):
            h_id = hostel[i].id
            filtered_room = Room.objects.filter(
                hostel_id=h_id, room_type=student_room_type, vacant=True)
            filtered_rooms = filtered_rooms | filtered_room
        form.fields["room"].queryset = filtered_rooms
        return render(request, 'CAPAPPv1/ALog/book/select_room.html', {'form': form})
#+ 'with the following details' +
#                str(request.user.student.room) + 'and from' + request.user.student.reserved_start_date.strftime("%m/%d/%Y, %H:%M:%S") + 'to'
 #               + request.user.student.reserved_end_date.strftime("%m/%d/%Y, %H:%M:%S")


@login_required
def warden_dues(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Student.objects.all()
            return render(request, 'CAPAPPv1/ALog/book/dues.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


@login_required
def warden_add_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = DuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = False
                    student.save()
                    return HttpResponse('Done')
                #return render(request, 'CAPAPPv1/ALog/book/add_due.html', {'form': form})
            else:
                form = DuesForm()
                return render(request, 'CAPAPPv1/ALog/book/add_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


@login_required
def warden_remove_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = NoDuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = True
                    student.save()
                    return HttpResponse('Done')
            else:
                form = NoDuesForm()
                return render(request, 'CAPAPPv1/ALog/book/remove_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


def logout_view(request):
    logout(request)
    return redirect('/')


def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.   objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'CAPAPPv1/ALog/book/hostels.html', context)


@login_required
def warden_student_list(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = []
            #for course in user.warden.hostel.course.all():
            students = students + list(Student.objects.all())
            return render(request, 'CAPAPPv1/ALog/book/warden_student_list.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


@login_required
def change_student_details(request, enrollment_no):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            try:
                this_student = Student.objects.get(enrollment_no=enrollment_no)
                old_room_id = this_student.room_id
            except BaseException:
                raise Http404("Invalid Student or Room")
            if request.method == 'POST':
                form = StudentDetailsForm(request.POST, instance=this_student)
                if form.is_valid():
                    form.save()
                    print(str(old_room_id) + " " + str(this_student.room_id))
                    if not this_student.room_id:
                        # Clear room selection of this student
                        print("clear")
                        old_room = Room.objects.get(id=old_room_id)
                        old_room.vacant = True
                        old_room.save()
                        this_student.room_allotted = False
                        this_student.save()
                    elif old_room_id != this_student.room_id:
                        # Free the old room
                        print("switch")
                        old_room = Room.objects.get(id=old_room_id)
                        old_room.vacant = True
                        old_room.save()
                        # Allot new room
                        new_room = Room.objects.get(id=this_student.room_id)
                        new_room.vacant = False
                        new_room.save()

                    form = StudentDetailsForm(instance=this_student)
                    form.fields["room"].queryset = Room.objects.filter(vacant=True) | Room.objects.filter(id=this_student.room_id)
                    return render(request, 'CAPAPPv1/ALog/book/change_student_details.html', {'form': form})
            else:
                form = StudentDetailsForm(instance=this_student)
                form.fields["room"].queryset = Room.objects.filter(vacant=True) | Room.objects.filter(
                    id=this_student.room_id)
                return render(request, 'CAPAPPv1/ALog/book/change_student_details.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')





# def home(request):
#
#     return render(request, 'CAPAPPv1/ALog/book/simple_book.html')

def funtest(request):
    return render(request, 'CAPAPPv1/index.html')

def aboutfun(request):
    return render(request, 'CAPAPPv1/about.html')

def contactfun(request):
    return render(request, 'CAPAPPv1/contact.html')

def loginfun(request):
    return render(request, 'registration/login.html')

def homefun(request):
    return render(request, 'CAPAPPv1/ALog/home.html')