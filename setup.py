from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

setup(
    name='taxodist',
    version='v0.0.0',
    url='https://github.com/janschneida/taxodist',
    license='MIT',
    author='Jan Janosch Schneider',
    author_email='janjanosch.schneider@med.uni-goettingen.de',
    description='Package for distance calculations of concepts in taxonomic hierarchies.',
    #long_description=README,
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.9.6",
    install_requires=['numpy>=1.21.1', 'scikit-learn>=0.24.2', 'pandas>=1.3.0', 'treelib==1.6.1']
)