'''
Created on November 29, 2012

@author: Psalm
'''
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    help = "Creates test users for a %s installation" % (Site.objects.get_current().name)
    help = "%s\nUsage:\npython manage.py create_sample_users <number of users>" % help
    help = "%s [--prefix <prefix for usernames> --password <sample password>]" % help
    help = "%s\n\nIf --prefix and --password are not provided the default values will be" % help
    help = "%s 'testuser' and 'samplepass,' respectively." % help
    
    option_list = BaseCommand.option_list + (
                make_option('--prefix',
                            action='store',
                            type='string',
                            default='testuser'
                            ),
                make_option('--password',
                            action='store',
                            type='string',
                            default='samplepass'
                            ),
                )

    """
    Name: handle
    Description:
    main program; run the command
    """   
    def handle(self, *args, **options):
        #set variables
        try:
            num_users = int(args[0])
        except:
            raise CommandError(self.help) 
        prefix = options['prefix']
        password = options['password']

        #create usernames
        users = list()
        for num in xrange(num_users):
            name = "%s%d" % (prefix, num)
            users.append({
                         'username': name,
                         'password': password,
                         'email': "%s@test.com" % name,
                         'first_name': name
                         })
        #create users
        for user in users:
            # delete if exists
            user_object = User.objects.filter( username__exact=user["username"] )
            if user_object is not None:
                user_object.delete()

            user_object = User.objects.create_user( user["username"], email=user["email"], password=user["password"] )
            user_object.first_name = user["first_name"]
            user_object.save()
            print 'Created User %s' % user_object