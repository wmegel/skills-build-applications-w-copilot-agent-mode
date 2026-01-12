from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from datetime import date
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Nettoyage compatible Djongo/MongoDB
        for model in [User, Team, Activity, Workout, Leaderboard]:
            for obj in model.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()

        # Teams
        marvel = Team.objects.create(name='Marvel', universe='marvel')
        dc = Team.objects.create(name='DC', universe='dc')

        # Users
        ironman = User.objects.create(email='ironman@marvel.com', name='Iron Man', team=marvel)
        spiderman = User.objects.create(email='spiderman@marvel.com', name='Spider-Man', team=marvel)
        batman = User.objects.create(email='batman@dc.com', name='Batman', team=dc)
        superman = User.objects.create(email='superman@dc.com', name='Superman', team=dc)

        # Activities
        Activity.objects.create(user=ironman, type='Running', duration=30, date=date.today())
        Activity.objects.create(user=spiderman, type='Cycling', duration=45, date=date.today())
        Activity.objects.create(user=batman, type='Swimming', duration=60, date=date.today())
        Activity.objects.create(user=superman, type='Yoga', duration=20, date=date.today())

        # Workouts
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity for heroes')
        w1.suggested_for.set([marvel, dc])
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for super strength')
        w2.suggested_for.set([dc])

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=150, week='2026W02')
        Leaderboard.objects.create(team=dc, points=120, week='2026W02')

        # Index unique sur email (MongoDB)
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('octofit_db a été peuplée avec des données de test.'))
