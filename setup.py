from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

setup(
    name='taxodist',
    version='0.0.0',
    url='https://github.com/janschneida/taxodist',
    license='MIT',
    author='Jan Janosch Schneider',
    author_email='janjanosch.schneider@med.uni-goettingen.de',
    description='Package for distance calculations of concepts in taxonomic hierarchies.',
    long_description=README,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.9.6",
    install_requires=['scipy>=1.3.1','numpy>=1.16.5', 'scikit-learn>=0.21.3', 'pandas>=0.25.1', 'treelib==1.6.1']
)