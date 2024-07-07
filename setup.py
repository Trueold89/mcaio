from setuptools import setup

setup(
    name="mcaio",
    version="0.1",
    url="https://git.orudo.ru/trueold89/mcaio",
    author="trueold89",
    author_email="trueold89@orudo.ru",
    description="Asynс lib to get information about Minecraft server",
    packages=["mcaio"],
    entry_points={
        "console_scripts": ["mcaio = mcaio.cli:main"]
    }
)
