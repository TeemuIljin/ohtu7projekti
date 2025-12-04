class App:
    def __init__(self, viite_service, io):
        self.viite_service = viite_service
        self.io = io

    def run(self):
        self.io.write(
            "Komennot: uusi, hae, poista, muokkaa, listaa, bibtex, hae nimella, lopeta, hae kategoriaa, suodata")

        while True:
            command = self.io.read("> ")

            if not command:
                break

            if command == "lopeta":
                break

            if command == "uusi":
                tyyppi = self.io.read("Viitteen tyyppi: ")

                (bib_tyyppi, kysyttavat) = self.viite_service.anna_tagit_ja_bib_tyyppi(
                    tyyppi)

                # Jos tyyppiä ei ole, lopetetaan
                if kysyttavat is None:
                    self.io.write(f"Tyyppiä {tyyppi} ei ole olemassa")
                    continue

                tagit = {}
                for fi_nimi, bib_nimi in kysyttavat:
                    tagit[bib_nimi] = self.io.read(f"{fi_nimi}: ")

                while True:
                    uusi_tagi = self.io.read("Valinnainen tagi: ")

                    if uusi_tagi == "":
                        break

                    (fi_nimi, bib_nimi) = self.viite_service.anna_fi_nimi_ja_bib_nimi(
                        uusi_tagi)

                    if not bib_nimi:
                        self.io.write(f"Tagia {uusi_tagi} ei ole olemassa")
                        continue

                    if uusi_tagi:
                        arvo = self.io.read(f"{uusi_tagi}: ")
                        tagit[bib_nimi] = arvo

                self.viite_service.luo_viite(bib_tyyppi, tagit)
                self._listaa_viitteet()

            elif command == "muokkaa":
                muokattava = self.io.read("Muokattavan viitteen nimi: ")
                tagi = self.io.read("Mitä viitteestä muokataan: ")
                arvo = self.io.read("Uusi arvo: ")

                self.viite_service.muokkaa_tagia(muokattava, tagi, arvo)

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))

            elif command == "hae":
                polku = self.io.read(
                    "Datalähteen polku (Enter käyttää oletusta): ").strip()
                try:
                    maara = self.viite_service.hae_viitteet_tiedostosta(
                        polku or None)
                    self.io.write(f"Hain {maara} viitettä.")
                except (FileNotFoundError, ValueError) as err:
                    self.io.write(f"Virhe: {err}")

            elif command == "listaa":
                self._listaa_viitteet()

            elif command == "bibtex":
                polku = self.io.read(
                    "BibTeX-tiedoston polku (Enter käyttää oletusta): ").strip()
                kohde = self.viite_service.kirjoita_bibtex(polku or None)
                self.io.write(f"Tallennettu tiedostoon {kohde}")

            elif command == "poista":
                title = self.io.read("Poistettavan viitteen nimi: ") ##Kysytään poistettaan viitteen nimi
                poistettu = self.viite_service.poista_viite(title) 
                if poistettu:
                    self.io.write(f"Viite: '{title}' poistettu.")
                else:
                    self.io.write(f"Viitettä: '{title}' ei löydetty.")

            elif command == "hae nimella":
                hakusana = self.io.read(
                    "Haettavan viitteen nimi tai osa nimestä: ")
                hakusana = hakusana.strip()
                if len(hakusana) >= 1:
                    tulokset = self.viite_service.hae_nimea(hakusana)
                    if not tulokset:
                        print("Ei hakua vastaavia viitteita")
                    else:
                        for viite in tulokset:
                            print(f"{viite}\n")
                else: 
                    print("hakusanan täytyy olla vähintään yksi kirjain tai merkki")
                    
            elif command == "hae kategoriaa":
                kategoria = self.io.read("Haettava kategoria: ")
                kategoria = kategoria.strip()
                if len(kategoria) >= 1:
                    tulokset = self.viite_service.hae_kategoriaa(kategoria)
                    if not tulokset:
                        print("Ei hakua vastaavia viitteita")
                    else:
                        for viite in tulokset:
                            print(f"{viite}\n")

            elif command == "suodata":
                self.io.write("Suodatuskriteerit (jätä tyhjäksi ohittaaksesi):")
                tyyppi = self.io.read("Viitteen tyyppi: ").strip() or None
                vuosi = self.io.read("Vuosi: ").strip() or None
                kirjoittaja = self.io.read("Kirjoittaja: ").strip() or None

                tulokset = self.viite_service.suodata(tyyppi, vuosi, kirjoittaja)

                if not tulokset:
                    self.io.write("Ei suodatusta vastaavia viitteitä.")
                else:
                    self.io.write(f"Löytyi {len(tulokset)} viitettä:")
                    print("\n\n".join(map(str, tulokset)))

            else:
                self.io.write("Tuntematon komento.")

                print("\n\n".join(map(str, self.viite_service.anna_viitteet())))
    def _listaa_viitteet(self):
        viitteet = self.viite_service.anna_viitteet()
        if not viitteet:
            self.io.write("Ei yhtään viitettä.")
            return
        else:
            print("\n\n".join(map(str, viitteet)))

