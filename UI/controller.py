import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        anni = self._model.getAnni()
        for i in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(i))

    def fillShape(self, e):
        self._view.ddshape.options.clear()
        anno = self._view.ddyear.value
        print(f"{anno}")
        forme = self._model.getForma(anno)
        for i in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(i))
        self._view.update_page()

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un anno"))
            return
        if self._view.ddshape.value is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona una shape"))
            return
        anno= self._view.ddyear.value
        forma = self._view.ddshape.value
        self._model.buildGraph(anno, forma)

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNodes()} nodi e {self._model.getEdges()} archi "))

        pesi= self._model.getPesoArco()
        for p in pesi:
            self._view.txt_result.controls.append(ft.Text(f"nodo {p[0]} ha peso : {p[1]}"))

        self._view.update_page()


    def handle_path(self, e):
        self._model.searchPath()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f" Distanza: {self._model.maxDistanza}"))
        self._view.update_page()