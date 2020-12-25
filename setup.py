import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blinka-bcr",
    version="0.0.1",
    author="Blake Ramsdell",
    author_email="blaker@gmail.com",
    description="Command-line utility for CircuitPython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bcr/blinka-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
