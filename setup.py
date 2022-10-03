import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="community-tulip-api",
    version="0.1.1",
    author="Henry Jones",
    author_email="henryivesjones@gmail.com",
    description="A community wrapper for the Tulip API",
    license="GPLv3",
    keywords="tulip api",
    url="https://github.com/henryivesjones/community-tulip-api",
    packages=["tulip_api"],
    package_dir={"tulip_api": "tulip_api"},
    install_requires=["requests"],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "LICENSE :: OSI APPROVED :: GNU AFFERO GENERAL PUBLIC LICENSE V3",
    ],
)
