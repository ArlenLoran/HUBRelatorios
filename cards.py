import flet
from flet import *
from controls import return_control_reference, add_to_control_reference
from configurations import *
from queries import *

control_map = return_control_reference()

class card_receiving(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardReceiving", self)


        self.logo = Container(
                        width=52, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "DLX",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardReceiving':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardReceiving':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()


    def app_form_input_field(self, sugestion, name: str, expand: int):
        return Container(
            expand=True,
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                    Text(
                        value=name,
                        size=9, color="black",
                        weight="bold"
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    ),
                ]
            )
        )


    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )


    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Recebimento", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.Dropdown(None,"Operação",["Embu","Itupeva"]),
                self.app_form_input_field(None,"SKU", 1),
                self.app_form_input_field(None,"Lote", 1),
                self.app_form_input_field(None,"Data inicial", 1),
                self.app_form_input_field(None,"Data final", 1),
                Divider(height=5, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: RecevingToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_shipment(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardShipment", self)

        self.logo = Container(
                        width=52, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "DLX",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardShipment':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardShipment':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()


    def app_form_input_field(self, sugestion, name: str, expand: int):
        return Container(
            expand=True,
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                    Text(
                        value=name,
                        size=9, color="black",
                        weight="bold"
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    ),
                ]
            )
        )


    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )


    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Expedição", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.Dropdown(None,"Operação",["Embu","Itupeva"]),
                self.app_form_input_field(None,"SKU", 1),
                self.app_form_input_field(None,"Lote", 1),
                self.app_form_input_field(None,"Data inicial", 1),
                self.app_form_input_field(None,"Data final", 1),
                Divider(height=5, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: ShipmentToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_stock(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardStock", self)

        self.logo = Container(
                        width=52, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "DLX",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardStock':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardStock':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()


    def app_form_input_field(self, sugestion, name: str, expand: int):
        return Container(
            expand=True,
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                    Text(
                        value=name,
                        size=9, color="black",
                        weight="bold"
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    ),
                ]
            )
        )


    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )


    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Estoque", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.Dropdown(None,"Operação",["Embu","Itupeva"]),
                self.app_form_input_field(None,"SKU", 1),
                self.app_form_input_field(None,"Lote", 1),
                Divider(height=130, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: StockToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_production(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardProduction", self)

        self.logo = Container(
                        width=120, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "PROTHEUS",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardProduction':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardProduction':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()


    def app_form_input_field(self, sugestion, name: str, expand: int):
        return Container(
            expand=True,
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                    Text(
                        value=name,
                        size=9, color="black",
                        weight="bold"
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    ),
                ]
            )
        )


    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )


    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Produção", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.app_form_input_field(None, "Data inicial", 1),
                self.app_form_input_field(None, "Data final", 1),
                Divider(height=190, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: ProdutionToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_devolution(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardDevolution", self)

        self.logo = Container(
                        width=120, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "PROTHEUS",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardDevolution':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardDevolution':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()

    def app_form_input_field(self, sugestion, name: str, expand: int):
        return Container(
            expand=True,
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                    Text(
                        value=name,
                        size=9, color="black",
                        weight="bold"
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        content_padding=0,
                        cursor_color="black",
                        cursor_width=1,
                        cursor_height=18,
                        color="black"
                    ),
                ]
            )
        )


    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )


    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Devolução", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.app_form_input_field(None, "Data inicial", 1),
                self.app_form_input_field(None, "Data final", 1),
                Divider(height=190, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: DevolutionToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_analytic(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardAnalytic", self)

        self.logo = Container(
                        width=120, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "PROTHEUS",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardAnalytic':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardAnalytic':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()

    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Analítico", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                Divider(height=315, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: AnaliticoToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_ocupation(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardOcupation", self)

        self.logo = Container(
                        width=120, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "DLX",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))
    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardOcupation':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardOcupation':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()

    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Ocupação", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.Dropdown(None, "Operação", ["Embu", "Itupeva"]),
                Divider(height=255, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: OcupationToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )

class card_basedlx(UserControl):
    def __init__(self):
        super().__init__()

    def app_instance(self):
        add_to_control_reference("CardBaseDlx", self)

        self.logo = Container(
                        width=120, height=52, bgcolor="transparent",
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            "DLX",
                            color="red",
                            size=20,
                            weight="Bold"
                        ))
    def Dropdown(self, sugestion, name, values):
        listaFunc = []
        for x in values:
            listaFunc.append(x)

        return Container(
            height=45,
            bgcolor="#E1E6ED",
            border_radius=6,
            expand=1,
            padding=8,
            content=Column(
                expand=True,
                spacing=1,
                controls=[
                        Text(
                            value=name,
                            size=9, color="black",
                            weight="bold"
                        ),
                    Dropdown(
                        border_color="transparent",
                        height=20,
                        text_size=13,
                        hint_text=sugestion,
                        hint_style=TextStyle(size=12, color="grey"),
                        options=[dropdown.Option(x) for x in listaFunc],
                        content_padding=0,
                        color="black",
                    )
                    ,
                ]
            )
        )

    def status(self):
        return Row(
            vertical_alignment="center",
            alignment="center",
            spacing=5,
            opacity=1,
            animate_opacity=Animation(100),
            controls=[Container(
                width=6,
                height=6,
                shape=BoxShape("circle"),
                bgcolor="cyan"
            ), Text("Gerar relatório", size=10, color="black")],
        )

    def HightLight(self, event):
        for key, value in control_map.items():
                if key == 'CardBaseDlx':
                    if event.data == 'true':
                        value.controls[0].shadow= BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.with_opacity(1, "red"),
                            offset=Offset(2,2)
                        ),
                        value.controls[0].update()
                    else:
                        value.controls[0].shadow = BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=colors.with_opacity(0.21, "black"),
                            offset=Offset(2, 2)
                        ),
                value.controls[0].update()

    def button(self, name, onclick):
        return ElevatedButton(name, bgcolor="red", color="white", on_click=onclick)


    def open_card(self, event):
        if event.control.height == 180:
            event.control.height = 560
            event.control.width = 260
            event.control.update()

    def close_card(self, event):
        for key, value in control_map.items():
            if key == 'CardBaseDlx':
                value.controls[0].width = 160
                value.controls[0].height = 180
                value.controls[0].update()

    def build(self):
        self.app_instance()
        return Container(
                width= 160,
                height= 180,
                padding=10,
                on_hover=lambda e: self.HightLight(e),
                on_click=lambda e: self.open_card(e),
                bgcolor= "#FFFFFF",
                border_radius= 5,
                animate= Animation(420, "easeInOutBack"),
                data= False,
                clip_behavior= ClipBehavior.HARD_EDGE,
                shadow= BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=colors.with_opacity(0.21, "black"),
                    offset=Offset(2,2)
                ),
                content=Column(
            alignment="start",
            horizontal_alignment="center",
            controls=[
                Divider(height=5, color="transparent"),
                Row(
                    controls=[
                        self.logo
                    ],
                    alignment="center"
                ),
                Text("Base DLX", size=18, color="black", font_family="Open Sans"),
                Divider(height=5, color="transparent"),
                self.status(),
                Divider(height=5, color="transparent"),
                self.Dropdown(None, "Operação", ["Embu", "Itupeva"]),
                Divider(height=255, color="transparent"),
                Row(
                    vertical_alignment="center",
                    alignment="center",
                    controls=[self.button("Voltar", lambda e: self.close_card(e)), self.button("Extrair", lambda e: BaseDlxToExcel(e))]
                ),
                Divider(height=5, color="transparent"),
                    ]
            )
        )