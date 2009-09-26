import os, sys, site, subprocess, shutil, tempfile, urllib2, logging, string
import os.path
import zc.buildout
import setuptools.archive_util
import distutils.core

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)
        options['location'] = os.path.join(
                buildout['buildout']['parts-directory'], name)
        self.location = options['location']
        buildout['buildout'].setdefault('downloads-cache', 
                os.path.join(buildout['buildout']['directory'], 'downloads'))
        self.downloads = buildout['buildout']['downloads-cache']
        options['extra-path'] = os.path.join(self.location, 'lib', 
                'python%d.%d' % sys.version_info[:2],
                'site-packages')
        self.offline = buildout['buildout']['offline'].lower() == 'true'
        if not os.path.exists(self.downloads):
            os.mkdir(self.downloads)
        self.urls = options['urls'].splitlines()
        self.urls = map(string.strip, self.urls)
        self.urls = filter(len, self.urls)

    def install(self):
        if not os.path.exists(self.options['extra-path']):
            self.logger.debug("Creating %s" % (self.options['extra-path'],))
            os.makedirs(self.options['extra-path'])
        for url in self.urls:
            self.logger.info("Processing %s" % (url,))
            path = self._get_archive(url)
            tmp = tempfile.mkdtemp(prefix='buildout-')
            try:
                args = ['install', '--prefix=%s' % (self.location,)]
                self.logger.debug("Extracting into %s" % (tmp,))
                setuptools.archive_util.unpack_archive(path, tmp)
                # Let's find our setup.py
                search_paths = [os.path.join(tmp, 'setup.py'),]
                for d in os.listdir(tmp):
                    search_paths.append(os.path.join(tmp, d, 'setup.py'))
                setup_path = None
                for p in search_paths:
                    self.logger.debug("Checking %s" % (p,))
                    if os.path.exists(p):
                        setup_path = p
                if setup_path is None:
                    raise zc.buildout.UserError, \
                        "Could not find a setup.py in this package"
                self.logger.info("Installing into %s" % (self.location,))
                self._install_pkg(setup_path)
            finally:
                shutil.rmtree(tmp)
        return self.location

    def update(self):
        pass
    
    def _install_pkg(self, setup_path):
        old_dir = os.getcwd()
        os.chdir(os.path.dirname(setup_path))
        env = os.environ.copy()
        env['PYTHONPATH'] = env.get('PYTHONPATH', '') + ':' + \
                self.options['extra-path']
        try:
            cmd = [sys.executable, 'setup.py', 'install', 
                   '--prefix="%s"' % (self.location,)]
            subprocess.call(' '.join(cmd), env=env, shell=True)
        finally:
            os.chdir(old_dir)

    def _get_archive(self, url):
        fname = self._get_filename(url)
        path = os.path.join(self.downloads, fname)
        if os.path.exists(path):
            self.logger.debug(" -> already cached")
        else:
            if self.offline:
                raise zc.buildout.UserError, \
                    "Can not download archive because of offline-mode"
            self.logger.debug(" -> downloading")
            out = open(path, 'wb+')
            try:
                fp = urllib2.urlopen(url)
                for line in fp:
                    out.write(line)
            finally:
                out.close()
        return path


    def _get_filename(self, url):
        return os.path.basename(url)
