from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
setup(
    name="slang",
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'aiohappyeyeballs>=2.4.4',
        'aiohttp>=3.11.11',
        'aiosignal>=1.3.2',
        'attrs>=24.3.0',
        'Brotli>=1.1.0',
        'chardet>=5.2.0',
        'click>=8.1.8',
        'fake-useragent>=2.0.3',
        'frozenlist>=1.5.0',
        'idna>=3.10',
        'markdown-it-py>=3.0.0',
        'mdurl>=0.1.2',
        'msgspec>=0.19.0',
        'multidict>=6.1.0',
        'propcache>=0.2.1',
        'Pygments>=2.18.0',
        'rich>=13.9.4',
        'shellingham>=1.5.4',
        'typer>=0.15.1',
        'typing_extensions>=4.12.2',
        'yarl>=1.18.3'
    ],
    entry_points = {
        "console_scripts":[
            "slang = slang.cli:app" 
        ]
    },
    long_description=description,
    long_description_content_type='text/markdown',

    
)


#long_description=description
#long_description_content_type="text/markdown"