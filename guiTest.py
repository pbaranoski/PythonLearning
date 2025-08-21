#from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ourwindow(Gtk.Window):
  
    def __init__(self):
        Gtk.Window.__init__(self, title="Demonstration\
        of PyObject GUI Application Creation")
        Gtk.Window.set_default_size(self, 400,325)
        Gtk.Window.set_position(self, Gtk.WindowPosition.CENTER)
  
        button1 = Gtk.Button("GeeksforGeeks")
        button1.connect("clicked", self.whenbutton1_clicked)
  
        self.add(button1)
          
    def whenbutton1_clicked(self, button):
      print("GeeksforGeeks")
  
window = ourwindow()        
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()


"""
[BZH3@dd-az2-infa-dei-node1-217113 ~]$ python guiTest.py
/usr/lib64/python2.7/site-packages/gi/overrides/Gtk.py:50: RuntimeWarning: You have imported the Gtk 2.0 module.  Because Gtk 2.0 was not designed for use with introspection some of the interfaces and API will fail.  As such this is not supported by the pygobject development team and we encourage you to port your app to Gtk 3 or greater. PyGTK is the recomended python module to use with Gtk 2.0
  warnings.warn(warn_msg, RuntimeWarning)
guiTest.py:1: PyGIWarning: Gtk was imported without specifying a version first. Use gi.require_version('Gtk', '2.0') before import to ensure that the right version gets loaded.
  from gi.repository import Gtk
/usr/lib64/python2.7/site-packages/gi/overrides/__init__.py:326: Warning: invalid (NULL) pointer instance
  return super_init_func(self, **new_kwargs)
/usr/lib64/python2.7/site-packages/gi/overrides/__init__.py:326: Warning: g_signal_connect_data: assertion 'G_TYPE_CHECK_INSTANCE (instance)' failed
  return super_init_func(self, **new_kwargs)

"""
