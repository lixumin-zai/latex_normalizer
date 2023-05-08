import sys
import os
import setuptools


with open("README.md", "r", encoding='utf-8') as rfile:
    long_description = rfile.read()

with open(os.path.join("xizi_latex_normalizer", "__about__.py")) as rfile:
    v_dict = {}
    exec(rfile.read(), v_dict)
    version = v_dict['__version__']


setuptools.setup(
    name="xizi-latex-normalizer",
    version=version,
    author="Dongsheng Lin",
    description="Normalize latex formula",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/xizi_ai/dashboard/projects/xizhi-aied/xizi_latex_normalizer/code/",
    test_suite="nose.collector",
    tests_require=["nose"],
    packages=setuptools.find_packages(exclude=["test"]),
    package_dir={"xizi_latex_normalizer": "xizi_latex_normalizer"},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    project_urls={
        "Source": "https://gitee.com/xizi_ai/dashboard/projects/xizhi-aied/xizi_latex_normalizer/code/",
    },
)
