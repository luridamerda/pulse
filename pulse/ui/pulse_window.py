import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class PulseWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Pulse')

        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

        adw_toast_overlay = Adw.ToastOverlay.new()
        self.set_content(content=adw_toast_overlay)

        adw_toolbar_view = Adw.ToolbarView.new()
        adw_toast_overlay.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        open_button = Gtk.Button.new()
        open_button.connect('clicked', self.on_open_button_clicked)
        open_button_content = Adw.ButtonContent.new()
        open_button_content.set_icon_name(icon_name='document-open-symbolic')
        open_button_content.set_label(label='Open')
        open_button.set_child(child=open_button_content)
        adw_header_bar.pack_start(child=open_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)
        
    def on_open_button_clicked(self, button):
        print('Open button clicked.')
