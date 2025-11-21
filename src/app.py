class App:
    def __init__(self, viite_service, io):
        self.viite_service = viite_service
        self.io = io

    def run(self):
        while True:
            command = self.io.read("> ")

            if not command:
                break

            if command == "uusi":
                tyyppi = self.io.read("Viitteen tyyppi: ")

                kysyttavat = self.viite_service.anna_tagit(tyyppi)

                tagit = {}
                for tagi in kysyttavat:
                    tagit[tagi] = self.io.read(f"{tagi}: ")

                self.viite_service.luo_viite(tyyppi, tagit)

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))
