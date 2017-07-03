#   This is a component of LinuxCNC
#   Copyright 2013 Chris Morley <chrisinnanaimo@hotmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#############################################################################
# This is a gscreen skin customized for a Bridgeport Interact Mill that used a
# Heidenhain TNC 151a controller.
# Chris Brady	Oct 2015
#
import hal
import gtk
import gladevcp.makepins # needed for the dialog's calulator widget
import pango
import hal_glib

_MAN = 0;_MDI = 1;_AUTO = 2;_LOCKTOGGLE = 1

# This is a handler file for using Gscreen's infrastructure
# to load a completely custom glade screen
# The only things that really matters is that it's saved as a GTK builder project,
# the toplevel window is caller window1 (The default name) and you connect a destroy
# window signal else you can't close down linuxcnc 
class HandlerClass:

    # This will be pretty standard to gain access to everything
    # emc is for control and status of linuxcnc
    # data is important data from gscreen and linuxcnc
    # widgets is all the widgets from the glade files
    # gscreen is for access to gscreens methods
    def __init__(self, halcomp,builder,useropts,gscreen):
        self.emc = gscreen.emc
        self.data = gscreen.data
        self.widgets = gscreen.widgets
        self.gscreen = gscreen

# Hide all menus at the bottom of the default gscreen page
	self.widgets.mode0.hide()
	self.widgets.mode1.hide()
	self.widgets.mode2.hide()
	self.widgets.mode3.hide()
	self.widgets.mode4.hide()
        self.widgets.button_mode.hide()
	self.widgets.diameter_mode.hide()
	self.widgets.aux_coolant_m7.hide()
	self.widgets.aux_coolant_m8.hide()
	self.widgets.show_dtg.hide()
	self.widgets.diameter_mode.hide()
	self.widgets.button_run.hide()

