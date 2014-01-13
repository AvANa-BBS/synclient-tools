#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
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

def apply_config():
    subprocess.call(get_cmd())


class MainWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_border_width(10)
        box = gtk.VBox(False, 0)
        box.add(Form())
        self.add(box)
        self.connect("destroy", self.quit)

    def quit(self, widget, data=None):
        gtk.main_quit()

class Form(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self, False, 0)
        self.values = get_values()
        self.conf = get_conf()
       
        table = gtk.Table(4, 2, True)
        self.add(table)

        self.tapButton1Label = gtk.Label('One finger click')
        self.tapButton1 = self.create_combo('TapButton1')
        table.attach(self.tapButton1Label, 0, 1, 0, 1)
        table.attach(self.tapButton1, 1, 2, 0, 1)

        self.tapButton2Label = gtk.Label('Two fingers click')
        self.tapButton2 = self.create_combo('TapButton2')
        table.attach(self.tapButton2Label, 0, 1, 1, 2)
        table.attach(self.tapButton2, 1, 2, 1, 2)

        self.tapButton3Label = gtk.Label('Three fingers click')
        self.tapButton3 = self.create_combo('TapButton3')
        table.attach(self.tapButton3Label, 0, 1, 2, 3)
        table.attach(self.tapButton3, 1, 2, 2, 3)

        saveButton = gtk.Button('Save')
        saveButton.connect('clicked', self.save)
        table.attach(saveButton, 0, 1, 3, 4)

    def create_combo(self, data_key):
        combo = gtk.combo_box_new_text()
        i = 0
        for key, value in self.values[data_key].iteritems():
            combo.append_text("%s"%value)
            if self.conf[data_key] == key:
                combo.set_active(i)
            i+=1
        return combo

    def save(self, widget, data=None):
        conf = self.get_new_config()
        save_conf(conf)
        apply_config()

    def get_new_config(self):
        tapButton1 = self.get_key(self.values['TapButton1'], self.tapButton1.get_active_text())
        tapButton2 = self.get_key(self.values['TapButton2'], self.tapButton2.get_active_text())
        tapButton3 = self.get_key(self.values['TapButton3'], self.tapButton3.get_active_text())
        return {'TapButton1':tapButton1, 'TapButton2':tapButton2, 'TapButton3':tapButton3}

    def get_key(self, dict, searched_value):
        for key, value in dict.iteritems():
            if str(value) == str(searched_value):
                return key
        return None

if __name__ == '__main__':
    USAGE = """%s CMD

CMD:
  gtk - Run gtk UI
  run - Apply stored conf""" % sys.argv[0]

    if len(sys.argv) != 2:
        print USAGE
    else:
        cmd = sys.argv[1]
        if cmd == 'gtk':
            window = MainWindow()
            window.show_all()
            gtk.main()
        elif cmd == 'run':
            apply_config()
        else:
            print USAGE
