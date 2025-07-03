from .models import SiteSetup

def meu_context_exemplo(request):
    return {
        'nome_qualquer': request.user
    }


def site_setup(request):

    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup
    }