#!/usr/bin/python3
import time
import sys
sys.path.append('/home/wjy/SComet/')
import exe

class Container:
    image = ''
    name = ''
    ip = ''
    passwd = ''
    task = ''
    running = None
    command = None
    def __init__(self, image_, name_, ip_, passwd_, net = False):
        self.image = image_
        self.name = name_
        self.ip = ip_
        self.passwd = passwd_
        print('Container %s@%s init' % (self.name, self.ip))
        exe.cmd_and_wait('%s docker stop %s' % (self.ssh_pre(), self.name))
        exe.cmd_and_wait('%s docker rm %s' % (self.ssh_pre(), self.name))
        if net:
            output, err = exe.cmd_and_wait('%s docker run -id -v /home/wjy/SComet:/home/wjy/SComet --net=scomet --privileged --name %s %s /bin/bash' % (self.ssh_pre(), self.name, self.image))
        else:
            output, err = exe.cmd_and_wait('%s docker run -id -v /home/wjy/SComet:/home/wjy/SComet --privileged --name %s %s /bin/bash' % (self.ssh_pre(), self.name, self.image))
        print('init result: ', output, err)
        if err:
            time.sleep(86400)
        # exe.cmd_and_wait('%s docker run -id --net=scomet --privileged --cpuset-cpus %s -m %d --name %s %s /bin/bash' % (self.ssh_pre(), cpu_, memory_, self.name, self.image))

    def ssh_pre(self):
        return 'sshpass -p \'%s\' ssh root@%s' % (self.passwd, self.ip)
    
    def __repr__(self):
        return self.name + '-' + self.task
        # return f'Container(name: {self.name}, container: {self.get_container()})'

    def remove(self):
        print('Container %s@%s remove' % (self.name, self.ip))
        exe.cmd_and_wait('%s "docker stop %s"' % (self.ssh_pre(), self.name))
        exe.cmd_and_wait('%s "docker rm %s"' % (self.ssh_pre(), self.name))

    def copy_file(self, src_, dest_):
        exe.cmd_and_wait('%s "docker cp %s:%s %s"' % (self.ssh_pre(), self.name, src_, dest_))

    def get_running_benchmark_set(self):
        return self.command.split('/')[-3]

    def get_running_task(self):
        return '.'.join(self.command.split('/')[-1].split('.')[0:-1])
    
    def get_id(self):
        output, err = exe.cmd_and_wait('%s "docker ps -a | grep %s"' % (self.ssh_pre(), self.name))
        if not output:
            print('get %s id error, err message' % self.name, err)
        return output[0].decode('utf-8').split()[0]

    def get_ip(self):
        output, err = exe.cmd_and_wait('%s "docker exec %s ifconfig"' % (self.ssh_pre(), self.name))
        for index in range(len(output)):
            ifconfig_log = output[index].decode('utf-8')
            if 'eth0' in ifconfig_log:
                ifconfig_log = output[index + 1].decode('utf-8')
                host = ifconfig_log.split()[1]
        return host

    def run_task(self, benchmark_set_, task_, arg_=''):
        self.task = task_
        self.run('sh /home/wjy/SComet/%s/script/%s.sh %s' % (benchmark_set_, task_, arg_))

    def run_accompany_task(self, benchmark_set_, task_, arg_=''):
        self.run('sh /home/wjy/SComet/%s/script/%s.sh %s' % (benchmark_set_, task_, arg_))

    def run(self, command_):
        self.command = command_
        print('Container %s@%s run %s' % (self.name, self.ip, self.command))
        # print('%s "docker exec %s sh -c \\\"%s\\\""' % (self.ssh_pre(), self.name, self.command))
        self.running = exe.cmd('%s "docker exec %s sh -c \\\"%s\\\""' % (self.ssh_pre(), self.name, self.command))




