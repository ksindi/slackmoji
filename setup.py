import textwrap

from setuptools import setup, find_packages

with open('README.md') as f_readme:
    readme = f_readme.read()

setup(
    name='slackmoji',
    description='Upload custom emojis to Slack',
    long_description=readme,
    packages=find_packages(),
    use_scm_version=True,
    author='Kamil Sindi',
    author_email='ksindi@ksindi.com',
    url='https://github.com/ksindi/slackmoji',
    keywords='slack emoji'.split(),
    license='MIT',
    install_requires=[
        'requests>=2.18.4',
        'requests-html>=0.9.0',
        'pyaml>=17.12.1',
        'python-box>=3.1.1',
    ],
    setup_requires=[
        'pytest-runner',
        'setuptools_scm',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-flake8',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=textwrap.dedent("""
        Development Status :: 5 - Production/Stable
        License :: OSI Approved :: MIT License
        Environment :: Console
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.6
        """).strip().splitlines(),
)
