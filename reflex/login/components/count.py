
import reflex as rx

from rxconfig import config


class State(rx.State):
    count = 0
    
    def aumentar (self):
        self.count += 1
    
    def reducir (self):
        self.count -= 1


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
            rx.heading(
                "Contador", size= "9"
            ),
        rx.hstack(
            rx.button( "+",
                color_scheme= "green",
                on_click= State.aumentar
            ),
            rx.heading(State.count, size="6"),
            rx.button( "-",
                color_scheme= "ruby",
                on_click= State.reducir
            ),
        )
        
        # rx.color_mode.button(position="top-right"),
        # rx.vstack(
        #     rx.heading("Welcome to Reflex!", size="9"),
        #     rx.text(
        #         "Get started by editing ",
        #         rx.code(f"{config.app_name}/{config.app_name}.py"),
        #         size="5",
        #     ),
        #     rx.link(
        #         rx.button("Check out our docs!"),
        #         href="https://reflex.dev/docs/getting-started/introduction/",
        #         is_external=True,
        #     ),
        #     spacing="5",
        #     justify="center",
        #     min_height="85vh",
        # ),
    )


app = rx.App()
app.add_page(index)
