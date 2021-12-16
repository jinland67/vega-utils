from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vega-utils',
    version='0.1.0',
    author='jinland',
    author_email='jinland@bommaru.com',
    description='Library for using string, date and networ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jinland-bommaru/vega_utils.git',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.10',
    install_requires=[
        'pytz >= 2021.3',
        'python-dateutil >= 2.8.2',
        'psutil >= 5.8.0',
        'slack-sdk >= 3.11.2'
    ],
    package_data={"web_driver": ["*.txt"]},
    include_package_data=True,
)