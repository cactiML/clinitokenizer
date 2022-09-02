import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires=[
    "setuptools>=42",
    "torch",
    "tqdm>=4.62.3",
    "simpletransformers==0.63.6",
    "transformers==4.14.1",
    "spacy==3.1.3",
]

setuptools.setup(
    name="clinitokenizer",
    version="0.0.5",
    author="Sam Rawal",
    author_email="scrawal2@illinois.edu",
    description="Sentence tokenizer for text from clinical notes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clinisift/clinitokenizer",
    project_urls={
        "Bug Tracker": "https://github.com/clinisift/clinitokenizer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=install_requires,
)
