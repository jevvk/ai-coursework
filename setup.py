# -*- coding: utf-8 -*-
with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ai-coursework',
    version='0.0.1',
    description='AI coursework',
    long_description=readme,
    author='Emilian Simion, Eugen Patru, Razvan Lacatusu',
    url='https://github.com/linoimi/ai-coursework',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
