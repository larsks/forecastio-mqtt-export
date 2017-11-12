from setuptools import setup, find_packages

setup(
    name='forecastio-mqtt',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='https://github.com/larsks/forecastio-mqtt',
    packages=find_packages(),
    install_requires=[
        'requests',
        'paho_mqtt',
    ],
    entry_points={
        'console_scripts': [
            'forecastio-export-mqtt = forecastio_mqtt.main:main',
        ],
    }
)
