import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="saya",
    version="0.4.0",
    author="Ethosa",
    author_email="social.ethosa@gmail.com",
    description="The framework for vk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosa/saya",
    packages=setuptools.find_packages(),
    license="LGPLv3",
    keywords="vk api framework python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Github": "https://github.com/Ethosa/saya",
        "Documentation": "https://github.com/Ethosa/saya/blob/master/README.md",
    },
    python_requires=">=3",
    install_requires=[
        "requests",
        "regex",
        "beautifulsoup4",
        "retranslator",
        "websocket-client",
        "aiohttp",
    ]
)
