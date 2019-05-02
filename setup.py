from setuptools import setup, find_packages

setup(
    name='qsy',
    version='0.2',
    packages=find_packages(),
    author='Steven Oud',
    author_email='soud@pm.me',
    description='A quantum computer state vector simulator and quantum assembly language',
    license='MIT',
    install_requires=['numpy>=1.13', 'ply>=3'],
    entry_points = {
        'console_scripts': ['qsyasm=qsyasm.cli:main']
    }
)
