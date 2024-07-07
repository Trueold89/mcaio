from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mcaio",
    version="0.1",
    url="https://git.orudo.ru/trueold89/mcaio",
    author="trueold89",
    author_email="trueold89@orudo.ru",
    description="Asynс lib to get information about Minecraft server",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["mcaio"],
    entry_points={
        "console_scripts": ["mcaio = mcaio.cli:main"]
    }
)
