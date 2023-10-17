"""Installation script for the moocloze library.

Adapted from
https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/.
"""

import os
import configparser
from setuptools import setup, find_packages


# Read the configuration from moocloze.ini, section [moocloze]
ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moocloze.ini")
moocloze_options = configparser.ConfigParser()
moocloze_options.read(ini_path)
moocloze_options = moocloze_options["moocloze"]

setup_package_list = ["setuptools", "wheel"]

with open("README.md", "r") as readme_file:
    setup(
        # Metadata about the project
        name=moocloze_options["name"],
        version=moocloze_options["version"],
        url=moocloze_options["url"],
        download_url=moocloze_options["download_url"],
        license=moocloze_options["license"],
        author=moocloze_options["author"],
        author_email=moocloze_options["author_email"],
        description=moocloze_options["description"],
        long_description=readme_file.read(),
        long_description_content_type="text/markdown",
        platforms=moocloze_options["platforms"],
        python_requires=moocloze_options["python_requires"],
        classifiers=[
            "Programming Language :: Python",
            f"Development Status :: {moocloze_options['development_status']}",
            "Natural Language :: English",
            "Environment :: Console",
            "Intended Audience :: Developers",
            f"License :: OSI Approved :: {moocloze_options['license']}",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering",
        ],

        # Dependencies
        setup_requires=setup_package_list,

        install_requires=[],

        # This part determines the contents of the installed folder in your python's
        # site-packages location.
        # MANIFEST.in is assumed to have been updated, i.e., via git hooks.
        # This allows core plugins and templates to be automatically included.
        packages=[p for p in find_packages() if p.startswith("moocloze")],
        include_package_data=True)
