import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from markdown import markdown



class Category(models.Model):
    title = models.CharField(max_length=250, 
                             help_text='Maximum 250 characters')
    slug = models.SlugField(unique=True, 
                            help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "%s/" % self.slug

    get_absulute_url = models.permalink(get_absolute_url)

    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

    

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)



class Entry(models.Model):
    
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    # Core fields.
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters')
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    # Fields to store generated html.
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata.
    slug = models.SlugField(unique_for_date='pub_date')
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
 
    # Categorization.
    categories = models.ManyToManyField(Category)
    tags = TagField()

    # Managers.
    live = LiveEntryManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']

    
    def __unicode__(self):
        return self.title
    

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)

        
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), { 'year' : self.pub_date.strftime("%Y"),
                                               'month' : self.pub_date.strftime("%b").lower(),
                                               'day' : self.pub_date.strftime("%d"),
                                               'slug' : self.slug })
    
    
    get_absolute_url = models.permalink(get_absolute_url)



class Link(models.Model):

    # Link.
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    url = models.URLField(unique=True)
    via_name = models.CharField('Via', max_length=250, blank=True, 
                                help_text='The name af the site you spotted the link on. Optional.')
    via_url = models.URLField('Via URL', blank=True, 
                              help_text='The URL of the site you spotted the link on. Optional.')

    # Metadata.
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    tags = TagField()
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)
   

    class Meta:
        ordering = ['-pub_date']


    def __unicode__(self):
        return self.title


    def save(self):
        
        if self.description:
            self.description_html = markdown(self.description)
        
        if not self.id and self.post_elsewhere:
            import pydelicious
            from django.utils.encoding import smart_str
            # warning: the following line goes into an infinite loop if user/pass combo doesn't work
            #pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
            #                smart_str(self.url), smart_str(self.title), smart_str(self.tags))

        super(Link, self).save()
        

    def get_absolute_url(self):
        return ('coltrane_link_detail', 
                (), 
                { 'year': self.pub_date.strftime('%Y'),
                  'month': self.pub_date.strftime('%b').lower(),
                  'day': self.pub_date.strftime('%d'),
                  'slug': self.slug })

    get_absolute_url = models.permalink(get_absolute_url)


# Spam checking for comments
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.db.models import signals
from akismet import Akismet
from django.utils.encoding import smart_str
from django.contrib.comments.signals import comment_will_be_posted


def moderate_comment(sender, comment, request, **kwargs):

    if not comment.id:
        
        # Comments older than 30 days auto marked as spam.
        entry = comment.content_object
        delta = datetime.datetime.now() - entry.pub_date
        if delta.days > 30:
            comment.is_public = False

        # Run akismet on other comments.
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, 
                              blog_url="http://%s/" % Site.objects.get_current().domain)

        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                             'referrer': request.META['HTTP_REFERER'],
                             'user_ip': comment.ip_address,
                             'user_agent': request.META['HTTP_USER_AGENT'] }
            if akismet_api.comment_check(smart_str(comment.comment),
                                         akismet_data,
                                         build_data=True):
                comment.is_public = False


comment_will_be_posted.connect(moderate_comment, sender=Comment)
