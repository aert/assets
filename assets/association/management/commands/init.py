from os.path import dirname, join, abspath, exists
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = "<dest_file>"
    help = 'Generate ini file.'

    leave_locale_alone = True
    can_import_settings = False

    option_list = BaseCommand.option_list + (
        make_option('--develop',
                    action='store_true',
                    dest='develop',
                    default=False),
    )

    def handle(self, file_path, develop=None, **options):
        dst = file_path

        if exists(dst):
            raise CommandError('file "%s" already exists' % dst)

        if develop:
            name = "config_develop.ini"
        else:
            name = "config_release.ini"

        config_file = join(dirname(abspath(__file__)), "../../../etc", name)

        with open(config_file, "r") as fsource:
            content = fsource.read()

        try:
            open(dst, 'w').write(content)
        except:
            raise CommandError('Unable to write "%s" file.' % dst)
        print('"%s" written.' % join(dst))
