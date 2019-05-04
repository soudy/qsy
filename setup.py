from setuptools import setup, find_packages
import re


with open('./qsy/__init__.py') as f:
    version, = re.findall('__version__ = \'(.*)\'', f.read())

setup(
    name='qsy',
    version=version,
    packages=find_packages(),
    author='Steven Oud',
    author_email='soud@pm.me',
    description='A quantum computer state vector/stabilizer circuit simulator and assembly language',
    license='MIT',
    install_requires=['numpy>=1.13', 'ply>=3'],
    entry_points = {
        'console_scripts': ['qsyasm=qsyasm.cli:main']
    }
)
