# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from setuptools import setup, find_packages

NAME = "mlx-api"
VERSION = "0.1.30-upload-catalog-from-url"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

# TODO: use/parse requirements.txt and include requirements.txt in MANIFEST.in
REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="MLX Server API",
    author_email="",
    url="https://github.com/machine-learning-exchange/mlx",
    keywords=["Swagger", "MLX API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={"": ["swagger/swagger.yaml"]},
    include_package_data=True,
    entry_points={"console_scripts": ["swagger_server=swagger_server.__main__:main"]},
    long_description="""\
    Machine Learning Exchange API
    """,
)
