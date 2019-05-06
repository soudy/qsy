from setuptools import setup, find_packages
import re


with open('./qsy/__init__.py') as f:
    version, = re.findall('__version__ = \'(.*)\'', f.read())

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='qsy',
    version=version,
    packages=find_packages(),
    author='Steven Oud',
    author_email='soud@pm.me',
    description='A quantum computer state vector/stabilizer circuit simulator and assembly language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/soudy/qsy',
    license='MIT',
    install_requires=['numpy>=1.13', 'ply>=3'],
    download_url='https://github.com/soudy/qsy/archive/v{}.tar.gz'.format(version),
    keywords=['quantum', 'computing', 'simulator', 'stabilizer', 'circuit',
              'assembly', 'chp', 'statevector'],
    entry_points={
        'console_scripts': ['qsyasm=qsyasm.cli:main']
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Assemblers'
    ]
)
