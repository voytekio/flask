from setuptools import setup

setup(name='flask-vc-project',
        version = '0.1.1',
        packages=['flaskvc'],
        description='flask vc project',
        include_package_data=True,
        install_requires=[
            'Flask',
            'pyvmomi',
            'requests'
        ],
        license = 'BSD',
        url = 'http://github.com/vkrudysz/oneofthesedays.html',
        author = 'Voytek Krudysz',
        author_email = 'voytek@voytek.io',
        entry_points={
            'console_scripts': [
                'flaskvc=flaskproject:main',
            ]
        }
)
