from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify 

# Create your models here.
class CustomUser(AbstractUser):
    # You can add custom fields here if needed
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_img', blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    youtube = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    # Overriding the save method to ensure any custom logic if needed in future 
class Blog(models.Model):
    CATEGORY = [
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Economy', 'Economy'),
        ('Business', 'Business'),  # fixed typo
        ('Sports', 'Sports'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="blogs",
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=CATEGORY, blank=True, null=True)
    featured_image = models.ImageField(upload_to='blog_img', blank=True, null=True)

    class Meta:
        # Order newest published first; drafts (null published_date) will appear last
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug only if it's missing
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug = base_slug
            num = 1
            # Exclude self when checking (so updates don't keep appending -1, -2, ...)
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        # Set published_date when moving out of draft
        if not self.is_draft and self.published_date is None:
            self.published_date = timezone.now()

        # ✅ Correct indentation: call super INSIDE the method
        super().save(*args, **kwargs)