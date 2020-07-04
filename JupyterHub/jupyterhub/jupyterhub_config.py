# JupyterHub configuration

import os
from dockerspawner import SwarmSpawner

## Generic
c.Spawner.default_url = '/lab'

# NativeAuthenticator https://github.com/jupyterhub/nativeauthenticator
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

# Set admin user
c.Authenticator.admin_users = {'fagundo'}
c.DummyAuthenticator.password = 'password'

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']

c.JupyterHub.hub_ip = os.environ['HUB_IP']
c.JupyterHub.port = 80

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
