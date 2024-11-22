from setuptools import setup, find_packages


setup(
    name="SnmpPyLite",
    version="0.1.0",
    author="Evgeny Ockatiev",
    author_email="evgeny.ockatiev@gmail.com",
    description="SNMP Python Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/katzeNilpferd/SnmpPyLite",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "flake8"],
    },
)