# Initialize variables
	self.data.lathe_mode=False
	self.data.graphic_ypos=0
	self.data.graphic_xpos=0
	self.data.view=0
	self.data.homed=0
	self.data.jog_rates=[30,50,80,120]
	self.data.jog_incrs=[0.0002,0.001,0.01,0.1]
	self.data.jog_rate_idx=2
	self.data.notebook_page=0

	self.widgets.jog_r1.set_label("%5.4f"% self.data.jog_incrs[0])
	self.widgets.jog_r2.set_label("%4.3f"% self.data.jog_incrs[1])
	self.widgets.jog_r3.set_label("%3.2f"% self.data.jog_incrs[2])
	self.widgets.jog_r4.set_label("%2.1f"% self.data.jog_incrs[3])
        self.widgets.spindle_gear.set_range(1250.0, 2500.0)
        self.widgets.spindle_gear.set_increments(1250.0, 1250.0)
        self.widgets.accel_sel.set_range(3.0, 10.0)
        self.widgets.accel_sel.set_increments(0.5, 0.5)
        self.widgets.button_mode.hide()
        self.widgets.button_home_all.hide()
        self.widgets.button_auto_stop.hide()
        self.widgets.led_mist.set_active(False)

    # every 100 milli seconds this gets called
    # we add calls to the regular functions for the widgets we are using.
    # and add any extra calls/code
    def periodic(self):
        self.gscreen.update_dro()
        self.gscreen.update_active_gcodes()
        self.gscreen.update_active_mcodes()
        self.gscreen.update_feed_speed_label()
        self.gscreen.update_tool_label()
        self.update_leds()
        self.gscreen.update_machine_on_led()
        self.gscreen.update_jog_rate_label()
        self.gscreen.update_mode_label()
        self.gscreen.update_units_button_label()
	self.update_override_label()
	self.update_spindle()

    def	update_spindle(self):
	# Actual speed from hal
	# Limit speed representation to 1 decimal point
	speed = int(self.gscreen.halcomp["spindle-spd-disp"]*10)/10
        self.widgets.meter_spindle_speed.set_property("value", speed)

    # Initialize hal pins that we need access to
    def initialize_pins(self):
        self.gscreen.init_spindle_pins()
        self.gscreen.init_coolant_pins()
        self.gscreen.init_jog_pins()
        self.gscreen.init_override_pins()
        self.gscreen.init_control_pins()
	self.gscreen.halcomp.newpin("spindle-spd-disp", hal.HAL_FLOAT, hal.HAL_IN)
	self.gscreen.halcomp.newpin("jog-spd-out", hal.HAL_FLOAT, hal.HAL_OUT)
	self.data['ext-estop'] = hal_glib.GPin(self.gscreen.halcomp.newpin('ext-estop', hal.HAL_BIT, hal.HAL_IN))
        self.data['ext-estop'].connect('value-changed', self.on_estop_in)
	self.data['enc-fault-x'] = hal_glib.GPin(self.gscreen.halcomp.newpin('enc-fault-x', hal.HAL_BIT, hal.HAL_IN))
        self.data['enc-fault-x'].connect('value-changed', self.on_x_enc_fault)
	self.data['enc-fault-y'] = hal_glib.GPin(self.gscreen.halcomp.newpin('enc-fault-y', hal.HAL_BIT, hal.HAL_IN))
        self.data['enc-fault-y'].connect('value-changed', self.on_y_enc_fault)
	self.data['enc-fault-x'] = hal_glib.GPin(self.gscreen.halcomp.newpin('enc-fault-z', hal.HAL_BIT, hal.HAL_IN))
        self.data['enc-fault-x'].connect('value-changed', self.on_z_enc_fault)
	self.gscreen.halcomp.newpin("spindle-gear-sel", hal.HAL_BIT, hal.HAL_OUT)

        data = self.gscreen.prefs.getpref('spindle_gear', 2500.0, float)
        self.data.spindle_gear = data
        self.widgets.spindle_gear.set_value(data)
        if data == 2500:
            self.gscreen.halcomp["spindle-gear-sel"] = True
        elif data == 1250:
            self.gscreen.halcomp["spindle-gear-sel"] = False
        self.data.max_accel=self.gscreen.prefs.getpref('accel_sel', 5.6, float)
        self.widgets.accel_sel.set_value(self.data.max_accel)

    def on_emc_off(self,*args):
        self.widgets.button_clear.show()
        self.widgets.button_mode.hide()
        self.widgets.button_home_all.hide()
	# Force mode to manual
        a,b,c = self.data.mode_order
	if self.data.mode_order[0] == self.data._AUTO:
            self.data.mode_order = b,c,a
	elif self.data.mode_order[0] == self.data._MDI:
            self.data.mode_order = c,a,b
        label = self.data.mode_labels
        self.widgets.button_mode.set_label(label[self.data.mode_order[0]])
        self.mode_changed(self.data.mode_order[0])
	
    def on_btn_clear(self,widget):
	if self.gscreen.halcomp["ext-estop"] == False:
	    self.emc.estop_reset(1)
	    self.emc.machine_on(1)
            self.widgets.button_clear.hide()
            self.widgets.button_home_all.show()

    def on_estop_in(self,widget):
	self.widgets.mode0.hide()
	if self.gscreen.halcomp["ext-estop"] == True:
	    self.emc.estop_reset(1)
	    self.emc.machine_on(1)
	else:
	    self.emc.machine_off(1)
	    self.emc.estop(1)

    def on_hal_status_interp_idle(self,widget):
        print "Idle"
        self.gscreen.sensitize_widgets(self.data.sensitive_run_idle,True)
        state = self.data.all_homed
        self.gscreen.sensitize_widgets(self.data.sensitive_all_homed,state)
        mode = self.emc.get_mode()
        print "Mode",mode,self.data.mode_order[0]
        self.widgets.button_reload.set_sensitive(1)
        if self.data.mode_order[0] == self.data._MAN and not mode == 1:
            if self.data.notebook_page <> 5:
                print "Set to manual"
                self.emc.set_manual_mode()

    def update_leds(self):
	if self.data.estopped:
            self.widgets.led_estop.set_active(False)
	else:
            self.widgets.led_estop.set_active(True)
        state = self.widgets.button_option_stop.get_active()
        self.widgets.led_option_stop.set_active(state)
        state = self.widgets.button_block_delete.get_active()
        self.widgets.led_block_delete.set_active(state)

    def on_x_enc_fault(self,hal_object):
	print"X Encoder Fault"
	self.gscreen.add_alarm_entry(_("X Axis Encoder Error"))
	
    def on_y_enc_fault(self,hal_object):
	print"Y Encoder Fault"
	self.gscreen.add_alarm_entry(_("Y Axis Encoder Error"))
	
    def on_z_enc_fault(self,hal_object):
	print"Z Encoder Fault"
	self.gscreen.add_alarm_entry(_("Z Axis Encoder Error"))

    def homing(self,*args):
	self.mode_changed(self.data._MAN)
        self.widgets.button_mode.hide()
        self.widgets.button_home_all.show()
        self.widgets.button_move_to.set_sensitive(0)

    def on_hal_status_all_homed(self,widget):
	self.gscreen.on_hal_status_all_homed(1)
	self.data.homed=1
        self.widgets.button_home_all.hide()
        self.widgets.button_mode.show()
	self.widgets.jog_r3.set_active(1)
	self.on_jog_rate(self.widgets.jog_r3)
	self.gscreen.sensitize_widgets(self.data.sensitive_all_homed,1)
        self.widgets.button_move_to.set_sensitive(1)

    def on_interp_run(self,*args):
	self.gscreen.sensitize_widgets(self.data.sensitive_run_idle,False)
	self.widgets.button_reload.set_sensitive(0)

    def on_jog_rate(self,widget):
	if widget == self.widgets.jog_r1:
	    self.data.jog_rate_idx=0
	    speed = self.data.jog_rates[0]
	    self.widgets.jog_r2.set_active(0)
	    self.widgets.jog_r3.set_active(0)
	    self.widgets.jog_r4.set_active(0)
	    self.gscreen.halcomp["jog-spd-out"] = speed
	elif widget == self.widgets.jog_r2:
	    self.data.jog_rate_idx=1
	    speed = self.data.jog_rates[1]
	    self.widgets.jog_r1.set_active(0)
	    self.widgets.jog_r3.set_active(0)
	    self.widgets.jog_r4.set_active(0)
	    self.gscreen.halcomp["jog-spd-out"] = speed
	elif widget == self.widgets.jog_r3:
	    self.data.jog_rate_idx=2
	    speed = self.data.jog_rates[2]
	    self.widgets.jog_r1.set_active(0)
	    self.widgets.jog_r2.set_active(0)
	    self.widgets.jog_r4.set_active(0)
	    self.gscreen.halcomp["jog-spd-out"] = speed
	elif widget == self.widgets.jog_r4:
	    self.data.jog_rate_idx=3
	    speed = self.data.jog_rates[3]
	    self.widgets.jog_r1.set_active(0)
	    self.widgets.jog_r2.set_active(0)
	    self.widgets.jog_r3.set_active(0)
	    self.gscreen.halcomp["jog-spd-out"] = speed

    def jog_point1(self,widget):
        if self.data.mode_order[0] == self.data._MAN: # if in manual mode
                print "jog point1"
                if widget == self.widgets.jog_plus:
                    self.do_jog(True,True)
                else:
                    self.do_jog(False,True)

    def do_jog(self,direction,action):
        # if manual mode, if jogging
        # if only one axis button pressed
        # jog positive  at selected rate
        if self.data.mode_order[0] == self.data._MAN:
            if len(self.data.active_axis_buttons) > 1:
                print self.data.active_axis_buttons
            elif self.data.active_axis_buttons[0][0] == None:
                self.gscreen.homed_status_message = self.widgets.statusbar1.push(1,"No axis selected to jog")
            else:
                if not self.data.active_axis_buttons[0][0] == "s":
                    if not action: cmd = 0
                    elif direction: cmd = 1
                    else: cmd = -1
                    self.emc.jogging(1)
                    jogincr = self.data.jog_incrs[self.data.jog_rate_idx]
                    self.emc.incremental_jog(self.data.active_axis_buttons[0][1],cmd,jogincr)

    def on_mode_clicked(self,widget,event):
        # only change machine modes on click
        if event.type == gtk.gdk.BUTTON_PRESS:
            a,b,c = self.data.mode_order
            self.data.mode_order = b,c,a
            label = self.data.mode_labels
            self.widgets.button_mode.set_label(label[self.data.mode_order[0]])
            self.mode_changed(self.data.mode_order[0])

    def mode_changed(self,mode):
	print "Mode Change", mode
        if mode == self.data._MAN:
            self.widgets.notebook_mode.hide()
            self.widgets.hal_mdihistory.hide()
            self.widgets.dro_frame.show()
            self.widgets.vmode0.show()
            self.widgets.button_zero_origin.show()
            self.widgets.button_offset_origin.show()
            self.widgets.button_move_to.show()
            self.widgets.Handwheel.show()
            self.widgets.button_auto_stop.hide()
            self.widgets.vmode1.hide()
	    self.widgets.button_run.set_active(0)
	    self.widgets.button_jog_mode.set_active(1)
	    self.widgets.button_view.emit("clicked")
        elif mode == self.data._MDI:
            if self.data.plot_hidden:
                self.toggle_offset_view()
            self.emc.set_mdi_mode()
            self.widgets.hal_mdihistory.show()
            self.widgets.vmode0.show()
            self.widgets.button_zero_origin.hide()
            self.widgets.button_offset_origin.hide()
            self.widgets.button_move_to.hide()
            self.widgets.Handwheel.hide()
            self.widgets.button_auto_stop.show()
            self.widgets.vmode1.hide()
	    self.widgets.button_run.set_active(0)
            self.widgets.notebook_mode.hide()
	    self.widgets.button_jog_mode.set_active(0)
        elif mode == self.data._AUTO:
            self.widgets.vmode0.hide()
            self.widgets.vmode1.show()
	    self.widgets.button_run.set_active(0)
            if self.data.full_graphics:
                self.widgets.notebook_mode.hide()
            else:
                self.widgets.notebook_mode.show()
            self.widgets.hal_mdihistory.hide()
	    self.widgets.button_jog_mode.set_active(0)

    def on_button_flood(self,widget):
	if self.widgets.button_flood.get_active():
                self.gscreen.halcomp["aux-coolant-m8-out"] = True
                self.widgets.led_mist.set_active(True)
	else:
		self.gscreen.halcomp["aux-coolant-m8-out"] = False
                self.widgets.led_mist.set_active(False)

    def on_ign_toolc_pressed(self, widget):
	data = widget.get_active()

    def on_tool_change(self,widget):
	if self.widgets.ignore_toolchange.get_active() == True:
	    self.gscreen.halcomp["tool-changed"] = True
	else:
            h = self.gscreen.halcomp
            c = h['change-tool']
            n = h['tool-number']
            cd = h['tool-changed']
            print "tool change",c,cd,n
            if c:
                message =  _("Please change to tool # %s, then click OK."% n)
                self.gscreen.warning_dialog(message, True,pinname="TOOLCHANGE")
            else:
                h['tool-changed'] = False

    def on_button_edit_clicked(self,widget):
        state = widget.get_active()
        if not state:
            self.gscreen.edited_gcode_check()
        self.widgets.notebook_main.set_current_page(0)
        self.widgets.notebook_main.set_show_tabs(not (state))
        self.edit_mode(state)
        if state:
            self.widgets.search_box.show()
        else:
            self.widgets.search_box.hide()

    def edit_mode(self,data):
        print "edit mode pressed",data
        self.gscreen.sensitize_widgets(self.data.sensitive_edit_mode,not data)
        if data:
            self.widgets.mode6.show()
            self.widgets.dro_frame.hide()
            self.widgets.gcode_view.set_sensitive(1)
            self.data.edit_mode = True
            self.widgets.show_box.hide()
            self.widgets.notebook_mode.show()
            self.widgets.display_btns.hide()
        else:
            self.widgets.mode6.hide()
            self.widgets.dro_frame.show()
            self.widgets.gcode_view.set_sensitive(0)
            self.data.edit_mode = False
            self.widgets.show_box.show()
            self.widgets.display_btns.show()

    def on_button_full_view_clicked(self,widget):
        self.set_full_graphics_view(widget.get_active())

    def on_manual_spindle(self,widget):
	if self.data.mode_order[0] == self.data._AUTO:
	    return
	if self.widgets.button_man_spindle.get_active():
	    self.widgets.button_man_spindle.set_label("Stop")
	    self.emc.spindle_forward(1,self.data.spindle_start_rpm)
        else:
	    print "Spindle stop"
	    self.widgets.button_man_spindle.set_label("Start")
	    self.emc.spindle_off(1)

    def on_spindle_plus(self,widget):
	if self.data.mode_order[0] != self.data._AUTO:
	    self.emc.spindle_faster(1)

    def on_spindle_minus(self,widget):
	if self.data.mode_order[0] != self.data._AUTO:
	    self.emc.spindle_slower(1)

    def on_view_change(self,widget):
	mode = self.data.mode_order[0]
	if mode == self.data._AUTO:
	    self.data.view = self.data.view+1
	    if self.data.view > 3:
	        self.data.view = 0
	    view = self.data.view
        else:
            view = 0
	print "view", view
        if view == 0:
	    # Gremlin + Gcode + DRO
	    self.data.full_graphics = False
            self.widgets.show_box.show()
	    if mode == self.data._AUTO:
                self.widgets.notebook_mode.show()
            self.widgets.dro_frame.show()
            self.widgets.display_btns.show()
            self.widgets.gremlin.set_property('enable_dro',False)
	elif view == 1:
	    # Gremlin style DRO
	    self.data.full_graphics = True
            self.widgets.show_box.show()
            self.widgets.notebook_mode.hide()
            self.widgets.dro_frame.hide()
            self.widgets.gremlin.set_property('enable_dro',True)
	elif view == 2:
	    # Gremlin + DRO
	    self.data.full_graphics = True
            self.widgets.dro_frame.show()
            self.widgets.notebook_mode.hide()
            self.widgets.show_box.show()
            self.widgets.gremlin.set_property('enable_dro',False)
	elif view == 3:
	    # DRO + Gcode
	    self.data.full_graphics = False
            self.widgets.dro_frame.show()
	    if mode == self.data._AUTO:
                self.widgets.notebook_mode.show()
                self.widgets.gcode_view.set_sensitive(0)
            self.widgets.show_box.hide()
            self.widgets.display_btns.hide()
            self.widgets.gremlin.set_property('enable_dro',False)

    def update_override_label(self):
	self.widgets.fo.set_text("FO:  %3d%%"%(round(self.data.feed_override,2)*100))
	self.widgets.mv.set_text("RO:  %3d%%"%(round(self.data.rapid_override,2)*100))
	self.widgets.so.set_text("SO:  %3d%%"%(round(self.data.spindle_override,2)*100))

