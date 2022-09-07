from setuptools import setup

setup(
    name='DynamicForaging',
    version='0.1.0',
    author='Peiheng',
    author_email='aac@example.com',
    packages=['analysis', 'test', 'hardware', 'database'],
    # description='An awesome package that does something',
    install_requires=[
        "seaborn",
        "pandas"
    ],
)