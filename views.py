from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from SMS.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import uuid
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .forms import *


def home(request):
    return render(request, 'home.html')


def regis(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pas = request.POST.get('password')
        if User.objects.filter(username=uname).first():
            messages.success(request, "username already taken")
            return redirect(regis)
        if User.objects.filter(email=email).first():
            messages.success(request, "email already taken")
            return redirect(regis)
        user_obj = User(username=uname, email=email)
        user_obj.set_password(pas)
        user_obj.save()

        auth_token = str(uuid.uuid4())
        profile_obj = profile1.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email, auth_token)
        return redirect(success)
    return render(request, 'register.html')


def success(request):
    return render(request, "success.html")


def lo(request):
    global User;
    if request.method == 'POST':
        username = request.POST.get('uname')
        pas = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'user not found')
            return redirect(lo)
        profile_obj = profile1.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'profile not verified check ur email')
            return redirect(lo)
        User = authenticate(username=username, password=pas)
        if User is None:
            messages.success(request, 'wrong password or username')
            return redirect(lo)
        obj = profile1.objects.filter(user=user_obj)
        assignments = Assignment.objects.filter(student=request.user)
        return render(request, 'h.html', {'obj': obj, 'assignments': assignments})
    return render(request, 'stafflogin.html')


def verify(request, auth_token):
    profile_obj = profile1.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'your account is already verified')
            redirect(lo)
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, 'ur account is verified')
        return redirect(lo)
    else:
        return redirect(error)


def error(request):
    return render(request, 'error.html')


def send_mail_regis(email, token):
    subject = "your account has been verified"
    message = f'pass the link to verify your account  http://127.0.0.1:8000/verify/{token}'
    email_from = EMAIL_HOST_USER
    recipient = [email]
    send_mail(subject, message, email_from, recipient)


def class_view(request):
    students = Student.objects.all()
    return render(request, 'class.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        user_form = UserCreationForm(request.POST)
        if student_form.is_valid() and user_form.is_valid():
            # Save student data
            student = student_form.save(commit=False)

            # Create user account
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # Set password
            user.save()

            # Associate the user with the student
            student.user = user
            student.save()

            messages.success(request, 'Student added successfully!')
            return redirect('class')  # Redirect to the class view
    else:
        student_form = StudentForm()
        user_form = UserCreationForm()
    return render(request, 'add_student.html', {'student_form': student_form, 'user_form': user_form})


def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('class_view')  # Redirect to the list of students page
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})


def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('class_view')  # Redirect to the list of students page
    return render(request, 'delete_student.html', {'student': student})


def send_message(request):
    students = Student.objects.all()  # Fetch all students for the dropdown
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        student = get_object_or_404(Student, user_id=user_id)  # Get the student based on the user ID
        resume_file = request.FILES.get('resume')  # Retrieve the uploaded resume file
        message_text = request.POST.get('text')  # Retrieve the message text
        # Create a new message instance and associate it with the student
        message = Message.objects.create(student=student, text=message_text, resume=resume_file)
        return HttpResponse("Message sent successfully!")
    return render(request, 'class.html', {'students': students})


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect(
                'student_dashboard')  # Replace 'student_dashboard' with the URL name for the student dashboard
        else:
            # Return an error message or render the login page again with an error
            return render(request, 'student_login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'student_login.html')


def student_dashboard(request):
    # Get the logged-in student
    student = request.user.student

    # Fetch messages associated with the logged-in student
    messages = Message.objects.filter(student=student)
    student_name = student.user.username

    # Render the student dashboard template with the messages
    return render(request, 'student_dashboard.html', {'messages': messages, 'student_name': student_name})


def d1(request):
    username = request.POST.get('uname')
    user_obj = User.objects.filter(username=username).first()
    obj = profile1.objects.filter(user=user_obj)
    return render(request, 'h.html', {'obj': obj})


def profile(request):
    # Get the logged-in student
    student = request.user.student

    # Pass student's details to the template context
    student_details = {
        'username': student.user.username,
        'name': student.name,  # Add the name field from the Student model
        'roll_number': student.roll_number,  # Add the roll_number field from the Student model
        # Add more details as needed
    }

    # Render the profile template with student details
    return render(request, 'profile.html', {'student_details': student_details})


def raise_doubt_view(request):
    if request.method == 'POST':
        doubt_text = request.POST.get('doubt')
        # Create a Doubt object and save it to the database
        doubt = Doubt(student=request.user, text=doubt_text)
        doubt.save()
        return HttpResponse('Doubt created', status=201)  # Return HTTP response with status code 201 (Created)
    return render(request, 'raised.html')


def view_doubts(request):
    # Get all doubts from the database
    doubts = Doubt.objects.all()
    # Render a template with the doubts
    return render(request, 'view_doubts.html', {'doubts': doubts})


# Render the same page for GET requests


def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            return HttpResponse("Assignment uploaded successfully")
    else:
        form = AssignmentForm()
    return render(request, 'upload_assignment.html', {'form': form})


def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    assignment.delete()
    messages.success(request, "Assignment deleted successfully")
    return render(request, 'h.html')
