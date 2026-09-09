from tkinter import END
from tkinter import messagebox as mb
import customtkinter as ctk
import threading
from PIL import Image
import pystray

import vision
import config
import user_data
import monitor

ctk.set_appearance_mode("dark")


class App:
	def __init__(self):
		self.root=ctk.CTk()
		self.root.title("Focus Guard")
		self.root.iconbitmap("assets/icon.ico")
		self.root.geometry("600x500")
		self.root.grid_columnconfigure((0, 1), weight=1)

		[self.eyes_distance,
		self.eyes_distance_pix,
		self.focal_length,
		self.alarm]=user_data.load_user_data()

		self.check=monitor.Check()
		self.vp=vision.VisionProcessor()
		
		#Calculating user image width and height
		self.frame_width=config.FRAME_WIDTH
		self.frame_height=int(self.vp.cam_height/self.vp.cam_width*config.FRAME_WIDTH)

		black_img=Image.new("RGB", (self.frame_width, self.frame_height), (0, 0, 0))
		ctkimg=ctk.CTkImage(light_image=black_img, dark_image=black_img, size=(self.frame_width, self.frame_height))

		self.cam_out_lbl=ctk.CTkLabel(self.root, image=ctkimg, text="")
		self.cam_out_lbl.grid(row=0, column=0, columnspan=2)

		fps=self.check.get_fps()
		delay=int(1000/fps)
		self.cam_out_lbl_after_id=self.cam_out_lbl.after(delay, lambda: self.update_cam_output(0))

		self.distance_lbl=ctk.CTkLabel(self.root, text="distance: unknown | angle: unknown")
		self.distance_lbl.grid(row=1, column=0, columnspan=2, pady=(5, 0))

		self.fps_lbl=ctk.CTkLabel(self.root, text=f"fps: {fps}")
		self.fps_lbl.grid(row=2, column=0, columnspan=2, pady=(0, 15))

		self.init_settings_btn=ctk.CTkButton(self.root, text="initial settings", command=self.init_settings_btn_click)
		self.init_settings_btn.grid(row=3, column=1, sticky="w", padx=10)

		self.customize_btn=ctk.CTkButton(self.root, text="customize", command=self.customize_btn_click, fg_color="#28a745", hover_color="#1d702f")
		self.customize_btn.grid(row=3, column=0, sticky="e")

		self.hide_btn=ctk.CTkButton(self.root, text="hide window", fg_color="#727372", hover_color="#565756", command=self.hide_window)
		self.hide_btn.grid(row=4, column=0, columnspan=2, pady=9)


		self.init_set_guide=ctk.CTkLabel(self.root, text="keep a distance of 60 cm from the monitor")

		self.eyes_dis_lbl=ctk.CTkLabel(self.root, text="outer eyes distance(cm):")
		self.eyes_dis_entry=ctk.CTkEntry(self.root, placeholder_text="15")
		if self.eyes_distance is not None: self.eyes_dis_entry.insert(END, self.eyes_distance)

		self.init_set_save_btn=ctk.CTkButton(self.root, text="save", fg_color="#28a745", hover_color="#1d702f", command=self.save_init_settings)

		self.alarm_lbl=ctk.CTkLabel(self.root, text="warning type:")
		self.alarm_menu=ctk.CTkOptionMenu(self.root, values=config.ALARM_OPTIONS)
		self.alarm_menu.set(config.ALARM_OPTIONS[self.alarm])

		self.customize_save_btn=ctk.CTkButton(self.root, text="save", fg_color="#28a745", hover_color="#1d702f", command=self.save_customize_settings)

		#Initializing tray icon
		tray_icon_img=Image.open("assets/icon.png")
		menu=(
			pystray.MenuItem('show window', self.show_window),
			pystray.MenuItem('exit', self.exit_app)
		)
		self.tray_icon=pystray.Icon("name", tray_icon_img, "Focus Guard", menu)



	def update_cam_output(self, frame_timestamp_ms):
		frame, frame_timestamp_ms=self.vp.detect_face(frame_timestamp_ms)

		#Checking camera access
		if frame is None:
			mb.showerror("Error", "Unable to access the camera\nPlease restart the application")
			self.exit_app()
			return

		#Showing fram on cam_out_lbl label
		frame=Image.fromarray(frame)
		frame=frame.resize((self.frame_width, self.frame_height))
		ctkimg=ctk.CTkImage(light_image=frame, dark_image=frame, size=(self.frame_width, self.frame_height))
		self.cam_out_lbl.configure(image=ctkimg)

		angle=self.vp.get_eyes_angle()
		distance=self.vp.calculate_eyes_distance(self.eyes_distance, self.focal_length)


		if None not in (angle, distance):
			self.distance_lbl.configure(text=f"distance: {round(distance)}cm | angle: {round(angle)}°")
			self.check.check_status(distance, angle)
		else:
			self.distance_lbl.configure(text="distance: unknown | angle: unknown")


		fps=self.check.get_fps()
		self.fps_lbl.configure(text=f"fps: {fps}")
		delay=int(1000/fps)
		self.cam_out_lbl_after_id=self.cam_out_lbl.after(delay, lambda: self.update_cam_output(frame_timestamp_ms))



	def init_settings_btn_click(self):
		self.init_settings_btn.grid_remove()
		self.customize_btn.grid_remove()
		self.hide_btn.grid_remove()

		self.init_set_guide.grid(row=3, column=0, columnspan=2, pady=5)
		self.eyes_dis_lbl.grid(row=4, column=0, sticky="e", padx=10)
		self.eyes_dis_entry.grid(row=4, column=1, sticky="w")
		self.init_set_save_btn.grid(row=5, column=0, columnspan=2, pady=10)

	def save_init_settings(self):
		try:
			self.eyes_distance=int(self.eyes_dis_entry.get())
		except:
			mb.showerror("Error", "Please Enter valid number in input")
			return

		self.eyes_distance_pix=self.vp.get_eyes_distance_pix()
		if self.eyes_distance_pix is None:
			mb.showerror("Error", "There is no face")
			return

		#Calculating focal length
		self.focal_length=60*self.eyes_distance_pix/self.eyes_distance

		#Saving user data
		user_data.save_user_data(
			self.eyes_distance,
			self.eyes_distance_pix,
			self.focal_length,
			self.alarm
		)

		self.init_set_guide.grid_remove()
		self.eyes_dis_lbl.grid_remove()
		self.eyes_dis_entry.grid_remove()
		self.init_set_save_btn.grid_remove()
		self.init_settings_btn.grid(row=3, column=1, sticky="w", padx=10)
		self.customize_btn.grid(row=3, column=0, sticky="e")
		self.hide_btn.grid(row=4, column=0, columnspan=2, pady=9)


	def customize_btn_click(self):
		self.init_settings_btn.grid_remove()
		self.customize_btn.grid_remove()
		self.hide_btn.grid_remove()

		self.alarm_lbl.grid(row=4, column=0, sticky="e", padx=10)
		self.alarm_menu.grid(row=4, column=1, sticky="w")
		self.customize_save_btn.grid(row=5, column=0, columnspan=2, pady=10)

	def save_customize_settings(self):
		self.alarm=config.ALARM_OPTIONS.index(self.alarm_menu.get())

		#Saving user data
		user_data.save_user_data(
			self.eyes_distance,
			self.eyes_distance_pix,
			self.focal_length,
			self.alarm
		)

		self.alarm_lbl.grid_remove()
		self.alarm_menu.grid_remove()
		self.customize_save_btn.grid_remove()
		self.init_settings_btn.grid(row=3, column=1, sticky="w", padx=10)
		self.customize_btn.grid(row=3, column=0, sticky="e")
		self.hide_btn.grid(row=4, column=0, columnspan=2, pady=9)


	def hide_window(self):
		self.root.withdraw()


	def show_window(self):
		self.root.after(0, self.root.deiconify)

	def exit_app(self):
		self.cam_out_lbl.after_cancel(self.cam_out_lbl_after_id)
		self.vp.close()
		self.tray_icon.stop()
		self.root.after(0, self.root.destroy)


	def run(self):
		threading.Thread(target=self.tray_icon.run, daemon=True).start()
		self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
		self.root.mainloop()