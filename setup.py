from setuptools import setup

setup(
    name='DynamicForaging',
    version='1.1.0',
    author='Peiheng',
    author_email='s1948149@ed.ac.uk',
    packages=['lib', 'lib.benchmark', 'lib.hardware', 'lib.database', 'lib.ui', 'lib.visualization'],
    # description='An awesome package that does something',
    install_requires=[
        "seaborn",
        "pandas"
    ],
)