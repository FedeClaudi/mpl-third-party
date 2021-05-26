#!/usr/bin/env python

import os
from pathlib import Path
from yaml import safe_load
import requests

here = Path(__file__).parent.resolve()
cache_path = here.parent / 'doc/_static/cache'
print(cache_path)
badge = os.getenv('BADGE')

cache = {
    "stars": "https://img.shields.io/github/stars/{repo}.svg?style=social",
    "contributors": "https://img.shields.io/github/contributors/{repo}.svg?style=social&logo=github",
    "pypi_downloads": "https://img.shields.io/pypi/dm/{pypi_name}.svg?label=pypi",
    "license": "https://img.shields.io/pypi/l/{pypi_name}.svg?label",
}
url = cache.get(badge)
if url is None:
    raise ValueError((f'{badge} not in {", ".join(cache.keys())}, use env '
                      'var BADGE to set.'))

cache_path.mkdir(exist_ok=True)

with (here / 'tools.yml').open() as f:
    config = safe_load(f)

for section in config:
    print(f"Building cache for {section.get('name', '')}")
    for package in section['packages']:
        try:
            package['user'], package['name'] = package['repo'].split('/')
        except:
            raise Warning('Package.repo is not in correct format', package)
            continue
        package['pypi_name'] = package.get('pypi_name', package['name'])

        print(f"  * package: {package.get('pypi_name', '')}")
        rendered_url = url.format(repo=package['repo'], pypi_name=package['pypi_name'])
        r = requests.get(rendered_url)
        badge = cache_path / f"{package['name']}_{badge}_badge.svg"
        badge.write_bytes(r.content)
