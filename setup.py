from setuptools import setup

setup(
    name='DynamicForaging',
    version='1.0.2',
    author='Peiheng',
    author_email='s1948149@ed.ac.uk',
    packages=['analysis', 'analysis.benchmark', 'analysis.models', 'test', 'hardware', 'database', 'test'],
    # description='An awesome package that does something',
    install_requires=[
        "seaborn",
        "pandas"
    ],
)