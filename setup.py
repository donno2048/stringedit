from setuptools import setup, find_packages
setup(
    name='stringedit',
    version='1.0.0',
    license='MIT',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description='Replace strings in binary files.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/stringedit',
    project_urls={
        'Documentation': 'https://github.com/donno2048/stringedit#readme',
        'Bug Reports': 'https://github.com/donno2048/stringedit/issues',
        'Source Code': 'https://github.com/donno2048/stringedit',
    },
    python_requires='>=3.0',
    packages=find_packages(),
    install_requires=["prompt_toolkit"],
    entry_points={ 'console_scripts': [
        'stringed=stringedit.__main__:edit_strings',
        'stringpr=stringedit.__main__:print_strings',
    ] }
)
