import time
from rich.live import Live
from rich.layout import Layout
from terminal.panels import create_header, create_traffic_panel, create_alerts_panel, create_top_talkers_panel
from core.engine import DetectionEngine

class Dashboard:
    def __init__(self, engine: DetectionEngine, interface: str):
        self.engine = engine
        self.interface = interface
        self.layout = self.make_layout()

    def make_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main")
        )
        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        layout["left"].split_column(
            Layout(name="alerts"),
            Layout(name="traffic", size=10)
        )
        return layout

    def generate_ui(self):
        self.layout["header"].update(create_header(status="ONLINE", interface=self.interface, stats=self.engine.stats))
        self.layout["alerts"].update(create_alerts_panel(self.engine.recent_alerts))
        self.layout["traffic"].update(create_traffic_panel(self.engine.stats["protocols"]))
        self.layout["right"].update(create_top_talkers_panel(self.engine.stats["top_src"]))
        return self.layout

    def run(self):
        try:
            with Live(self.generate_ui(), refresh_per_second=2, screen=True) as live:
                while True:
                    time.sleep(0.5)
                    live.update(self.generate_ui())
        except KeyboardInterrupt:
            pass
