import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'sqlite3',
    'py-bcrypt'
    ]

setup(name='login',
      version='0.0',
      description='login',
      author='Ashish Pandhi',
      author_email='ashish@pandhi.me',
      url='pandhi.me',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="login",
      entry_points="""\
      [paste.app_factory]
      main = login:main
      """,
      )
