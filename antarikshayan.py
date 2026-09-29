import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import csv
import random

# --- System Configuration ---
RUNNING = True
SIMULATION_MODE = True  # True = simulate telemetry without physical hardware


class AntarikshayanMissionControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Antarikshayan Mission Control Hub")
        self.root.geometry("850x650")
        self.root.configure(bg="#0F172A")

        # Telemetry State Variables
        self.temp_var = tk.StringVar(value="0.0 °C")
        self.gas_var = tk.StringVar(value="0 ppm")
        self.impact_var = tk.StringVar(value="0 raw")

        self.build_ui()

        # Background telemetry thread
        self.data_thread = threading.Thread(
            target=self.process_telemetry_stream,
            daemon=True
        )
        self.data_thread.start()

    def build_ui(self):

        # 1. Main Mission Status Banner
        self.status_banner = tk.Label(
            self.root,
            text="🛰️ INITIALIZING GROUND CONTROL DATA LINK...",
            font=("Segoe UI", 13, "bold"),
            bg="#1E293B",
            fg="#F59E0B",
            height=2
        )
        self.status_banner.pack(fill=tk.X, pady=(0, 15))

        # 2. Telemetry Panels
        panel_frame = tk.Frame(
            self.root,
            bg="#0F172A"
        )
        panel_frame.pack(pady=10)

        # Temperature
        t_frame = tk.LabelFrame(
            panel_frame,
            text=" ECLSS Internal Temp ",
            bg="#1E293B",
            fg="#38BDF8",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=15
        )
        t_frame.grid(row=0, column=0, padx=15)

        tk.Label(
            t_frame,
            textvariable=self.temp_var,
            font=("Consolas", 24, "bold"),
            bg="#1E293B",
            fg="#34D399"
        ).pack()

        # Gas concentration
        g_frame = tk.LabelFrame(
            panel_frame,
            text=" Air Quality (Gas Density) ",
            bg="#1E293B",
            fg="#38BDF8",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=15
        )
        g_frame.grid(row=0, column=1, padx=15)

        tk.Label(
            g_frame,
            textvariable=self.gas_var,
            font=("Consolas", 24, "bold"),
            bg="#1E293B",
            fg="#34D399"
        ).pack()

        # Structural impact
        i_frame = tk.LabelFrame(
            panel_frame,
            text=" Structural Hull Load ",
            bg="#1E293B",
            fg="#38BDF8",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=15
        )
        i_frame.grid(row=0, column=2, padx=15)

        tk.Label(
            i_frame,
            textvariable=self.impact_var,
            font=("Consolas", 24, "bold"),
            bg="#1E293B",
            fg="#F87171"
        ).pack()

        # 3. Telecommand Console
        cmd_deck = tk.LabelFrame(
            self.root,
            text=" Flight Command Telemetry Deck ",
            bg="#1E293B",
            fg="#C084FC",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=15
        )
        cmd_deck.pack(
            fill=tk.X,
            padx=35,
            pady=15
        )

        # Vent ON
        tk.Button(
            cmd_deck,
            text="🚀 Activate Cabin Vent Fan",
            command=lambda: self.execute_telecommand("VENT_ON"),
            bg="#0EA5E9",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=10)

        # Vent OFF
        tk.Button(
            cmd_deck,
            text="🛑 Deactivate Vent Fan",
            command=lambda: self.execute_telecommand("VENT_OFF"),
            bg="#475569",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=10)

        # Clear alarm
        tk.Button(
            cmd_deck,
            text="🧹 Reset Master Alarm flags",
            command=lambda: self.execute_telecommand("ALARM_CLR"),
            bg="#EF4444",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=10)

        # 4. Live Event Feed
        tk.Label(
            self.root,
            text="Live Flight Events Sequence:",
            bg="#0F172A",
            fg="#94A3B8",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(10, 0)
        )

        self.terminal_feed = tk.Text(
            self.root,
            height=14,
            bg="#1E293B",
            fg="#E2E8F0",
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.terminal_feed.pack(
            fill=tk.X,
            padx=35,
            pady=5
        )

        self.terminal_feed.insert(
            tk.END,
            f"[{time.strftime('%H:%M:%S')}] "
            "BOOT: Ground station telemetry data link online.\n"
        )

    def process_telemetry_stream(self):

        global RUNNING

        try:

            # CSV telemetry log
            with open(
                "antarikshayan_mission_data.csv",
                mode="a",
                newline=""
            ) as log_file:

                log_writer = csv.writer(log_file)

                log_writer.writerow([
                    "Timestamp",
                    "Temperature (C)",
                    "Gas (ppm)",
                    "Impact Magnitude",
                    "Impact Flag"
                ])

                while RUNNING:

                    if SIMULATION_MODE:

                        time.sleep(1)

                        # Simulated temperature
                        parsed_temp = round(
                            random.uniform(21.8, 25.4),
                            1
                        )

                        # Simulated gas concentration
                        parsed_gas = random.randint(
                            110,
                            165
                        )

                        # Simulated impact event
                        collision_event = (
                            1 if random.random() > 0.94 else 0
                        )

                        if collision_event:
                            parsed_impact = random.randint(
                                48000,
                                64000
                            )
                        else:
                            parsed_impact = random.randint(
                                120,
                                480
                            )

                        current_time = time.strftime(
                            "%H:%M:%S"
                        )

                        # Save telemetry
                        log_writer.writerow([
                            current_time,
                            parsed_temp,
                            parsed_gas,
                            parsed_impact,
                            collision_event
                        ])

                        log_file.flush()

                        # Update GUI safely
                        self.root.after(
                            0,
                            self.render_telemetry_ui,
                            parsed_temp,
                            parsed_gas,
                            parsed_impact,
                            collision_event
                        )

        except Exception as system_exception:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Critical Telemetry Crash",
                    "Ground control system caught an exception "
                    "processing incoming logs:\n"
                    + str(system_exception)
                )
            )

    def render_telemetry_ui(
        self,
        temp,
        gas,
        impact,
        flag
    ):

        self.temp_var.set(
            f"{temp} °C"
        )

        self.gas_var.set(
            f"{gas} ppm"
        )

        self.impact_var.set(
            f"{impact} raw"
        )

        if flag == 1:

            self.status_banner.config(
                text="⚠️ ALERT: ORBITAL KINETIC DEBRIS IMPACT SIGNATURE LOGGED",
                bg="#991B1B",
                fg="#FCA5A5"
            )

            self.terminal_feed.insert(
                tk.END,
                f"[{time.strftime('%H:%M:%S')}] "
                "CRITICAL: Micrometeorite impact energy "
                "parsed on channel ADC_26.\n"
            )

            self.terminal_feed.see(tk.END)

        else:

            self.status_banner.config(
                text="🛰️ BHARATIYA ANTARIKSH STATION (BAS) LINK: NOMINAL",
                bg="#065F46",
                fg="#A7F3D0"
            )

    def execute_telecommand(
        self,
        telecommand_string
    ):

        current_time = time.strftime(
            "%H:%M:%S"
        )

        self.terminal_feed.insert(
            tk.END,
            f"[{current_time}] "
            "TELECOMMAND ROUTED: -> Executed string "
            f"payload frame '{telecommand_string}'.\n"
        )

        self.terminal_feed.see(tk.END)


# --- Runtime Entry Module Execution ---

if __name__ == "__main__":

    app_root = tk.Tk()

    mission_dashboard = AntarikshayanMissionControl(
        app_root
    )

    def system_terminate_hook():

        global RUNNING

        RUNNING = False

        app_root.destroy()

    app_root.protocol(
        "WM_DELETE_WINDOW",
        system_terminate_hook
    )

    app_root.mainloop()
