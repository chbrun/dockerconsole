class DockerManager():

    client = None

    def __init__(self, client):
        self.client = client

    def getContainersId(self):
        containers = self.containers(all = True)
        return map(lambda x: x['Id'], containers)

    def getContainersName(self):
        containers = self.containers(all = True)
        return map(lambda x: x['Names'][0], containers)

    def getContainerId(self, containerName):
        containers = self.containers(all = True)
        container = filter(lambda x: containerName in x['Names'], containers)
        return container[0]['Id']

    def getImagesId(self):
        images = self.client.images()
        return map(lambda x: x['Id'], images)

    def containers(self, all=False, detail=False):
        containers =  self.client.containers(all=all)
        if detail:
            for container in containers:
                detail = self.inspect(container['Id'])
                container['Links'] = []
                if detail['HostConfig']['Links'] is not None:
                    links = map(lambda x: x.split(':')[0],detail['HostConfig']['Links'])
                    [container['Links'].append(i) for i in links if not i in container['Links']]
            return containers
        else:
            return containers

    def images(self):
        return self.client.images()

    def start(self, containerId):
        detail = self.inspect(containerId)
        listLinks = []
        if detail['HostConfig']['Links'] is not None:
            print('Depends')
            links = map(lambda x: x.split(':')[0],detail['HostConfig']['Links'])
            [listLinks.append(i) for i in links if not i in listLinks]
            for link in listLinks:
                subContainerId = self.getContainerId(link)
                print('start : {:<30}'.format(subContainerId))
                self.client.start(subContainerId)
        return self.client.start(containerId)

    def stop(self, containerId):
        return self.client.stop(containerId)

    def search(self, text):
        return self.client.search(text)

    def inspect(self, containerId):
        return self.client.inspect_container(containerId)
