from setuptools import setup, find_packages

version = '0.1'

setup(name='speck',
      version=version,

      description="Speck makes python testing better.",
      long_description="",

      author='Vaz',
      author_email='vaz@tryptid.com',
      url='http://github.com/vaz/speck',
      license='WTFPL',

      install_requires=[
      ],

      entry_points="""
      # -*- Entry points: -*-
      """,

      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,

      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Religion",
          "License :: Freeware",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          # TODO: Python 3,
          "Topic :: Software Development :: Testing"

      ],
      keywords='python test unit spec expectation should matcher',
      )
