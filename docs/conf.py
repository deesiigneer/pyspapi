from re import search, MULTILINE
import os
import sys


project = 'pyspapi'
copyright = '2022, deesiigneer'
author = 'deesiigneer'
with open("../pyspapi/__init__.py") as f:
    match = search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), MULTILINE)

    if not match or match.group(1) is None:
        raise RuntimeError("The version could not be resolved")

    version = match.group(1)

# The full version, including alpha/beta/rc tags.
release = version

# -- General configuration

sys.path.insert(0, os.path.abspath(".."))


extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

autodoc_member_order = "bysource"
autodoc_typehinta = "none"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

version_match = os.environ.get("READTHEDOCS_VERSION")
json_url = f"https://pyspapi.readthedocs.io/ru/{version_match}/_static/switcher.json"

intersphinx_disabled_domains = ['std']
language = 'en'
locale_dirs = ["locale/"]
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
        }
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/deesiigneer/pyspapi",
            "icon": "fab fa-brands fa-github",
            "type": "fontawesome"
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/VbyHaKRAaN",
            "icon": "fab fa-brands fa-discord",
            "type": "fontawesome"
        },
        {
            "name": "PyPi",
            "url": "https://pypi.org/project/pyspapi/",
            "icon": "fab fa-brands fa-python",
            "type": "fontawesome"
        }
    ],
    "header_links_before_dropdown": 4,
    "show_toc_level": 1,
    "navbar_start": ["navbar-logo"],
    "navigation_with_keys": True,
}
html_css_files = ["custom.css"]
