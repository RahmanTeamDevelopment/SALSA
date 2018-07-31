from setuptools import setup

exec(open('main/version.py').read())

setup(
    name='PLATYPUS',
    version=__version__,
    description='Wrapper for platypus and install',
    url='blabla',
    author='Shawn Yost',
    author_email='yostshawn@gmail.com',
    licence='MIT',
    packages=['main'],
    scripts=['bin/Platypus.py'],
    zip_safe=False
)
