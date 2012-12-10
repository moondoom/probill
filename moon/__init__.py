

def autodiscover():
    from models import MenuItems
    from django.conf import settings
    from django.utils.importlib import import_module
    MenuItems.objects.all().delete()
    for app in settings.INSTALLED_APPS:
        import_module(app)
        try:
            import_module('%s.menu' % app)
        except ImportError:
            pass
