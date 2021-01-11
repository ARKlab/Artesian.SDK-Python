import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="artesian-sdk",
    version="2.2.1",
    author="Ark-Lab",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author_email="niccolo.cecchi@ark-energy.eu",
    description="Library provides read access to the Artesian API",
    url="https://github.com/ARKlab/Artesian.SDK-Python",
    packages=setuptools.find_packages(),
    py_modules = ['artesian'], 
    install_requires=[
        'requests',
        'six'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
	)
