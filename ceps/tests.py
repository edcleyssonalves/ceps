import io
import os
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from django.db import IntegrityError
from ceps.models import Cep


class CepModelTests(TestCase):
    def test_str(self):
        cep = Cep.objects.create(cep="12345-678", logradouro="Rua Teste", bairro="Bairro", cidade="Cidade")
        self.assertEqual(str(cep), "12345-678 - Rua Teste")

    def test_unique_cep_constraint(self):
        Cep.objects.create(cep="11111-111", logradouro="Rua A", bairro="B", cidade="C")
        with self.assertRaises(IntegrityError):
            Cep.objects.create(cep="11111-111", logradouro="Rua B", bairro="B2", cidade="C2")


class CepListViewTests(TestCase):
    def setUp(self):
        self.cep = Cep.objects.create(cep="58200-001", logradouro="Rua das Flores", bairro="Centro", cidade="Guarabira")
        self.client = Client()

    def test_search_short_query_returns_warning(self):
        resp = self.client.get(reverse('ceps') + '?search=ru')
        self.assertEqual(resp.status_code, 200)
        # When a short query is provided (<3 chars) view returns no results and template shows warning
        self.assertContains(resp, "Nenhum endereço encontrado")

    def test_search_valid_query_returns_results(self):
        resp = self.client.get(reverse('ceps') + '?search=Flores')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Rua das Flores")
        self.assertContains(resp, "58200-001")

    def test_search_with_street_prefix(self):
        resp = self.client.get(reverse('ceps') + '?search=Rua das Flores')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Rua das Flores")

    def test_search_with_falsey_but_long_object_triggers_not_search(self):
        # Create an object that reports length >= 3 but evaluates as False
        class FakeStr:
            def lower(self):
                return self

            def strip(self):
                return self

            def __len__(self):
                return 3

            def __bool__(self):
                return False

        class DummyGET:
            def __init__(self, value):
                self._value = value

            def get(self, key, default=''):
                return self._value

        from types import SimpleNamespace
        from ceps.views import CepListView

        view = CepListView()
        view.request = SimpleNamespace(GET=DummyGET(FakeStr()))

        qs = view.get_queryset()
        # Should return empty queryset because 'not search' branch is hit
        self.assertFalse(qs.exists())


class ImportCommandTests(TestCase):
    def test_import_command_creates_objects_and_ignores_missing_cep(self):
        dummy = 'IGNORED LINE\n'
        header = 'Localidade;Logradouro;CEP;Bairro;Tipo Codificação;Numero Inicial;Número Final;Trecho;Lado\n'
        row1 = 'Guarabira;Rua Teste;11111-111;Bairro Teste;Tipo;1;10;Trecho;L\n'
        row2 = 'Guarabira;Rua SemCep;;Bairro2;Tipo;1;10;Trecho;L\n'  # missing CEP should be skipped

        tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        try:
            tmp.write(dummy)
            tmp.write(header)
            tmp.write(row1)
            tmp.write(row2)
            tmp.flush()
            tmp_name = tmp.name
        finally:
            tmp.close()

        out = io.StringIO()
        call_command('importar_cep', tmp_name, stdout=out)

        self.assertTrue(Cep.objects.filter(cep='11111-111').exists())
        self.assertFalse(Cep.objects.filter(logradouro='Rua SemCep').exists())
        self.assertIn('CEPS IMPORTADOS COM SUCESSO', out.getvalue())

        os.remove(tmp_name)
