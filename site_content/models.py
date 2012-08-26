from django.db import models

class StaticContent(models.Model):
    slug = models.SlugField()
    content = models.TextField()
    def __unicode__(self): return self.slug
    def title(self): return self.slug.replace('_', ' ')
