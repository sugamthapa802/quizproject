
# import os
# import csv
# from django.core.management.base import BaseCommand
# from quizapp.models import Topic,Question
# from django.shortcuts import get_object_or_404

# class Command(BaseCommand):
#     help='load the questions from csv file to database.'

#     def add_arguments(self, parser):
#         parser.add_argument('topic_name',type=str)


#     """
#     get the Topic or create if not exists
#     give the file path
#     if no file path exists:
#         return ('no file as such')

#     open file as csvfile :
#         create a instance of file reader
#         read every row:
#             make new instance of Question(
#                 for every row
#             )    
#     """

#     def handle(self, *args, **options):
#         topic_name=options['topic_name']
#         topic,created=Topic.objects.get_or_create(name=topic_name)
#         file_path=os.path.join('quizapp','data',f'{topic_name.lower()}.csv')
        
#         if not file_path:
#             self.stdout.write(self.style.ERROR(f'file not found:{file_path}'))
#             return
        
#         with open(file_path,newline='',encoding='utf-8') as csvfile:
#             reader= csv.reader(csvfile)
#             header=next(reader)

#             for row in reader:
#                 if len(row)<8:
#                     continue
#                 Question.objects.create(
#                         topic=topic,
#                         question_text=row[1],
#                         option_a=row[2],
#                         option_b=row[3],
#                         option_c=row[4],
#                         option_d=row[5],
#                         correct_option=row[6],
#                         explanation=row[7]
#                 )
#             self.stdout.write(self.style.SUCCESS(f'successfully imported questions for topic :{topic_name}'))
import os
import csv
from django.core.management.base import BaseCommand
from quizapp.models import Topic, Question

class Command(BaseCommand):
    help = 'Load questions from a CSV file to the database.'

    def add_arguments(self, parser):
        parser.add_argument('topic_name', type=str, help='Name of the topic in the database.')
        parser.add_argument(
            '--csvfile',
            type=str,
            help='Optional CSV filename (located in quizapp/data). If omitted, uses topic_name.lower().csv'
        )
 
    def handle(self, *args, **options):
        topic_name = options['topic_name']
        csvfile = options.get('csvfile')

        # Get or create the topic
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # Determine the file path
        if csvfile:
            file_path = os.path.join('quizapp', 'data', csvfile)
        else:
            # Replace spaces with underscores or keep spaces? 
            # Your choice. For now, keep spaces as-is:
            file_path = os.path.join('quizapp', 'data', f'{topic_name.lower()}.csv')

        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # skip header if present

            created_count = 0
            for row in reader:
                if len(row) < 8:
                    continue  # skip invalid rows
                
                Question.objects.create(
                    topic=topic,
                    question_text=row[1],
                    option_a=row[2],
                    option_b=row[3],
                    option_c=row[4],
                    option_d=row[5],
                    correct_option=row[6],
                    explanation=row[7]
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully imported {created_count} questions for topic: {topic_name}'
        ))
