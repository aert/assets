
try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('assets').version
except Exception, e:
    VERSION = 'unknown'
