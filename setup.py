import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))
meta_info = {}
with open(os.path.join(here, 'Artesian', '_package_info.py'), 'r') as f:
    exec(f.read(), meta_info)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=meta_info['__title__'],
    version=meta_info['__version__'],
    author=meta_info['__author__'],
    author_email=meta_info['__author_email__'],
    description=meta_info['__description__'],
    url=meta_info['__url__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=meta_info['__license__'],
    packages=setuptools.find_packages(include=["Artesian.*"], exclude=["test.*"]),
    py_modules = ['Artesian'], 
    install_requires=[
        'requests',
        'six',
        'asyncio',
        'jsons>=1.6.1',
        'dataclasses',
        'python-dateutil',
        #'typing-compat' # needed for get_args in 3.7 
    ],
    python_requires='>=3.8',
    extras_require={
        'test': [
            'responses>=0.18'
            #ideal will be 0.19 WHEN published
        ],
        'release': [
            'twine'
        ]
    },
    test_suite='test',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",        
        "Programming Language :: Python :: 3",
        *['Programming Language :: Python :: {}'.format(version)
          for version in meta_info['__python_versions__']],
    ]
	)
