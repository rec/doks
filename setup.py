import doks

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

if __name__ == '__main__':
    from setuptools import setup

    setup(
        name='doks',
        version=doks.__version__,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/doks',
        tests_require=['pytest'],
        py_modules=['doks'],
        description='Automatically generated READMEs',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['documentation'],
        scripts=['scripts/doks'],
        packages=['doks'],
        data_files=[('', ['shields.yml'])],
        install_requires=REQUIRED,
    )
