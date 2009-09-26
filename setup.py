from setuptools import setup, find_packages

setup(
        name='zerokspot.recipe.distutils',
        author='Horst Gutmann',
        author_email='zerok@zerokspot.com',
        description="Recipe for zc.buildout that downloads one or multiple distutils-archives and installs them",
        version='0.1.2',
        packages=find_packages(),
        entry_points={'zc.buildout': 
            ['default = zerokspot.recipe.distutils:Recipe']},
        install_requires=['setuptools', 'zc.buildout'],
        namespace_packages=['zerokspot'],
        zip_safe=True,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Plugins',
            'Framework :: Buildout',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Installation/Setup',
            'License :: OSI Approved :: BSD License',
        ],
        url='http://github.com/zerok/zerokspot.recipe.distutils/'
        )
