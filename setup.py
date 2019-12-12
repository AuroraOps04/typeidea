from setuptools import setup, find_packages

setup(
    name='typeidea',
    version='0.1',
    description='Blog System base on Django',
    author='rui tao',
    author_eamil='5239604@qq.com',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'':'typeidea'},
    package_data={'':[
        'themes/*/*/*/*',
    ]},
    install_requires=[
        'django~=1.11',
    ],
    extras_require={
        'ipython': ['ipython==6.2.1']
    },
    scripts=[
        'typeidea/mange.py'
    ],
    entry_points={
            'console_scripts': [
                'typeidea_mange = mange:main',
            ],
    },


        )
