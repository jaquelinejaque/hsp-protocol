from setuptools import setup, find_packages

setup(
    name="hsp-protocol",
    version="1.0.0",
    description="Official Python SDK for the Human Supervision Protocol",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="HSP Protocol Team",
    author_email="contact@hsp-protocol.org",
    url="https://github.com/jaquelinejaque/hsp-protocol",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "web3>=6.0.0",
        "eth-account>=0.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="hsp human-supervision ai-safety blockchain ethereum polygon eu-ai-act compliance",
    project_urls={
        "Documentation": "https://docs.hsp-protocol.org",
        "Source": "https://github.com/jaquelinejaque/hsp-protocol",
        "Tracker": "https://github.com/jaquelinejaque/hsp-protocol/issues",
    },
)
