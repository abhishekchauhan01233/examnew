from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Create your models here.
class scheduletestmodel(models.Model):
    courses = (
        ('BCA','BCA'),
        ('BBA','BBA'),
        ('MBA','MBA'),
        ('BTech','BTech'),
        ('Diploma','Diploma'),
        ('BVocational','BVocational'),
    )
    course = models.CharField(max_length=50, choices=courses)
    subjects = models.CharField(max_length=20)
    date = models.DateField(max_length=20)
    time = models.TimeField()
    duration = models.TimeField()
    questions = models.BigIntegerField()
    marks =  models.BigIntegerField()

    def __str__(self):
        return self.course

class feedbackmodel(models.Model):
    name = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    feedback = models.TextField(max_length=200)

    def __str__(self):
        return self.email

class studentdatamodel(models.Model):
    courses = (
        ('BCA','BCA'),
        ('BBA','BBA'),
        ('MBA','MBA'),
        ('BTech','BTech'),
        ('Diploma','Diploma'),
        ('BVocational','BVocational'),
    )

    categorys = (
        ('General','General'),
        ('SC','SC'),
        ('ST','ST'),
        ('OBC','OBC'),
        ('Minority','Minority'),
    )

    qualifications = (
        ('10th','10th'),
        ('10+2Science','10+2Science'),
        ('10+2Commerce','10+2Commerce'),
        ('10+2Arts','10+2Arts'),
    )

    sources = (
        ('Counsellor','Counsellor'),
        ('Socialmedia','Socialmedia'),
        ('SMS','SMS'),
        ('Leaflet','Leaflet'),
        ('Newspaper','Newspaper'),
        ('Friends/Relatives','Friends/Relatives'),
        ('Poster','Poster'),
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=50, choices=courses, blank=False)
    branch = models.CharField(max_length=50)
    firstname = models.CharField(max_length=60, blank=False)
    lastname = models.CharField(max_length=60, default=None)
    fname = models.CharField(max_length=60, blank=False)
    dob = models.CharField(max_length=20, blank=False)
    category = models.CharField(max_length=40, blank=False, choices=categorys)
    qualification = models.CharField(max_length=40, blank=False, choices=qualifications)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=100, blank=False)
    address = models.CharField(max_length=100, default=None)
    pincode = models.CharField(max_length=100,default=None)
    state = models.CharField(max_length=100, default=None)
    district = models.CharField(max_length=100, default=None)
    source = models.CharField(max_length=100, blank=False, choices=sources)
    counsellor = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.user.username

class uploadquestionpapermodel(models.Model):
    qno = models.BigIntegerField()
    question = models.CharField(max_length=800)
    optiona = models.CharField(max_length=200)
    optionb = models.CharField(max_length=200)
    optionc = models.CharField(max_length=200)
    optiond = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, default=None)

class resultmodel(models.Model):
    email = models.EmailField(max_length=200)
    name = models.CharField(max_length=60)
    fname = models.CharField(max_length=60, default=None)
    mobile = models.BigIntegerField()
    subject = models.CharField(max_length=100, default=None)
    marks = models.BigIntegerField()

    def __str__(self):
        return self.email

