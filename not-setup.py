from setuptools import setup
import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='Y360 API Scripts',
    version='0.0.1',
    description='Scripts to help interacting with Y360 REST API',
    url='https://github.com/gavingreenhorn/Y360_Scripts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points = {
        "console_scripts": [
            "users = scripts.users:main",
            "groups = scripts.groups:main"
        ]
    },
    author='GavinGreenhorn',
    python_requires='>=3.9',
    install_requires=['python-dotenv', 'requests-cache', 'prettytable'],
    license='MIT',
    packages= setuptools.find_packages()
)