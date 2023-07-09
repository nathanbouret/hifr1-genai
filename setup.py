# -*- coding: utf-8 -*-
"""
Created on Fri Jun  30 18:00:33 2023

@author: hadjahmed
"""
from setuptools import setup, find_packages
import sys

# To prevent users from accidentally publishing the package in PyPi repository


def forbid_publish():
    argv = sys.argv
    blacklist = ['register', 'upload', 'testarg']

    for command in blacklist:
        if command in argv:
            values = {'command': command}
            print('Command "%(command)s" has been blacklisted, exiting...' % values)
            sys.exit(2)


forbid_publish()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="HIFR1-GENAI",
    version="0.0.1",
    author="HI France - HIFR1-GENAI Team",
    description="HIFR1-GENAI project code from Capgemini Development Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(include=['.*']),
    install_requires=[
                    'google-cloud-aiplatform==1.27.0',
                    'numpy==1.25.0',
                    'pydantic==1.10.8',
                    'streamlit==1.24.0',
                    'cachetools==5.3.1',
                    'certifi==2023.5.7',
                    'charset-normalizer==3.1.0',
                    'google-api-core==2.11.1',
                    'google-auth==2.21.0',
                    'googleapis-common-protos==1.59.1',
                    'grpcio==1.56.0',
                    'grpcio-status==1.56.0',
                    'pypdf==3.12.0',
                    'pycryptodome==3.18.0',
                    'idna==3.4',
                    'proto-plus==1.22.3',
                    'protobuf==4.23.3',
                    'pyasn1==0.5.0',
                    'pyasn1-modules==0.3.0',
                    'requests==2.31.0',
                    'rsa==4.9',
                    'six==1.16.0',
                    'urllib3==1.26.16',
                    'google-cloud-documentai==2.16.0',
                    'streamlit-chat==0.1.1',
                    'langchain==0.0.222'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.8',
)