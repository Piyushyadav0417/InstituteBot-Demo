from django.db import models

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150)
    bio = models.TextField()
    photo = models.ImageField(upload_to='trainers/')
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    duration = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    language = models.CharField(max_length=100, default="English")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    trainers = models.ManyToManyField(Trainer, related_name='courses')

    def __str__(self):
        return self.title






class About(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="about/", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading