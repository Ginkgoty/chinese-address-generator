from setuptools import setup, find_packages

setup(
    name='chinese_address_generator',
    version='0.1.0',
    description='Random generation of Chinese place names',
    author='uint8_t',
    url='https://github.com/uint8-t/chinese-address-generator',
    author_email='nmjbh@qq.com',
    packages=find_packages(),
    package_data={'chinese_address_generator': ['src/level3.json', 'src/level4.txt']},
    license="MIT"
)
