from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import connections, ProgrammingError, OperationalError

from sparrow import settings


class Command(BaseCommand):
    help = """Database Related"""

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            dest='subcommand',
            help='Subcommands',
        )

        create_subcommand = subparsers.add_parser(
            'create',
            help='My subcommand 1',
        )
        create_subcommand.add_argument(
            '--drop',
            '-d',
            action='store_true',
            default=False,
            help='Drop Database Before Creating.',
        )

        subparsers.add_parser(
            'drop',
            help='My subcommand 2',
        )

    def handle(self, *args, **options):
        subcommand = options['subcommand']
        connection = connections['administrative']
        database_name = settings.DATABASES['default']['NAME']

        with connection.cursor() as cursor:
            if subcommand == 'create':
                self.create(cursor, database_name)
            elif subcommand == 'drop':
                self.drop(cursor, database_name)
            else:
                raise CommandError('Invalid subcommand')

    def create(self, cursor, database_name):
        try:
            cursor.execute(f'CREATE DATABASE {database_name}')

            self.stdout.write(self.style.SUCCESS(
                f'Database `{database_name}` Created Successfully'
            ))
        except ProgrammingError as exc:
            self.stdout.write(
                self.style.ERROR(
                    f'Database `{database_name}` Already Exists')
            )

    def drop(self, cursor, database_name):
        try:
            cursor.execute(f'DROP DATABASE {database_name}')
            self.stdout.write(self.style.SUCCESS(
                f'Database {database_name} Dropped Successfully'
            ))
        except ProgrammingError as exc:
            self.stdout.write(
                self.style.ERROR(
                    f'Database `{database_name}` Does Not Exists')
            )
        except OperationalError:
            self.stdout.write(self.style.ERROR(
                f'Database `{database_name}` Is Being Accessed By Other Users'
            ))

