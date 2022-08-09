from django.db import models
from django.utils.translation import gettext_lazy as _

class SocialContentType(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Social Content Type')
        verbose_name_plural = _('Social Content Types')

class SocialContent(models.Model):
    type = models.ForeignKey(SocialContentType, verbose_name=_('type'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=150)
    link = models.URLField(_('link'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True, default=None)
    image = models.ImageField(_('image'), blank=True, null=True, default=None)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Social Content')
        verbose_name_plural = _('Social Contents')
