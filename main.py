import flet
from flet import *
from configurations import *
from cards import *

def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#E1E6ED"
    page.scroll = "always"
    page.add(
        Container(
            content=Column(
                horizontal_alignment="center",
                alignment="center",
                controls=[
                    Divider(height=20, color="transparent"),
                    Text("RELATÓRIOS DLX", size=25, font_family="Open Sans"),
                    Divider(height=5, color="transparent"),
                    Row(
                        vertical_alignment=CrossAxisAlignment.START,
                        alignment="center",
                        controls=[
                            card_receiving(), card_shipment(), card_stock(), card_ocupation(), card_basedlx()
                        ]
                    ),
                    Divider(height=5, color="transparent"),
                    Text("RELATÓRIOS PROTHEUS", size=25, font_family="Open Sans"),
                    Divider(height=5, color="transparent"),
                    Row(
                        vertical_alignment=CrossAxisAlignment.START,
                        alignment="center",
                        controls=[
                            card_production(), card_devolution(), card_analytic()
                        ]
                    ),
                ]
            )
        )
    )

if __name__ == "__main__":
    flet.app(target=main, assets_dir="assets")

