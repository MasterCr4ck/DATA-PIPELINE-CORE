from setuptools import setup, find_packages

setup(
    name="data-pipeline-core",
    version="2.0.0",
    description="Core reutilizable para pipelines de datos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    author="Dieo Ortiz Puerto",
    python_requires=">=3.10",

    packages=find_packages(exclude=("tests*",)),
    include_package_data=True,

    install_requires=[
        "pandas>=2.0",
        "sqlalchemy>=2.0",
        "pyyaml>=6.0",
        "pymysql>=1.0",
        "yaml>=6.0.3"
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
