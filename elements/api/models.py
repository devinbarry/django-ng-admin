# coding=utf-8
from django.db import models
from django.templatetags.static import static


class BaseTimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    def created_date_with_seconds(self):
        """Format the created_date datetime object to include seconds in its display."""
        return self.created_date.strftime("%B %d, %Y, %I:%M:%S %p")

    created_date_with_seconds.short_description = 'Created Date'


class Disclaimer(BaseTimeStampedModel):
    text = models.TextField(blank=True, default='Type disclaimer here.')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.text[0:100], self.pk)


class Question(BaseTimeStampedModel):
    question = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='', help_text='This might be the lead in to the answer')
    fragment = models.ForeignKey('Fragment', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ForeignKey('Image', blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.BooleanField('Deleted', blank=False, null=False, default=False, editable=False)

    def thumbnail(self):
        """
        Return HTML allowing an image preview in the admin site.
        """
        if self.image:
            return self.image.admin_image()
        return None
    thumbnail.allow_tags = True

    def __unicode__(self):
        return u'{0} ({1})'.format(self.question, self.pk)


class Answer(models.Model):
    # All possible values for answer type
    CORRECT = 'correct'
    INCORRECT = 'incorrect'

    # User selectable values for task types
    ANSWER_TYPES = (
        (CORRECT, 'Correct'),
        (INCORRECT, 'Incorrect'),
    )

    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.SET_NULL, related_name='answers')
    # We are expecting something like "True" or "False" here
    answer = models.CharField(blank=True, max_length=255, help_text='eg. Waar')
    # Is the answer correct/incorrect/neither
    type = models.CharField(max_length=15, choices=ANSWER_TYPES, default=CORRECT)
    # We display this to the user after they choose this answer
    result_title = models.CharField(blank=True, max_length=255,
                                    help_text='Shown to the user after they choose this answer')
    # This is a more detailed text description shown to user after they choose this answer
    result_description = models.TextField(blank=True, max_length=255,
                                          help_text='Shown to the user after they choose this answer')

    def __unicode__(self):
        return u'{0} - {1} - {2} ({3})'.format(self.answer, self.type, self.result_title, self.pk)


class Fragment(BaseTimeStampedModel):
    """
    This model represents a video fragment stored on a remote server.
    """
    name = models.CharField(blank=True, max_length=255, help_text='Short name to help identify the video')
    code = models.CharField(blank=True, max_length=255, help_text='OBEN Fragment code')
    video_id = models.CharField(blank=True, max_length=255, help_text='ODI video code')
    thumbnail = models.ForeignKey('Image', blank=True, null=True)
    share_url = models.CharField(blank=True, max_length=255)
    start_time = models.PositiveIntegerField(blank=True, null=True, help_text='start time of fragment in seconds')
    end_time = models.PositiveIntegerField(blank=True, null=True, help_text='end time of fragment in seconds')
    deleted = models.BooleanField('Deleted', blank=False, null=False, default=False, editable=False)

    def admin_thumbnail(self):
        """
        Return HTML allowing an image preview in the admin site.
        """
        if self.thumbnail:
            return self.thumbnail.admin_image()
        return None
    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = 'Thumbnail'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.pk)


def _upload_to(instance, file_name):
    # Save images to an images directory inside MEDIA_ROOT
    return 'images/{}'.format(file_name)


class AbstractImage(BaseTimeStampedModel):
    """
    Base model for both the Image and Background models (which both store
    images in the database)
    """
    image = models.ImageField(null=True, blank=True, upload_to=_upload_to)
    color = models.CharField(blank=True, max_length=255)

    class Meta:
        abstract = True

    def admin_image(self):
        return '<img src="%s" height="50"/>' % static(self.image.url)
    admin_image.allow_tags = True

    def __unicode__(self):
        return self.image.url


class Image(AbstractImage):
    """
    Image model used to store images in the database.
    """
    # upload_to = 'images/'
    pass


class Background(AbstractImage):
    """
    Background model used to store background images in the database.
    """
    # upload_to='backgrounds/'
    pass
