from importlib.metadata import version as pkg_version
import os

project = "pyspapi"
author = "deesiigneer"
copyright = "2022, deesiigneer"

version = pkg_version("pyspapi")
release = version

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

autosummary_generate = True

version_match = os.environ.get("READTHEDOCS_VERSION")
json_url = f"https://pyspapi.readthedocs.io/ru/{version_match}/_static/switcher.json"


language = "ru"
exclude_patterns = []
html_static_path = ["_static"]

html_theme = "pydata_sphinx_theme"
html_logo = "./images/logo.png"
html_favicon = "./images/logo.ico"

html_theme_options = {
    "external_links": [
        {
            "url": "https://github.com/deesiigneer/pyspapi/releases",
            "name": "Changelog",
        },
        {
            "url": "https://github.com/sp-worlds/api-docs/wiki",
            "name": "SPWorlds API Docs",
        }
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/deesiigneer/pyspapi",
            "icon": "fab fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/VbyHaKRAaN",
            "icon": "fab fa-brands fa-discord",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pyspapi/",
            "icon": "fab fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
    "header_links_before_dropdown": 4,
    "show_toc_level": 1,
    "navbar_start": ["navbar-logo"],
    "navigation_with_keys": True,
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
}
