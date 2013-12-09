#!/usr/bin/python2
import telnetlib
from gi.repository import Gtk

class allow_mac(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "Allow MAC", None,
            Gtk.DialogFlags.MODAL, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        label = Gtk.Label('Allow MAC, example 11:22:33:44:55:66')
        box.add(label)
        self.entry = Gtk.Entry()
        box.add(self.entry)
        self.show_all()

class deny_mac(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "Deny MAC", None,
            Gtk.DialogFlags.MODAL, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))
        box = self.get_content_area()
        label = Gtk.Label('Deny MAC, example 11:22:33:44:55:66')
        box.add(label)
        self.entry = Gtk.Entry()
        box.add(self.entry)
        self.show_all()

class hellphyze:

    def on_send_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        telnet.write("{0}\r".format(self.custom_commands.get_text()))
        telnet.write("exit\r")
        self.textbuffer.set_text("{0}".format(telnet.read_all()))

    def on_network_up_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        telnet.write("ppp ifattach intf=pppInternet\r")
        telnet.write("ip ifattach intf=ipInternet\r")
        telnet.write("saveall\r")
        telnet.write("exit\r")
        self.textbuffer.set_text("{0}".format(telnet.read_all()))

    def on_network_down_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        telnet.write("ppp ifdetach intf=pppInternet\r")
        telnet.write("ip ifdetach intf=ipInternet\r")
        telnet.write("saveall\r")
        telnet.write("exit\r")
        self.textbuffer.set_text("{0}".format(telnet.read_all()))

    def on_allow_2_mac_clicked(self, widget):
        dialog = allow_mac()
        response = dialog.run()
        entered_text = dialog.entry.get_text()
        if response == Gtk.ResponseType.OK:
            telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
            telnet.read_until("Username : ")
            telnet.write(self.host_username.get_text() + "\r")
            telnet.read_until("Password : ")
            telnet.write(self.host_password.get_text() + "\r")
            telnet.write('wireless macacl modify ssid_id=0 hwaddr="{0}" permission=allow\r'.format(entered_text))
            telnet.write("exit\r")
            self.textbuffer.set_text("{0}".format(telnet.read_all()))
        dialog.destroy()

    def on_deny_2_mac_clicked(self, widget):
        dialog = deny_mac()
        response = dialog.run()
        entered_text = dialog.entry.get_text()
        if response == Gtk.ResponseType.OK:
            telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
            telnet.read_until("Username : ")
            telnet.write(self.host_username.get_text() + "\r")
            telnet.read_until("Password : ")
            telnet.write(self.host_password.get_text() + "\r")
            telnet.write('wireless macacl modify ssid_id=0 hwaddr="{0}" permission=deny\r'.format(entered_text))
            telnet.write("saveall\r")
            telnet.write("exit\r")
            self.textbuffer.set_text("{0}".format(telnet.read_all()))
        dialog.destroy()

    def on_disable_reset_button_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        telnet.write("system config resetbutton=disabled\r")
        telnet.write("system qual led value=alloff\r")
        telnet.write("service system modify name=CWMP-S state=disabled\r")
        telnet.write("service system modify name=CWMP-C state=disabled\r")
        telnet.write("saveall\r")
        telnet.write("exit\r")
        self.textbuffer.set_text("{0}".format(telnet.read_all()))

    def on_list_devices_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        telnet.write("hostmgr list\r")
        telnet.write("exit\r")
        self.textbuffer.set_text("{0}".format(telnet.read_all()))

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('data_hellphyze/hellphyze.ui')
        self.builder.connect_signals(self)

        self.custom_commands = self.builder.get_object('custom_commands')
        self.host_ip = self.builder.get_object('host_ip')
        self.host_port = self.builder.get_object('host_port')
        self.host_username = self.builder.get_object('host_username')
        self.host_password = self.builder.get_object('host_password')
        self.textview = self.builder.get_object('textview1')
        self.textbuffer = self.textview.get_buffer()

        self.window = self.builder.get_object("window1")
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()

if __name__ == '__main__':
    hellphyze()
    Gtk.main()