from setuptools import setup, find_packages
setup(
    name="ConsoleServer",
    version="0.2",
    description="This is a logging console server that can also accessed over ssh.",
    packages=find_packages(),
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        'twisted>=12.2',
        'pyserial>=2.5',
        'configobj>=4.7',
        'pycrypto',
        'pyasn1',
    ],

    package_data={
        '': ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'consoleserver = consoleserver.main:main',
        ]
    },

    # metadata for upload to PyPI
    author="Lawrence P. Klyne",
    author_email="pypi@lklyne.co.uk",
    license='GPL',
    keywords=[
        'console',
        'server',
        'ssh',
        'serial',
    ],
    url="",  # github
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
)
