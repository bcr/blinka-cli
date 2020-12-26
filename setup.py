import setuptools

setuptools.setup(
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['blinka=blinka.__main__:main'],
    },
)
