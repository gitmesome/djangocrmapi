# Django Product API

This reusable Django app exposes a read-only API for the Product model using Django REST Framework.

Update the webcrm/urls.py file as follows:
```python
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
```

To specify which products will be exosed, add the following line.  If this is not add
you will get an error:
```python
PUBLIC_PRODUCTS=[1,2,5,8,11,14]
```

```python
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
```

