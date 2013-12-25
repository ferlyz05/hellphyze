#!/usr/bin/env python2
import os
import telnetlib
from gi.repository import Gtk, Gdk

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

profile_file = os.getenv("HOME") + "/.hellphyze_profile"
encrypted_profile_file = os.getenv("HOME") + "/.hellphyze_profile.gpg"
class hellphyze:

    def on_show_password_toggled(self, widget):
        if widget.get_active():
            self.host_password.set_visibility(True)
        else:
            self.host_password.set_visibility(False)

    def on_load_profile_clicked(self, widget):
        if not os.path.isfile(encrypted_profile_file):
            dialog_no_profile = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Profile file does not exist!")
            dialog_no_profile.format_secondary_text("")
            dialog_no_profile.run()
            dialog_no_profile.destroy()
        else:
            # decrypt the encrypted profile - call gpg
            os.system('gpg "{0}"'.format(encrypted_profile_file))
            if not os.path.isfile(profile_file):
                dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
                    Gtk.ButtonsType.OK, "Wrong password, huh ?")
                dialog.format_secondary_text("")
                dialog.run()
                dialog.destroy()
                # now open and read it's content
            with open(profile_file) as read_ip_port_username:
                for i, line in enumerate(read_ip_port_username.readlines(), 0):
                    for char in line:
                        if char in ("\n"):
                            line = line.replace(char,'')
                    if i == 0:
                        self.host_ip.set_text(line)
                    if i == 1:
                        self.host_port.set_text(line)
                    if i == 2:
                        self.host_username.set_text(line)
                    if i == 3:
                        self.host_password.set_text(line)
            os.remove(profile_file)

    def on_save_profile_clicked(self, widget):
        if os.path.isfile(encrypted_profile_file):
            os.remove(encrypted_profile_file)
        profile = open(profile_file, "w")
        profile.write("{0}\n".format(self.host_ip.get_text()))
        profile.write("{0}\n".format(self.host_port.get_text()))
        profile.write("{0}\n".format(self.host_username.get_text()))
        profile.write("{0}\n".format(self.host_password.get_text()))
        profile.close()
        # encrypt the profile - call gpg
        os.system('gpg -o "{0}" --cipher-algo AES256 --symmetric "{1}"'.format(encrypted_profile_file, profile_file))
        os.remove(profile_file)
        if os.path.isfile(encrypted_profile_file):
            dialog_encrypted = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Profile saved & encrypted")
            dialog_encrypted.format_secondary_text("")
            dialog_encrypted.run()
            dialog_encrypted.destroy()

    # type many commands in the "custom commands" field, separated by a ,  do not add spaces !
    def on_send_clicked(self, widget):
        telnet = telnetlib.Telnet(self.host_ip.get_text(), self.host_port.get_text())
        telnet.read_until("Username : ")
        telnet.write(self.host_username.get_text() + "\r")
        telnet.read_until("Password : ")
        telnet.write(self.host_password.get_text() + "\r")
        line = self.custom_commands.get_text()
        for char in line:
            if char in (","):
                line2 = line.replace(char, '\r')
                telnet.write("{0}\r".format(line2))
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

        self.screen = Gdk.Screen.get_default()
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('data_hellphyze/style.css')
        self.priority = Gtk.STYLE_PROVIDER_PRIORITY_USER
        self.context = Gtk.StyleContext()
        self.context.add_provider_for_screen(self.screen, self.css_provider, self.priority)

if __name__ == '__main__':
    hellphyze()
    Gtk.main()