import re
from django.views.generic import ListView
from ceps.models import Cep
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


@method_decorator(ratelimit(key="ip", rate="30/m", block=True), name="dispatch")
class CepListView(ListView):
    model = Cep
    template_name = "cep.html"
    context_object_name = "ceps"

    def get_queryset(self):
        search = self.request.GET.get("search", "").lower().strip()

        if len(search) < 3:
            return Cep.objects.none()
        if not search:
            return Cep.objects.none()

        search = re.sub(
            r"\b(rua|r\.|avenida|av\.|travessa|tv\.)\b",
            "",
            search,
        ).strip()

        return (
            Cep.objects
            .filter(logradouro__icontains=search)
            .order_by("logradouro")[:1]
        )
