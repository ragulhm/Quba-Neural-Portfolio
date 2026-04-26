from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('source-only', 'Source Only'),
        ('in-progress', 'In Progress'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.JSONField(default=list, help_text="List of technologies used")
    features = models.JSONField(default=list, help_text="List of key features")
    demo_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    grid_span = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class SkillCategory(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Lucide icon name (e.g., 'code-2')")
    gradient = models.CharField(max_length=100, help_text="Tailwind gradient classes (e.g., 'from-violet-500 to-purple-600')")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order']

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} ({self.email})"

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(help_text="Markdown supported")
    excerpt = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(BlogCategory, related_name='posts', on_delete=models.SET_NULL, null=True)
    thumbnail_url = models.URLField(blank=True, null=True, help_text="Optional image URL for the post")
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
