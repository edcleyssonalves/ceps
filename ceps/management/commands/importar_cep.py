import csv
from django.core.management.base import BaseCommand
from ceps.models import Cep


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo a ser importado .csv',
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]
            reader = csv.DictReader(lines, delimiter=';')
            print(reader.fieldnames)
            for raw in reader:
                cidade = raw['Localidade']
                logradouro = raw['Logradouro']
                cep = raw['CEP']
                if not cep:
                    continue
                bairro = raw['Bairro']
                tipo_codificacao = raw['Tipo Codificação']
                numero_inicial = raw['Numero Inicial']
                numero_final = raw['Número Final']
                trecho = raw['Trecho']
                lado = raw['Lado']

                self.stdout.write(self.style.NOTICE(f'importando: {cep} - {logradouro}'))

                Cep.objects.create(
                    cidade=cidade,
                    logradouro=logradouro,
                    cep=cep,
                    bairro=bairro,
                    tipo_codificacao=tipo_codificacao,
                    numero_inicial=numero_inicial,
                    numero_final=numero_final,
                    trecho=trecho,
                    lado=lado,
                )

        self.stdout.write(self.style.SUCCESS('CEPS IMPORTADOS COM SUCESSO'))
