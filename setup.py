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
        "progressbar2",
        "requests",
        "sqlalchemy",
        "orjson",
    ],
    entry_points={
        "console_scripts": [
            "xtract=src.wikixtractor.extract_db_from_latest:main",
            "ingest_views=src.wikixtractor.apply_viewdata:main",
            "upload=src.wikixtractor.launch_to_api:main",
        ],
    },
)
