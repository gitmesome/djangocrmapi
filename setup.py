from setuptools import setup, find_packages

setup(
    name='djangocrmapi',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',
        'djangorestframework>=3.14',
        'bleach>=6.0',
        'django_extensions',
        'django-cors-headers',
        'google-cloud-recaptcha-enterprise',
    ],
    description='Reusable DRF app for exposing Product read-only API',
    author='Christian Ullman',
    license='MIT',
)
