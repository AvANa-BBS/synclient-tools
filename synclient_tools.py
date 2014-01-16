#!/usr/bin/env python
import yaml
import subprocess
import sys

def get_values():
    values = file('values.yaml').read()
    return yaml.load(values)

def get_conf():
    conf = file('conf.yaml').read()
    return yaml.load(conf)

def save_conf(conf):
    yaml_conf = yaml.dump(conf)
    file('conf.yaml', 'w').write(yaml_conf)

def get_cmd():
    cmd = ["synclient"]
    for key, value in get_conf().iteritems():
        cmd.append("%s=%s "%(key, value))
    return cmd

def apply_conf():
    subprocess.call(get_cmd())


if __name__ == '__main__':
    apply_conf()
