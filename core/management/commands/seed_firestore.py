from django.core.management.base import BaseCommand

from core.firestore_service import seed_demo_programs


class Command(BaseCommand):
    help = 'Seed Firestore with demo OBE program data.'

    def handle(self, *args, **options):
        programs = seed_demo_programs()
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(programs)} programs into Firestore.'))
