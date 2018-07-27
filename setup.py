from setuptools import setup

exec(open('main/version.py').read())

setup(
    name='SALSA',
    version=__version__,
    description='Software package used to process targeted panel sequencing data for germline genetic testing',
    url='blabla',
    author='Shawn Yost',
    author_email='yostshawn@gmail.com',
    licence='MIT',
    packages=['main'],
    scripts=['bin/SALSA.py'],
    zip_safe=False
)
