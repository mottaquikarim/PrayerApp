from setuptools import find_packages, setup

setup(
    name='prayerapp',
    version='0.0.1',
    description='Prayer App',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
    setup_requires=['wheel'],
    )

