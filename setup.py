import setuptools

setuptools.setup(
    name="wikixtractor",
    version="0.1.0",
    author="Eric Hennenfent",
    author_email="ecapstone@gmail.com",
    description="Extract wikipedia articles from XML dumps",
    url="https://github.com/ehennenfent/wikixtractor",
    packages=setuptools.find_packages(),
    keywords="mediawiki",
    install_requires=[
        "mwparserfromhell",
        "progressbar2",
    ],
    entry_points={
        "console_scripts": ["xtract=src.wikixtractor.visit_person:main"],
    },
)
