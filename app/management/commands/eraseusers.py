from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'erase django users'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='erase all django users')

    def handle(self, *args, **options):
        if options['all']:
            User.objects.all().delete()
            self.stdout.write('all django users deleted')

