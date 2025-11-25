class App:
    def __init__(self, viite_service, io):
        self.viite_service = viite_service
        self.io = io

    def run(self):
        self.io.write("Komennot: uusi, hae, poista, muokkaa, listaa, bibtex, lopeta")

        while True:
            command = self.io.read("> ")

            if not command:
                break

            if command == "lopeta":
                break
                
            if command == "uusi":
                tyyppi = self.io.read("Viitteen tyyppi: ")

                kysyttavat = self.viite_service.anna_tagit(tyyppi)

                tagit = {}
                for fi_nimi, bib_nimi in kysyttavat:
                    tagit[bib_nimi] = self.io.read(f"{fi_nimi}: ")

                self.viite_service.luo_viite(tyyppi, tagit)
                self._listaa_viitteet()
                
            elif command == "muokkaa":
                muokattava = self.io.read("Muokattavan viite: ")
                tagi = self.io.read("Mitä viitteestä muokataan: ")
                arvo = self.io.read("Uusi arvo: ")

                self.viite_service.muokkaa_tagia(muokattava, tagi, arvo)

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))
                self.io.write("\n\n".join(map(str, self.viite_service.anna_viitteet())))
                
            elif command == "hae":
                polku = self.io.read("Datalähteen polku (Enter käyttää oletusta): ").strip()
                try:
                    maara = self.viite_service.hae_viitteet_tiedostosta(polku or None)
                    self.io.write(f"Hain {maara} viitettä.")
                except (FileNotFoundError, ValueError) as err:
                    self.io.write(f"Virhe: {err}")
                    
            elif command == "listaa":
                self._listaa_viitteet()
                
            elif command == "bibtex":
                polku = self.io.read("BibTeX-tiedoston polku (Enter käyttää oletusta): ").strip()
                kohde = self.viite_service.kirjoita_bibtex(polku or None)
                self.io.write(f"Tallennettu tiedostoon {kohde}")
                
            else:
                self.io.write("Tuntematon komento.")

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))

            if command == "poista":
                
                id = self.io.read("Viitteen tunniste: ")
                self.viite_service.poista_viite(id)

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))

    def _listaa_viitteet(self):
        viitteet = self.viite_service.anna_viitteet()
        if not viitteet:
            self.io.write("Ei yhtään viitettä.")
            return
                
        
