from __future__ import unicode_literals
import uuid, os
from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import UUIDField


class BaseClass(Model):
    id = UUIDField(default=uuid.uuid4, primary_key=True)
    ts = DateTimeField(auto_now_add=True)
    uts = DateTimeField(auto_now=True)


class Movies(BaseClass):
    '''
    This table is for keeping track of user-to-movie score
    '''
    imdbid = CharField(max_length=10, unique=True)
    name = CharField(max_length=100)
    year = IntegerField()
    type = CharField(max_length=10, null=True)
    rtscore = FloatField(default=0)  # rotten tomatoes score
    boscore = FloatField(default=0)  # box office score based on collection
    box_office = IntegerField(null=True, default=None)  # total box office collection(in $)
    totalscore = FloatField(default=0)

    def __str__(self):
        return self.name + '_' + self.imdbid

    @classmethod
    def AddMovie(self, data):
        try:
            if data['rtscore'] == 'N/A':
                data['rtscore'] = 0
            if data['boscore'] == 'N/A':
                data['boscore'] = 0
            instance = self.objects.create(imdbid=data['imdb_id'], name=data['title'], year=data['year'],
                                           rtscore=data['rtscore'], boscore=data['boscore'],
                                           box_office=data['box_office'],
                                           totalscore=float(float(data['rtscore']) + float(data['boscore'])))
            instance.save()
            return instance
        except Exception as e:
            print(e)
            return self.objects.get(imdbid=data['imdb_id'])

    class Meta:
        verbose_name = 'Movies'
        verbose_name_plural = 'Movies'


class User(AbstractUser):
    phone = CharField(max_length=12, null=True)
    signup_method = CharField(max_length=10, null=True)
    gender = CharField(max_length=10, null=True)
    picture = ImageField(upload_to='picture/')
    score = FloatField(default=0)
    rank = IntegerField(default=0)
    delete = BooleanField(default=False)
    movies = ManyToManyField(Movies)

    def __str__(self):
        return self.username

    class Admin:
        list_display = ('first_name', )

    class Meta:
        verbose_name = 'Fantasy User'
        verbose_name_plural = 'Fantasy Users'

    @classmethod
    def update_user(cls, data, email):
        try:
            name, extension = os.path.splitext(data['picture'].name)
            replace_name, replace_ext = os.path.splitext(str(email))
            replace_full = str(replace_name.split("@")[0]) + str(extension)
            data['picture'].name = replace_full
            uobj = User.objects.get(username=str(email))
            uobj.first_name = data['first_name']
            uobj.last_name = data['last_name']
            uobj.phone = data['phone']
            uobj.gender = data['gender']
            uobj.picture = data['picture']
            uobj.save()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def get_user_instance(cls, usrename):
        try:
            instance = cls.objects.get(username=usrename)
            return instance
        except cls.DoesNotExists:
            return None


class Group(BaseClass):
    group_name = CharField(max_length=50, unique=True)
    group_admin = ForeignKey(User, on_delete=DO_NOTHING, verbose_name="admin")
    active = BooleanField(default=True)

    @classmethod
    def createGroup(cls, data, adminobj):
        try:
            instance = cls.objects.create(data['group_name'], adminobj)
            return instance
        except Exception as e:
            return None

    @classmethod
    def searchGroupByName(cls, groupname):
        try:
            instance = cls.objects.get(group_name=groupname)
            return instance
        except Exception as e:
            return None


class UserGroup(BaseClass):
    uobj = ForeignKey(User, on_delete=DO_NOTHING, verbose_name="user")
    group = ForeignKey(Group, on_delete=DO_NOTHING, verbose_name="group")
    userActive = BooleanField(default=True)

    @classmethod
    def addUserToGroup(cls, userobj, groupobj):
        try:
            instance = cls.objects.create(uobj=userobj, group=groupobj)
            return instance
        except Exception as e:
            return None

    class Meta:
        unique_together = (('uobj', 'group'),)


class Upcoming_movies(BaseClass):
    title = CharField(max_length=100)
    year = IntegerField()
    rtscore = FloatField(default=0, null=True)
    boscore = FloatField(default=0, null=True)
    box_office = CharField(max_length=100, null=True)
    totalscore = FloatField(default=0, null=True)

    class Meta:
        verbose_name = 'Admin Added Movies'
        verbose_name_plural = 'Admin Added Movies'

    @classmethod
    def getlist(cls, title):
        movieslist = cls.objects.filter(title=title).values('title', 'year')
        return movieslist

    def __str__(self):
        return self.title


class map_userMovie(BaseClass):
    uobj = ForeignKey(User, on_delete=DO_NOTHING, verbose_name="user")
    mobj = ForeignKey(Movies, on_delete=DO_NOTHING, verbose_name="movie")
    dropbit = BooleanField(default=False)

    class Meta:
        unique_together = (('uobj', 'mobj'),)
        verbose_name = 'User Selected Movies'
        verbose_name_plural = 'User Selected Movies'

    def __str__(self):
        return self.uobj.first_name + '-' + self.mobj.name


class otp(BaseClass):
    uobj = ForeignKey(User, on_delete=DO_NOTHING)
    code = IntegerField(null=True)

    @classmethod
    def get_user(cls, email):
        try:
            otpobj = cls.objects.get(uobj__username=email)
            return otpobj
        except Exception as e:
            print(e)
            return None


class BOMax(Model):
    """
    This model stores collection of the movie having maximum collection
    of the year.
    """
    year = IntegerField()
    collection = IntegerField()

    class Meta:
        ordering = ('year',)
        verbose_name = 'bo_max'
        verbose_name_plural = 'bo_max'

    def __str__(self):
        return '<Year: {}, Collection: {}>'.format(self.year, self.collection)


class TopPoster(Model):
    """
    To store posters of top movies to display on search page.
    """
    title = CharField(max_length=128)
    url = URLField()
    num_votes = IntegerField()

    def __str__(self):
        return '<Name: {}, URL: {}>'.format(self.title, self.url)
