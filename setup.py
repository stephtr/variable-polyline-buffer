from setuptools import setup, find_packages

setup(
    name="variable_polyline_buffer",
    version="0.1.7",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description="A function for calculating a buffer around a polyline, defining the contours of a line with variable thickness.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Stephan Troyer",
    author_email="stephantroyer@live.at",
    url="https://github.com/stephtr/variable-polyline-buffer",
    install_requires=[
        "numpy",
    ],
)
