from setuptools import setup
import abbrev

_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

if __name__ == '__main__':
    setup(
        name='abbrev',
        version=abbrev.__version__,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/abbrev',
        tests_require=['pytest'],
        py_modules=['abbrev'],
        description='A dictionary that allows abbreviations',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['testing', 'modules'],
        scripts=['abbrev.py'],
    )
