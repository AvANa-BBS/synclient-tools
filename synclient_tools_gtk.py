#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
from synclient_tools import save_conf, get_conf, get_values, apply_conf


class MainWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_border_width(10)

        self.touchpadClicks = TouchpadClicks()
        self.twoFingerScroll = TwoFingerScroll()

        box = gtk.VBox(False, 0)
        box.add(self.twoFingerScroll)
        box.add(self.touchpadClicks)
        self.add(box)
        self.connect("destroy", self.quit)

        saveButton = gtk.Button('Save')
        saveButton.connect('clicked', self.save)
        box.add(saveButton)

    def quit(self, widget, data=None):
        gtk.main_quit()

    def save(self, widget, data=None):
        conf = {}
        for key, val in self.touchpadClicks.get_new_config().iteritems():
            conf[key] = val
        for key, val in self.twoFingerScroll.get_new_config().iteritems():
            conf[key] = val
        save_conf(conf)
        apply_conf()


class Tools:

    values = get_values()
    conf = get_conf()

    @staticmethod
    def create_combo(data_key):
        combo = gtk.combo_box_new_text()
        i = 0
        print Tools.conf
        for key, value in Tools.values[data_key].iteritems():
            combo.append_text("%s"%value)
            if Tools.conf[data_key] == key:
                combo.set_active(i)
            i+=1
        return combo

    @staticmethod
    def get_key(values_key, searched_value):
        values_dict = Tools.values[values_key]
        for key, value in values_dict.iteritems():
            if str(value) == str(searched_value):
                return key
        return None


class TwoFingerScroll(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self, False, 0)
        frame = gtk.Frame(label='Two finger scrolling')
        table = gtk.Table(2, 2, True)
        self.add(frame)
        frame.add(table)

        self.horizScrollLabel = gtk.Label('Horizontal scroll')
        self.horizScroll = Tools.create_combo('HorizTwoFingerScroll')
        table.attach(self.horizScrollLabel, 0, 1, 0, 1)
        table.attach(self.horizScroll, 1, 2, 0, 1)

        self.vertScrollLabel = gtk.Label('Vertical scroll')
        self.vertScroll = Tools.create_combo('VertTwoFingerScroll')
        table.attach(self.vertScrollLabel, 0, 1, 1, 2)
        table.attach(self.vertScroll, 1, 2, 1, 2)

    def get_new_config(self):
        horizScroll = Tools.get_key('HorizTwoFingerScroll', self.horizScroll.get_active_text())
        vertScroll = Tools.get_key('VertTwoFingerScroll', self.vertScroll.get_active_text())
        return {'HorizTwoFingerScroll':horizScroll, 'VertTwoFingerScroll':vertScroll}

class TouchpadClicks(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self, False, 0)
        self.values = get_values()
        self.conf = get_conf()
      
        frame = gtk.Frame(label='Touchpad clicks')
        table = gtk.Table(3, 2, True)
        self.add(frame)
        frame.add(table)

        self.tapButton1Label = gtk.Label('One finger click')
        self.tapButton1 = Tools.create_combo('TapButton1')
        table.attach(self.tapButton1Label, 0, 1, 0, 1)
        table.attach(self.tapButton1, 1, 2, 0, 1)

        self.tapButton2Label = gtk.Label('Two fingers click')
        self.tapButton2 = Tools.create_combo('TapButton2')
        table.attach(self.tapButton2Label, 0, 1, 1, 2)
        table.attach(self.tapButton2, 1, 2, 1, 2)

        self.tapButton3Label = gtk.Label('Three fingers click')
        self.tapButton3 = Tools.create_combo('TapButton3')
        table.attach(self.tapButton3Label, 0, 1, 2, 3)
        table.attach(self.tapButton3, 1, 2, 2, 3)

    def get_new_config(self):
        tapButton1 = Tools.get_key('TapButton1', self.tapButton1.get_active_text())
        tapButton2 = Tools.get_key('TapButton2', self.tapButton2.get_active_text())
        tapButton3 = Tools.get_key('TapButton3', self.tapButton3.get_active_text())
        return {'TapButton1':tapButton1, 'TapButton2':tapButton2, 'TapButton3':tapButton3}


if __name__ == '__main__':
    window = MainWindow()
    window.show_all()
    gtk.main()

