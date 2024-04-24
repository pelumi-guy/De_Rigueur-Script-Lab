import setuptools

setuptools.setup(
    include_package_data=False,
    name='ListingsPreprocessor',
    version='0.0.1',
    description='Listings Preprocessor python module',
    url='https://github.com/pelumi-guy/De_Rigueur-Script-Lab',
    author='one_pelumi_guy',
    author_email='pelumi.olalekan.g@limeguru.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'gspread',
        'pillow'
    ],
    long_description='Listings Preprocessor python module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)