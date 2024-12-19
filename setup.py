from setuptools import setup, find_packages

setup(
    name='slang-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer>=0.9.0',
        'rich>=13.9.4',
        # Add other dependencies
    ],
    entry_points={
        'console_scripts': [
            'slang=slang.cli:app',
        ],
    },
    author='Abdisa Merga',
    author_email='abdisamk@gmail.com',
    description='A CLI app for interacting with AI models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/slang-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)



