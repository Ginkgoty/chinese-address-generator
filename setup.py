from setuptools import setup, find_packages

setup(
    name='chinese_address_generator',
    version='0.2.0',
    description='Random generation of Chinese place names',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ginkgoty',
    url='https://github.com/Ginkgoty/chinese-address-generator/',
    author_email='int32@foxmail.com',
    packages=find_packages(),
    package_data={'chinese_address_generator': [
        'src/new_level3.json', 'src/new_level4.txt']},
    entry_points={
        'console_scripts': [
            'cnaddrgen=chinese_address_generator.cnaddrgen:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    license="MIT"
)
