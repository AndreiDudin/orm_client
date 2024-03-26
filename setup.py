from setuptools import setup
REQUIRES = [
    'records',
    'structlog',
    'sqlalchemy'
]
setup(
    name='orm_client',
    version='0.0.1',
    packages=['orm_client'],
    url='https://github.com/AndreiDudin/orm_client.git',
    license='MIT',
    author='Andrey Dudin',
    author_email='.',
    install_requires=REQUIRES,
    description='restclient with allure and logger'
)
