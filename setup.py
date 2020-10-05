from setuptools import setup, find_packages

setup(name="opt_media_planner",
      version="0.1",
      author="Rodrigo Teixeira",
      author_email="rodrigo_teixeira@id.uff.br",
      description="Simple Package to create an optimal media plan given a limit Budget and expected performance",
      long_description="",
      url="",
      keywords="'Linear Programming' LP 'Media Performance' 'Digital Marketing' Optimization",
      packages=find_packages(include=['pandas', 'numpy', 'pulp']),
      classifiers=["Programming Language : : Python :: 3", "Operating System : : OS Independent"],
      install_requires=['pandas', 'numpy', 'pulp'],
      python_requires=">=3"
      )
