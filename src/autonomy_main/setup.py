from setuptools import find_packages, setup

package_name = 'autonomy_main'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ks',
    maintainer_email='krystian.soltys7@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            
            'publisher_node = autonomy_main.publisher_node:main',
            'listener_node = autonomy_main.listener_node:main',
        ],
    },
)
