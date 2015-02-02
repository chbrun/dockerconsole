# -*- coding: utf-8 -*-
import cmd2
from termcolor import colored
from dockerGateway.manager import DockerManager
from consolecfg import DOCKER_URI, USE_NAME
from docker import Client


class DockerUICli(cmd2.Cmd):

    intro = colored('Docker Console','grey')
    prompt = colored('docker > ', 'green')
    client = None
    containersList = []

    def __init__(self, client):
        self.client = client
        if USE_NAME:
            self.containersList = map(lambda x: str(x.split('/')[-1:]),self.client.getContainersName())
        else:
            self.containersList = self.client.getContainersId()
        cmd2.Cmd.__init__(self)

    def do_containers(self, line):
        print(colored('{:>10} {:>50} {:<30} {:>30}'.format('Id','Names', 'Status', 'Links'), 'white'))
        self.containersList=[]
        color='red'
        listContainers = self.client.containers(all=True, detail = True)
        for container in listContainers:
            if 'Exited' in container['Status']:
                color='red'
            else:
                color='green'

            containerName = (container['Names'][0]).split('/')[-1:]
            print(colored('{:>10} {:<30} {:<30} {:>30}'.format(container['Id'][:10],containerName[0], container['Status'], container['Links']), color))

            if USE_NAME:
                self.containersList.append(str(container['Names'][0].split('/')[-1:]))
            else:
                self.containersList.append(container['Id'])

    def do_start(self, line):
        self.client.start(line)
        self.do_containers(line)

    def complete_containerId(self, text):
        if not text:
            completions = self.containersList[:]
        else:
            completions = [ f
                           for f in self.containersList
                           if f.startswith(text)
            ]
        return completions

    def complete_start(self, text, line, begidx, endidx):
        return self.complete_containerId(text)

    def do_stop(self, line):
        self.client.stop(line)
        self.do_containers(line)

    def complete_stop(self, text, line, begidx, endidx):
        return self.complete_containerId(text)

    def do_inspect(self, line):
        infos =  self.client.inspect(line)
        for key, value in infos.iteritems():
            if isinstance(value, dict):
                print(colored('{:>20} : {:<50}'.format(key,''),'white'))
                for subkey, subvalue in value.iteritems():
                    print(colored('{:>20} {:<20} : {:<50}'.format('',subkey,subvalue),'white'))
            elif isinstance(value, list):
                print(colored('{:>20} : {:<50}'.format(key,''),'white'))
                for subvalue in value:
                    print(colored('{:>20} {:<50}'.format('',subvalue),'white'))
            else:
                print(colored('{:>20} : {:<50}'.format(key,value),'white'))

    def complete_inspect(self, text, line, begidx, endidx):
        return self.complete_containerId(text)

    def do_search(self, text):
        print(colored('{:<30} {:>5} {:>7} {:>7} {:>50}'.format('name','stars', 'official', 'trusted', 'description'), 'white'))
        results = self.client.search(text)
        for result in results:
            print(colored(u'{:<30} {:>5} {:>7} {:>7} {:<50}'.format(result['name'],result['star_count'], result['is_official'], result['is_trusted'], result['description'][:50]), 'white'))

    def do_images(self, text):
        print(colored('{:>10} {:<30}'.format('Id','Repo Tags'), 'white'))
        images= self.client.images()
        for image in images:
            print(colored('{:>10} {:<30}'.format(image['Id'][:10],image['RepoTags'][0]), 'images'))

    def do_showcompletion(self, line):
        print self.containersList


if __name__ == '__main__':
    console = DockerUICli(DockerManager(Client(DOCKER_URI)))
    console.cmdloop()
