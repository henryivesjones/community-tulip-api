import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="community-tulip-api",
    author="Henry Jones",
    author_email="henryivesjones@gmail.com",
    description="A community wrapper for the Tulip API",
    url="https://github.com/henryivesjones/community-tulip-api",
    packages=["tulip_api", "tulip_api.asyncio"],
    package_dir={"tulip_api": "tulip_api", "tulip_api.asyncio": "tulip_api/asyncio"},
    package_data={"tulip_api": ["py.typed"], "tulip_api.asyncio": ["py.typed"]},
    include_package_data=True,
    install_requires=["requests", "aiohttp", "python-dateutil"],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "LICENSE :: OSI APPROVED :: GNU AFFERO GENERAL PUBLIC LICENSE V3",
    ],
)