# Gremlin display buttons
    def on_d_zoomp_pressed(self,widget):
        self.widgets.gremlin.zoom_in()
    def on_d_zoomm_pressed(self,widget):
        self.widgets.gremlin.zoom_out()
    def on_d_up_pressed(self,widget):
	self.data.graphic_ypos = self.data.graphic_ypos-8
	self.widgets.gremlin.pan(self.data.graphic_xpos,self.data.graphic_ypos)
    def on_d_down_pressed(self,widget):
	self.data.graphic_ypos = self.data.graphic_ypos+8
	self.widgets.gremlin.pan(self.data.graphic_xpos,self.data.graphic_ypos)
    def on_d_right_pressed(self,widget):
	self.data.graphic_xpos = self.data.graphic_xpos+8
	self.widgets.gremlin.pan(self.data.graphic_xpos,self.data.graphic_ypos)
    def on_d_left_pressed(self,widget):
	self.data.graphic_xpos = self.data.graphic_xpos-8
	self.widgets.gremlin.pan(self.data.graphic_xpos,self.data.graphic_ypos)

    def on_spindle_gear(self,widget):
        data = widget.get_value()
	self.gscreen.prefs.putpref('spindle_gear', data,float)
        if data == 2500:
            self.gscreen.halcomp["spindle-gear-sel"] = True
        elif data == 1250:
            self.gscreen.halcomp["spindle-gear-sel"] = False

    def on_accel_sel(self,widget):
        data = widget.get_value()
	self.gscreen.prefs.putpref('accel_sel', data,float)

    def on_nb_page_change(self,widget,a,page):
	# If switching from page 5 (Probe) to 0 set the mode to manual.
        if self.data.notebook_page == 5:
            if page == 0:
                self.emc.set_manual_mode()
                print "Set Mode to Manual"
        self.data.notebook_page = page

