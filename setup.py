'''
python3 setup.py bdist_wheel --universal



HTTPError: 400 Client Error: The description failed to render in the default format of reStructuredText

solved:
If you're using a Markdown long_description:
The metadata for your distribution is invalid and is not specifying Markdown.

This means that either you haven't set long_description_content_type='text/markdown', in your setup.py file, or that the tools that you're using are out of date and don't support this metadata field. Upgrade them to latest:

$ pip install -U twine wheel setuptools

'''

import setuptools

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()



setuptools.setup(
    name="textda",
    version="0.1.0.6",
    author="wac",
    author_email="wuanch@gmail.com",
    description="this is data augmentation for chinese text",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/wac81/textda",
    packages=setuptools.find_packages(),
    keywords='classification,expansion,augmentation,addition,data,text,chinese',
    license="MIT",
    package_data={
    'textda': [
            '**/*.gz',
            '**/*.txt',
            '**/*.vector',
        ]
    },

    install_requires=['jieba',
                      'synonyms'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)