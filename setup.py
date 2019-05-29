import setuptools

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()



setuptools.setup(
    name="textda",
    version="0.1.0.5",
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