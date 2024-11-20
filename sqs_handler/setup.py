from setuptools import setup, find_packages

setup(
    name="sqs-handler",
    version="0.1.0",
    description="A simple SQS integration handler for Python applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shanmukh Tadisetti",
    author_email="shanmukhtadisetti9@gmail.com",
    url="https://github.com/yourusername/sqs-handler",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
