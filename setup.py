import re

from setuptools import setup

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("pyspapi/__init__.py") as f:
    match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if match is None or match.group(1) is None:
        raise RuntimeError('Version is not set')

    version = match.group(1)

if not version:
    raise RuntimeError("Version is not set")

readme = ""
with open("README.rst") as f:
    readme = f.read()

packages = [
    "pyspapi"
]

setup(
    name='pyspapi',
    license='MIT',
    author='deesiigneer',
    version=version,
    url='https://github.com/deesiigneer/pyspapi',
    project_urls={
        "Documentation": "https://pyspapi.readthedocs.io/ru/latest/",
        "GitHub": "https://github.com/deesiigneer/pyspapi",
        "Discord": "https://discord.com/invite/VbyHaKRAaN"
    },
    description='API wrapper for SP servers written in Python',
    long_description=readme,
    long_description_content_type='text/x-rst',
    packages=packages,
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8.0',
)
