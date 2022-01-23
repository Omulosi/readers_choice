import os
import re
from urllib.parse import urlsplit
import json
import zlib
from datetime import datetime, timedelta

class DiskCache:

    def __init__(self, cache_dir='cache', max_len=255, compress=True,
            encoding='utf-8', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.max_len = max_len
        self.compress = compress
        self.encoding = encoding
        # self.expires = expires

    def url_to_path(self, url):
        """
        Return file system path string for given URL
        """
        components = urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub(r'[^/0-9a-zA-Z\-.,;_]', '_', filename)
        # restrict max num of characters
        filename = '/'.join(seg[:self.max_len] for seg in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def __getitem__(self, url):
        """
        Load data from disk for given url
        """
        path = self.url_to_path(url)
        if path.endswith('index'):
            path += '/'
            path = self.url_to_path(path)
        if os.path.exists(path):
            mode = ('rb' if self.compress else 'r')
            with open(path, mode) as fp:
                if self.compress:
                    data = zlib.decompress(fp.read()).decode(self.encoding)
                    data = json.loads(data)
                else:
                    data = json.load(fp)
            return data
        else:
            # URL not yet cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """
        Save data to disk for given url
        """
        path = self.url_to_path(url)
        if path.endswith('index'):
            path += '/'
            path = self.url_to_path(path)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        mode = ('wb' if self.compress else 'w')
        with open(path, mode) as fp:
            if self.compress:
                data = bytes(json.dumps(result), self.encoding)
                fp.write(zlib.compress(data))
            else:
                json.dump(result, fp)