# Connect to gscreens regular signals and add a couple more
    def connect_signals(self,handlers):
        self.gscreen.connect_signals(handlers)
        # connect to handler file callbacks:
        self.gscreen.widgets.d_zoomp.connect("clicked", self.on_d_zoomp_pressed)
        self.gscreen.widgets.d_zoomm.connect("clicked", self.on_d_zoomm_pressed)
        self.gscreen.widgets.d_up.connect("clicked", self.on_d_up_pressed)
        self.gscreen.widgets.d_down.connect("clicked", self.on_d_down_pressed)
        self.gscreen.widgets.d_left.connect("clicked", self.on_d_left_pressed)
        self.gscreen.widgets.d_right.connect("clicked", self.on_d_right_pressed)
        self.gscreen.widgets.button_man_spindle.connect("clicked", self.on_manual_spindle)
        self.gscreen.widgets.button_spindle_plus.connect("clicked", self.on_spindle_plus)
        self.gscreen.widgets.button_spindle_minus.connect("clicked", self.on_spindle_minus)
        self.gscreen.widgets.button_view.connect("clicked", self.on_view_change)
        self.gscreen.widgets.button_mode.connect("button_press_event", self.on_mode_clicked)
        self.gscreen.widgets.button_edit.connect("clicked", self.on_button_edit_clicked)
        self.gscreen.widgets.button_flood.connect("clicked", self.on_button_flood)
        self.gscreen.widgets.ignore_toolchange.connect("clicked", self.on_ign_toolc_pressed)
        self.gscreen.widgets.spindle_gear.connect("value-changed", self.on_spindle_gear)
        self.gscreen.widgets.accel_sel.connect("value-changed", self.on_accel_sel)
        self.gscreen.widgets.jog_r1.connect("pressed", self.on_jog_rate)
        self.gscreen.widgets.jog_r2.connect("pressed", self.on_jog_rate)
        self.gscreen.widgets.jog_r3.connect("pressed", self.on_jog_rate)
        self.gscreen.widgets.jog_r4.connect("pressed", self.on_jog_rate)
        self.gscreen.widgets.jog_plus.connect("clicked", self.jog_point1)
        self.gscreen.widgets.jog_minus.connect("clicked", self.jog_point1)
	self.gscreen.widgets.button_homing.connect("clicked", self.homing)
	self.gscreen.widgets.notebook_main.connect("switch-page", self.on_nb_page_change)
	self.widgets.hal_status.connect("all-homed",self.on_hal_status_all_homed)
	self.widgets.hal_status.connect("state-off",self.on_emc_off)
	self.gscreen.widgets.button_clear.connect("clicked", self.on_btn_clear)
	self.widgets.hal_status.connect("interp-idle",self.on_hal_status_interp_idle)
	self.widgets.hal_status.connect("interp-run",self.on_interp_run)

# standard handler call
def get_handlers(halcomp,builder,useropts,gscreen):
     return [HandlerClass(halcomp,builder,useropts,gscreen)]
