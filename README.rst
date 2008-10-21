==========================
zerokspot.recipe.distutils
==========================

This recipe offers a simple way to install dependencies that are only
available as distutils-archives::
    
    [buildout]
    parts = part

    [part]
    recipe = zerokspot.recipe.distutils
    urls = 
        http://domain.com/file.tar.gz

This will install the package into ``${buildout:parts-directory}/part/`` and
make its library components available via ``${part:extra-path}``.

Options
-------

urls
    A list of packages (one per line) that should be installed into
    ``${buildout:parts-directory}/<partname>``.

Additionally provided variables
-------------------------------

location
    Points to the prefix of the installed package

extra-path
    Points to the site-package-directory within the prefix


Disclaimer
----------

Function-wise this recipe is inspired by Kevin Teague's
`collective.recipe.distutils`_, but solves some aspects a little bit different.
For instance, this recipe uses setup.py's ``--prefix``-argument in order to
also support the installation of packages that have a script-component. It
also distinguishes between ``${part:location}`` and ``${part:extra-path}`` 
with the first representing the prefix-directory while the latter pointing 
to the respective "site-packages"-directory.

.. _`collective.recipe.distutils`: http://pypi.python.org/pypi/collective.recipe.distutils/0.1
