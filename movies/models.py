from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('released', 'Released'),
    ]

    title = models.CharField(max_length=100, db_index=True)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='movies', on_delete=models.CASCADE)
    producer = models.ForeignKey('Producer', related_name='movies', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['status']),
        ]


class Song(models.Model):
    movie = models.ForeignKey(Movie, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie', 'title'], name='unique_song_per_movie'),
            models.CheckConstraint(check=models.Q(movie__songs__count__lte=5), name='max_five_songs_per_movie'),
        ]


class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active_movie = models.OneToOneField(Movie, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_actor')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(active_movie__status='ongoing'),
                name='actor_must_have_ongoing_movie'
            )
        ]
