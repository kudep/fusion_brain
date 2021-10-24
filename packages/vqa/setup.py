from setuptools import setup, find_packages


setup(
    name="vqa",
    version="0.1.a1",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    author="",
    author_email="",
    python_requires=">=3.6, <4",
    install_requires=["filelock==3.0.12", "wget==3.2"],
    packages=find_packages(where="."),
)
