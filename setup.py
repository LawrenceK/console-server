from setuptools import setup
import sys
import os
import shutil
setup_base = os.path.dirname(os.path.abspath(__file__))

data_files = [
    ('/etc/init.d', [os.path.join(setup_base, 'etc/init.d/consoleserver'), ]),
    ('/etc/logrotate.d', [os.path.join(setup_base, 'etc/logrotate.d/consoleserver'), ]),
    ('/etc/udev/rules.d', [os.path.join(setup_base, 'etc/udev/rules.d/99-usb-blacklist.rules'), ])
]

setup(
    name="ConsoleServer",
    version="1.0.2",
    description="This is a logging console server that can also be accessed over ssh.",
    long_description=file('README.rst').read(),
    packages=['consoleserver', ],
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        'twisted>=10.2',
        'pyserial>=2.5',
        'configobj>=4.7',
        'pycrypto>=2.3',
        'pyasn1',
    ],

    data_files=data_files,

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
    url='https://github.com/LawrenceK/console-server',  # github
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
)

if 'xinstall' in sys.argv:
    # conditional copy of some files.
    for target, sources in data_files:
        for source in sources:
            targetname = os.path.join(target, os.path.basename(source))
            print targetname, os.listdir(os.path.dirname(source))
            if not os.path.exists(targetname):
                if not os.path.exists(target):
                    os.makedirs(target)
                shutil.copy2(source, targetname)
