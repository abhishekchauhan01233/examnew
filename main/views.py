from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import scheduletestmodel, feedbackmodel,uploadquestionpapermodel, studentdatamodel, resultmodel
from datetime import datetime, date, time
import smtplib

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        if request.POST.get('asave'):
            return redirect('/admin/')
            
        elif request.POST.get('rsave'):
            return redirect('/studentregister/')

        elif request.POST.get('lsave'):
            return redirect('/studentlogin/')

        elif request.POST.get('msave'):
            return redirect('/exampattern/')
        
        elif request.POST.get('gsave'):
            return redirect('/guidelines/')

        elif request.POST.get('dsave'):
            return redirect('/dates/')

        elif request.POST.get('sysave'):
            return redirect('/syllabus/')

        elif request.POST.get('scsave'):
            return redirect('/scholarships/')

        return render(request, 'main/home.html')

def exampattern(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        return render(request, 'main/exampattern.html')

def guidelines(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        return render(request, 'main/guidelines.html')

def dates(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        return render(request, 'main/dates.html')

def syllabus(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        return render(request, 'main/syllabus.html')

def scholarships(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        return render(request, 'main/scholarships.html')

def studentregister(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        if request.method == 'POST':
            course = request.POST.get('course')
            branch = request.POST.get('branch')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            fname = request.POST.get('fname')
            dob = request.POST.get('dob')
            category = request.POST.get('category')
            qualification = request.POST.get('qualification')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            district = request.POST.get('district')
            source = request.POST.get('source')
            counsellor = request.POST.get('counsellor')
                
            if (pass1==pass2):
                if User.objects.filter(username=email).exists():
                    return HttpResponse("<h1 align='center'>User with this Email already exists</h1>")
                else:
                    user = User.objects.create_user(username=email, password=pass1, email=email, first_name=firstname, last_name=lastname)
                    user.save()
                    student = studentdatamodel .objects.create(user=user,course=course,branch=branch, firstname=firstname, lastname=lastname,fname=fname, dob=dob, category=category, qualification=qualification, phone=phone, email=email, address=address, pincode=pincode, state=state, district=district, source=source, counsellor=counsellor)
                    student.save()
                    s = smtplib.SMTP("smtp.gmail.com",  587)
                    s.starttls()
                    s.login('Gangascholarshiptest@gmail.com','hitanshusaluja1')
                    message = '''Dear Candidate
Thank you for registring to our form of Online Admission cum Scholarship Test 2020 (GST-20).
Scholarship Test is scheduled on 21st June 2020 at 11:00 AM.
Kindly read all instructions before appearing in test.


All The BEST
Organizer : Ganga Technical Campus (a Unit of Ganga Group of Institutions), Delhi - NCR 
For Further Information Call :
Cordinator :- Mr. Hitanshu Saluja (8684000906)
Co-cordinator :- Mr. Ritesh (8684000920)

Other Helpline Numbers: 08684000906 / 920 / 925 / 934
'''
                    s.sendmail("Gangascholarshiptest@gmail.com", email, message)
                    s.quit()
                    return redirect('/studentlogin/')
            else:
                return HttpResponse("<h1 align='center'>Password1 and Password2 did not match</h1>")

        else:
            return render(request, 'main/studentregister.html')

def studentlogin(request):
    if request.user.is_authenticated:
        return redirect('/student/')
    else:
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/student/')
            else:
                return HttpResponse("<h1 align='center'>Invalid Credentials</h1>")
        else:
            return render(request, 'main/student_login.html')

@login_required(login_url='/studentlogin/')
def student(request):
    user = request.user
    userid = user.id

    data = studentdatamodel.objects.get(user_id=userid)

    if request.POST.get('psave'):
        return redirect('/profile/')
        
    elif request.POST.get('tsave'):
        return redirect('/taketest/')
        
    elif request.POST.get('rsave'):
        return redirect('/result/')
        
    elif request.POST.get('fsave'):
        return redirect('/feedback/')
        
    return render(request, 'main/student.html', {'data':data})

@login_required(login_url='/studentlogin/')
def profile(request):
    user = request.user
    userid = user.id
    data = studentdatamodel.objects.get(user_id=userid)

    context = {
        'data':data
        }

    if request.POST.get('lsave'):
        auth.logout(request)
        return redirect('/')
    
    elif request.POST.get('bsave'):
        return redirect('/student/')

    return render(request, 'main/profile.html', context)

@login_required(login_url='/studentlogin/')
def take_test(request):
    user = request.user
    userid = user.id
    today = date.today()

    timenow_ = datetime.strftime(datetime.now(),"%H:%M:%S")
    t = [timenow_,'05:30:00']
    totalsecs=0
    for i in t:
	    timeparts = [int(s) for s in i.split(':')]
	    totalsecs += (timeparts[0]*60 + timeparts[1])*60 + timeparts[2]
    totalsecs, sec = divmod(totalsecs, 60)
    hr, minute = divmod(totalsecs, 60)
    timenow = "%02d:%02d:%02d" % (hr,minute,sec)

    sdata = studentdatamodel.objects.get(user_id=userid)

    try:
        scheduletime = list(scheduletestmodel.objects.filter(date=today, course=sdata.course).order_by('time'))
        data = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))
        dur = str(data.duration)
        dur2 = [int(s) for s in dur.split(':')]
        dur3=0
        dur3 += (dur2[0]*60 + dur2[1])*60 + dur2[2]
        print(dur3)
        totalsecs=0
        timelist = [timenow]
        for i in timelist:
            timeparts = [int(s) for s in i.split(':')]
            totalsecs += (timeparts[0]*60 + timeparts[1])*60 + timeparts[2]
        totalsecs = totalsecs - dur3
        totalsecs, sec = divmod(totalsecs, 60)
        hr, minute = divmod(totalsecs, 60)
        timenow_duration = "%02d:%02d:%02d" % (hr,minute,sec)

        if timenow < str(scheduletime[0].time):
            data = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))  

        elif timenow > str(scheduletime[0].time):
            for i in range(len(scheduletime)):
                if str(scheduletime[i].time) < timenow_duration:
                    scheduletestmodel.objects.filter(time=scheduletime[i].time).delete()
                data = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time)) 
                    
        date1 = str(data.date)

        starttime = str(data.time)

        duration = str(data.duration)

        timelist = [duration,starttime]
        totalsecs=0
        for i in timelist:
            timeparts = [int(s) for s in i.split(':')]
            totalsecs += (timeparts[0]*60 + timeparts[1])*60 + timeparts[2]
        totalsecs, sec = divmod(totalsecs, 60)
        hr, minute = divmod(totalsecs, 60)
        endtime = "%02d:%02d:%02d" % (hr,minute,sec)

        if request.POST.get('save'):
            if resultmodel.objects.filter(email=sdata.user).exists(): 
                if resultmodel.objects.filter(subject=data.subjects).exists():
                    return HttpResponse("<h1 align='center'>You have already given this exam</h1>")
                        
                else:
                    if (timenow<starttime):
                        return HttpResponse("<h1 align='center'>The Exam has not been started yet!! </h1>")
                    elif (timenow > starttime and timenow < endtime):
                        return redirect('/test/')
                    elif (timenow>endtime):
                        return HttpResponse("<h1 align='center'>The Exam has been ended!! </h1>")
            else:
                if (timenow<starttime):
                    return HttpResponse("<h1 align='center'>The Exam has not been started yet!! </h1>")
                elif (timenow > starttime and timenow < endtime):
                    return redirect('/test/')
                elif (timenow>endtime):
                    return HttpResponse("<h1 align='center'>The Exam has been ended!! </h1>")
    except:
        return HttpResponse("<h1 align='center'>There are no scheduled tests for today!!</h1>")

    return render(request, 'main/taketest.html', {'data':data, 'date1':date1, 'starttime':starttime, 'duration':timenow})

