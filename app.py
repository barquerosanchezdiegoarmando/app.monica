from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Definir la interfaz de usuario
app_ui = ui.page_fluid(
    ui.panel_title("Herramienta de Scoring e Índices"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file_upload", "Elija un archivo Excel", accept=[".xlsx"]),
            ui.input_date_range("date_range", "Rango de fechas:", start="2023-01-01", end="2024-01-01"),
            ui.input_action_button("assign_scoring", "Asignar Scoring"),
            ui.input_action_button("download_report", "Descargar reporte")
        ),
        ui.panel_main(
            ui.h3("Información General"),
            ui.tags.ul(
                ui.tags.li("Para ejecutar la app, busque el archivo .xlsx con la información necesaria para ejecutar la app"),
                ui.tags.li("Se recomienda elegir al menos 2 años de información"),
                ui.tags.li("Presione el botón de Generar Score para generar todos los resultados, después puede navegar pestaña por pestaña"),
                ui.tags.li("Para buscar información específica para una empresa, puede copiar el nombre del cuadro que se muestra abajo")
            ),
            ui.output_text("file_info"),
            ui.output_plot("histogram_plot")
        )
    )
)

# Definir la lógica del servidor
def server(input, output, session):
    @reactive.event(input.file_upload)
    def file_info():
        file = input.file_upload()
        if file:
            df = pd.read_excel(file[0]["datapath"])
            return f"Archivo subido: {file[0]['name']} ({file[0]['size']} bytes)\n{df.head()}"
        return "No se ha subido ningún archivo."
    
    @output
    @render.text
    def file_info_output():
        return file_info()

    @reactive.event(input.file_upload)
    def data():
        file = input.file_upload()
        if file:
            df = pd.read_excel(file[0]["datapath"])
            return df
        return pd.DataFrame()

    @output
    @render.plot
    def histogram_plot():
        df = data()
        if not df.empty:
            df.hist(figsize=(10, 8))
            plt.tight_layout()
            plt.show()

# Crear la aplicación
app = App(app_ui, server)

# Correr la aplicación
if __name__ == "__main__":
    app.run()