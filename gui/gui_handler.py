#import gui.slider as s


class gui:
    def __init__(self,name) -> None:
        self.name = name
        self.elements = []

    def update(self):
        for element in self.elements:
            element.update()
            element.render()

    def element_append(self,element):
        for e in self.elements:
            if e.get_name() == element.get_name():
                raise "ui element with this name exists already"
        self.elements.append(element)

    def get_element_value(self,name) -> bool | float:
        for element in self.elements:
            if element.get_name() == name:
                return element.get_value()

    def get_element_type(self,name) -> str:
        for element in self.elements:
            if element.get_name == name:
                return type(element)

    def get_element(self,name):
        for element in self.elements:
            if element.get_name() == name:
                return element

    def get_name(self):
        return self.name