@login_required(login_url='/studentlogin/')
def test(request):
    user = request.user
    userid = user.id
    today=date.today()
    timenow = datetime.strftime(datetime.now(),"%H:%M:%S")
    sdata = studentdatamodel.objects.get(user_id=userid)

    scheduletime = list(scheduletestmodel.objects.filter(date=today, course=sdata.course).order_by('time'))
    data = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))
    dur = str(data.duration)
    dur2 = [int(s) for s in dur.split(':')]
    dur3=0
    dur3 += (dur2[0]*60 + dur2[1])*60 + dur2[2]

    totalsecs=0
    timelist = [timenow]
    for i in timelist:
        timeparts = [int(s) for s in i.split(':')]
        totalsecs += (timeparts[0]*60 + timeparts[1])*60 + timeparts[2]
    totalsecs = totalsecs - dur3
    totalsecs, sec = divmod(totalsecs, 60)
    hr, minute = divmod(totalsecs, 60)
    timenow_duration = "%02d:%02d:%02d" % (hr,minute,sec)

    if timenow < str(scheduletime[0].time):
        scheduledata = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))  

    elif timenow > str(scheduletime[0].time):
        for i in range(len(scheduletime)):
            if str(scheduletime[i].time) < timenow_duration:
                scheduletestmodel.objects.filter(time=scheduletime[i].time).delete()
            scheduledata = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time)) 
    try:         
        data = uploadquestionpapermodel.objects.filter(subject=scheduledata.subjects)
        marks=0
        if request.method == 'POST':
            if request.POST.get('1') == uploadquestionpapermodel.objects.get(qno=1, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('2') == uploadquestionpapermodel.objects.get(qno=2, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('3') == uploadquestionpapermodel.objects.get(qno=3, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('4') == uploadquestionpapermodel.objects.get(qno=4, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('5') == uploadquestionpapermodel.objects.get(qno=5, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('6') == uploadquestionpapermodel.objects.get(qno=6, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('7') == uploadquestionpapermodel.objects.get(qno=7, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('8') == uploadquestionpapermodel.objects.get(qno=8, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('9') == uploadquestionpapermodel.objects.get(qno=9, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('10') == uploadquestionpapermodel.objects.get(qno=10, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('11') == uploadquestionpapermodel.objects.get(qno=11, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('12') == uploadquestionpapermodel.objects.get(qno=12, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('13') == uploadquestionpapermodel.objects.get(qno=13, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('14') == uploadquestionpapermodel.objects.get(qno=14, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('15') == uploadquestionpapermodel.objects.get(qno=15, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('16') == uploadquestionpapermodel.objects.get(qno=16, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('17') == uploadquestionpapermodel.objects.get(qno=17, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('18') == uploadquestionpapermodel.objects.get(qno=18, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('19') == uploadquestionpapermodel.objects.get(qno=19, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('20') == uploadquestionpapermodel.objects.get(qno=20, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('21') == uploadquestionpapermodel.objects.get(qno=21, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('22') == uploadquestionpapermodel.objects.get(qno=22, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('23') == uploadquestionpapermodel.objects.get(qno=23, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('24') == uploadquestionpapermodel.objects.get(qno=24, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('25') == uploadquestionpapermodel.objects.get(qno=25, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('26') == uploadquestionpapermodel.objects.get(qno=26, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('27') == uploadquestionpapermodel.objects.get(qno=27, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('28') == uploadquestionpapermodel.objects.get(qno=28, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('29') == uploadquestionpapermodel.objects.get(qno=29, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('30') == uploadquestionpapermodel.objects.get(qno=30, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('31') == uploadquestionpapermodel.objects.get(qno=31, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('32') == uploadquestionpapermodel.objects.get(qno=32, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('33') == uploadquestionpapermodel.objects.get(qno=33, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('34') == uploadquestionpapermodel.objects.get(qno=34, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('35') == uploadquestionpapermodel.objects.get(qno=35, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('36') == uploadquestionpapermodel.objects.get(qno=36, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('37') == uploadquestionpapermodel.objects.get(qno=37, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('38') == uploadquestionpapermodel.objects.get(qno=38, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('39') == uploadquestionpapermodel.objects.get(qno=39, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('40') == uploadquestionpapermodel.objects.get(qno=40, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('41') == uploadquestionpapermodel.objects.get(qno=41, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('42') == uploadquestionpapermodel.objects.get(qno=42, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('43') == uploadquestionpapermodel.objects.get(qno=43, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('44') == uploadquestionpapermodel.objects.get(qno=44, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('45') == uploadquestionpapermodel.objects.get(qno=45, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('46') == uploadquestionpapermodel.objects.get(qno=46, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('47') == uploadquestionpapermodel.objects.get(qno=47, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('48') == uploadquestionpapermodel.objects.get(qno=48, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('49') == uploadquestionpapermodel.objects.get(qno=49, subject=scheduledata.subjects).answer:
                marks += 1
            if request.POST.get('50') == uploadquestionpapermodel.objects.get(qno=50, subject=scheduledata.subjects).answer:
                marks += 1

            if resultmodel.objects.filter(email=sdata.user).exists():
                
                if resultmodel.objects.filter(subject=scheduledata.subjects).exists():
                    return HttpResponse("<h1 align='center'>You have already given this exam</h1>")

                else:
                    resultmodel.objects.create(email=sdata.user, name=sdata.firstname, fname=sdata.fname, mobile=sdata.phone, subject=scheduledata.subjects, marks=marks)
                    return redirect('/result/')
                
            else:
                resultmodel.objects.create(email=sdata.user, name=sdata.firstname, fname=sdata.fname, mobile=sdata.phone, subject=scheduledata.subjects, marks=marks)
                return redirect('/result/')
    except:
        return HttpResponse("<h1 align='center'> Question Paper of this subject is not uploaded by the admin yet</h1>")
    
    return render(request, 'main/testscreen.html', {'data':data, 'sdata':sdata})

@login_required(login_url='/studentlogin/')
def result(request):
    user = request.user
    userid = user.id
    today=date.today()
    timenow = datetime.strftime(datetime.now(),"%H:%M:%S")
    sdata = studentdatamodel.objects.get(user_id=userid)

    

    '''try: 
        scheduletime = list(scheduletestmodel.objects.filter(date=today, course=sdata.course).order_by('time'))
        data = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))
        dur = str(data.duration)
        dur2 = [int(s) for s in dur.split(':')]
        dur3=0
        dur3 += (dur2[0]*60 + dur2[1])*60 + dur2[2]

        totalsecs=0
        timelist = [timenow]
        for i in timelist:
            timeparts = [int(s) for s in i.split(':')]
            totalsecs += (timeparts[0]*60 + timeparts[1])*60 + timeparts[2]
        totalsecs = totalsecs - dur3
        totalsecs, sec = divmod(totalsecs, 60)
        hr, minute = divmod(totalsecs, 60)
        timenow_duration = "%02d:%02d:%02d" % (hr,minute,sec)

        print(timenow_duration)

        if timenow < str(scheduletime[0].time):
            scheduledata = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))  

        elif timenow > str(scheduletime[0].time):
            for i in range(len(scheduletime)):
                if str(scheduletime[i].time) < timenow_duration:
                    scheduletestmodel.objects.filter(time=scheduletime[i].time).delete()
                scheduledata = scheduletestmodel.objects.get(Q(date=today),Q(course=sdata.course),Q(time=scheduletime[0].time))

        data = resultmodel.objects.get(email=sdata.user, subject=scheduledata.subjects)

        if request.POST.get('save'):
            return redirect('/student/')
    except:
        return HttpResponse("<h1 align='center'>You had not given any exam today or exam time is over</h1>")

    return render(request, 'main/result.html', {'data':data, 'sdata':sdata})'''

    return render(request, 'main/result.html')

@login_required(login_url='/studentlogin/')
def feedback(request):
    user = request.user
    userid = user.id
    data = studentdatamodel.objects.get(user_id=userid)

    if request.method == "POST":
        feedback = request.POST.get('feedback')
        feedbackmodel.objects.create(name=data.firstname, fname=data.fname, email=data.user, feedback=feedback)
        return redirect('/student/')

    return render(request, 'main/feedback.html', {'data':data})