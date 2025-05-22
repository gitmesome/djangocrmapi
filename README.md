# Django Product API

This reusable Django app exposes a read-only API for the Product model using Django REST Framework.

Update the webcrm/urls.py file as follows:

urlpatterns = [
    path('favicon.ico', FaviconRedirect.as_view()),
    path('voip/', include('voip.urls')),
    path(
        'OAuth-2/authorize/',
        staff_member_required(get_refresh_token), 
        name='get_refresh_token'
    ),   
    path('api/', include('djangocrmapi.urls', namespace='djangocrmapi')),
]

For better logging, add the following to webcrm/settings.py:
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

