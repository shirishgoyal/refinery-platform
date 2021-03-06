from data_set_manager.single_file_column_parser import SingleFileColumnParser
from data_set_manager.tasks import create_dataset
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    help = "Takes a tab-delimited file as input, parses, and inputs it into"
    help += " the database\n\nNOTE: All provided indices should be zero-based"

    option_list = BaseCommand.option_list + (
                make_option('--username',
                            action='store',
                            type='string',
                            help='(Required) username of the owner of this data set'
                            ),
                make_option('--title',
                            action='store',
                            type='string',
                            help='(Required) name of this data set'
                            ),
                make_option('--file_name',
                            action='store',
                            type='string',
                            help='(Required) absolute path to the file being parsed'
                            ),
                make_option('--source_column_index', '--source_column',
                            action='store',
                            type='string',
                            help='(Required) list of column indices to be used for source grouping (comma-separated, no spaces)\nValues in the columns indicated by the list of column indices provided for the "source_column_index" will be concatenated to create an identifier for the "source" of the sample'
                            ),
                make_option('--data_file_column',
                            action='store',
                            type='string',
                            help='(Required) index of the column of the input file that contains the path to or the URL of the file associated with this sample'
                            ),
                make_option('--auxiliary_file_column',
                            action='store',
                            type='string',
                            default=None,
                            help='column index of the input file that contains the path to an auxiliary file (e.g. for visualization) associated with the input file'
                            ),
                make_option('--base_path',
                            action='store',
                            type='string',
                            default="",
                            help='base path of your data file paths if using relative locations'
                            ),
                make_option('--slug',
                            action='store',
                            type='string',
                            default=None,
                            help='shortcut name for dataset URL; can only contain alpha-numeric characters and \'_\''
                            ),
                make_option('--species_column',
                            action='store',
                            type='string',
                            default=None,
                            help='column containing species names or ids'
                            ),
                make_option('--annotation_column',
                            action='store',
                            type='string',
                            default=None,
                            help='column containing boolean flag to indicate whether the data file in this row should be treated as an annotation file'
                            ),
                make_option('--genome_build_column',
                            action='store',
                            type='string',
                            default=None,
                            help='column containing genome build ids'
                            ),
                make_option('--data_file_permanent',
                            action='store_true',
                            default=False,
                            help='flag for whether data files should be permanently on the system or cached'
                            ),
                make_option('--is_public',
                            action='store_true',
                            default=False,
                            help='flag for whether this data set will be visible to the public'
                            ),
                )

    def handle(self, *args, **options):
        """Name: handle
        Description: main program; calls the parsing and insertion functions

        """
        required = ['username', 'title', 'file_name', 'source_column_index', 'data_file_column']
        for arg in required:
            if not options[arg]:
                raise CommandError('%s was not provided.' % arg)

        parser = SingleFileColumnParser()
        parser.file_permanent = options['data_file_permanent']
        parser.file_column_index = int( options['data_file_column'] )
        parser.source_column_index = [int(x.strip()) for x in options['source_column_index'].split(",")]
        parser.column_index_separator = "/"
        parser.file_base_path = options['base_path']
        
        if options['auxiliary_file_column'] is not None:
            parser.auxiliary_file_column_index = int( options['auxiliary_file_column'] )
        
        if options['species_column'] is not None:
            parser.species_column_index = int( options['species_column'] )
        
        if options['genome_build_column'] is not None:
            parser.genome_build_column_index = int( options['genome_build_column'] )                
        
        if options['annotation_column'] is not None:
            parser.annotation_column_index = int( options['annotation_column'] )                
        
        investigation = parser.run(options['file_name'])
        investigation.title = options['title']
        investigation.save()
        
        create_dataset(investigation_uuid=investigation.uuid,
                       username=options['username'],
                       dataset_title=options['title'],
                       slug=options['slug'],
                       public=options['is_public'])
