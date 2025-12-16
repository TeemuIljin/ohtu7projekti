# ohtu7projekti

[![Testien tila](https://github.com/TeemuIljin/ohtu7projekti/actions/workflows/ci.yml/badge.svg)](https://github.com/TeemuIljin/ohtu7projekti/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/TeemuIljin/ohtu7projekti/branch/main/graph/badge.svg)](https://codecov.io/gh/TeemuIljin/ohtu7projekti)

Linkki backlogiin Excel:
https://jyu-my.sharepoint.com/:x:/g/personal/iljitesa_jyu_fi/IQADiqLZVoVhQqi-13ucvxxHAVHBTSrdfIREZ8CGXW37-0E?e=hIiWEL

Linkki raporttiin:
https://jyu-my.sharepoint.com/:w:/g/personal/vartivov_jyu_fi/IQCcnmq5SGueT6fJLrB4YfgfAZeg_rU7f6qBDbRFalusqh0?e=mbd1X4

## Definition of Done

- Koodi on yhdistetty mainiin
- Kaikki hyväksymäkriteerit on toteutettu
- Testit on totetutettu ja ne läpäisevät tarkistukset
- Luodut ominaisuudet toimivat oikein
- Ohjelma toimii paikallisessa ympäristössä

## Käyttöohjeet

### Uuden viitteen luominen

Uuden viitteen luominen tapahtuu komennolla `uusi`.

Ohjelma kysyy viitteen tyyppiä ja siihen liittyviä pakollisten tagien arvoja. Tämän jälkeen on mahdollista antaa valinnaisia tageja, jotka ohjelma kysyy yksi kerrallaan. Kun olet valmis, jätä kysymys "Valinnainen tagi" tyhjäksi.

Valinnainen tagi voi olla mikä tahansa (esim. kannen väri), mutta jos annat alempana olevassa listassa olevan vaihtoehdon, ohjelma tallentaa BibTeX-tiedostoon aina englanninkielisen ilmaisun. Muussa tapauksessa tallennetaan käyttäjän syöte sellaisenaan tagin nimeksi.

Sekä viitetyypin että tagin voi antaa suomeksi tai englanniksi. Ohjelma ymmärtää molemmat.

**Kategorian lisääminen:** Voit lisätä viitteelle kategorian antamalla valinnaisen tagin `kategoria` (tai `category`) ja sille haluamasi arvon.

#### Viitetyyppivaihtoehdot:

| suomeksi             | englanniksi     |
| -------------------- | --------------- |
| `artikkeli`          | `article`       |
| `kirja`              | `book`          |
| `vihkonen`           | `booklet`       |
| `kirjan osa`         | `inbook`        |
| `artikkeli kirjassa` | `incollection`  |
| `konferenssi`        | `inproceedings` |
| `konferenssi`        | `conference`    |
| `käsikirja`          | `manual`        |
| `pro gradu`          | `mastersthesis` |
| `väitöskirja`        | `phdthesis`     |
| `tekninen raportti`  | `techreport`    |
| `sekalaista`         | `misc`          |
| `julkaisukokoelma`   | `proceedings`   |
| `julkaisematon`      | `unpublished`   |

#### Tagivaihtoehdot:

| suomeksi        | englanniksi    |
| --------------- | -------------- |
| `osoite`        | `address`      |
| `lisähuomautus` | `annote`       |
| `kirjoittaja`   | `author`       |
| `julkaisu`      | `booktitle`    |
| `luku`          | `chapter`      |
| `painos`        | `edition`      |
| `toimittaja`    | `editor`       |
| `julkaisumuoto` | `howpublished` |
| `laitos`        | `institution`  |
| `lehti`         | `journal`      |
| `kuukausi`      | `month`        |
| `huomautus`     | `note`         |
| `numero`        | `number`       |
| `organisaatio`  | `organization` |
| `sivut`         | `pages`        |
| `julkaisija`    | `publisher`    |
| `oppilaitos`    | `school`       |
| `sarja`         | `series`       |
| `teoksen nimi`  | `title`        |
| `tyyppi`        | `type`         |
| `vuosikerta`    | `volume`       |
| `vuosi`         | `year`         |
| `kategoria`     | `category`     |

#### Käyttöesimerkki

```
> uusi
Viitteen tyyppi: kirja
kirjoittaja: Sofi Oksanen
teoksen nimi: Puhdistus
julkaisija: WSOY
vuosi: 2008
Valinnainen tagi: painos
painos: 3
Valinnainen tagi: sivut
sivut: 10-30
Valinnainen tagi: [enter]
```

Nyt viite on luotu. Esimerkin tapauksessa ohjelma loi BibTeX-formaatin mukaisen viitteen:

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY},
  year = {2008},
  edition = {3},
  pages = {10-30}
}
```

### Viitteen muokkaaminen

Viitteen muokkaus tapahtuu komennolla `muokkaa`

Ohjelma kysyy käyttäjältä muokattavan viitteen nimeä, jonka jälkeen ohjelma kysyy mitä 
tägiä viitteestä muokataan. Tämän jälkeen käyttäjä syöttää uuden arvon muokattavalle tägille.

#### Käyttöesimerkki

Olemassa oleva viite:

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY},
  year = {2008},
  edition = {3},
  pages = {10-30}
}  
```
Muokkaa komento:
   
```
>muokkaa
Muokattavan viitteen nimi: Puhdistus
Luodaanko uusi viite? (kyllä/ei)

Vaihtoehto kyllä:
Valinnainen tagi: Kirjan väri
Kirjan väri: sininen

Vaihtoehto ei:
Mitä viitteestä muokataan: sivut
Uusi arvo: 15-30

```
Nyt viitettä on muokattu ja ohjelma ilmoittaa viestillä: "Viite Puhdistus on muokattu."
Ohjelma myös tulostaa tämän perään viitteet:

```
@book{SofiOksanen2008,
author = {Sofi Oksanen},
title = {Puhdistus},
year = {2008},
publisher = {Like},
pages = {1-30},
Kirjan väri = {sininen}
}

@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30}
}

```

### Viitteen poistaminen

Viitteen poistaminen tapahtuu komennolla `poista` 
Ohjelma kysyy käyttäjältä poistettavan viitteen nimeä. Jos viitettä ei löydy, ohjelma kertoo, ettei 
kyseistä viitettä ole olemassa.

#### Käyttöesimerkki

Olemassa oleva viite:

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY},
  year = {2008},
  edition = {3},
  pages = {10-30}
}  
```

Poista komento:

```
>poista
Poistettavan viitteen nimi: Puhdistus

```
Nyt viite on poistettu ja ohjelma ilmoittaa viestillä: "Viite 'Puhdistus' on poistettu."

### Viitteiden suodattaminen

Viitteiden suodattaminen tapahtuu komennolla `suodata`.

Ohjelma kysyy suodatuskriteerejä: viitteen tyyppi, vuosi ja kirjoittaja. Voit jättää minkä tahansa kriteerin tyhjäksi ohittaaksesi sen. Kirjoittajahaku toimii osittaishaulla.

#### Käyttöesimerkki

```
> suodata
Suodatuskriteerit (jätä tyhjäksi ohittaaksesi):
Viitteen tyyppi: book
Vuosi: 
Kirjoittaja: Oksanen
Löytyi 1 viitettä:
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY},
  year = {2008}
}
```

Voit myös suodattaa pelkästään yhdellä kriteerillä:

```
> suodata
Suodatuskriteerit (jätä tyhjäksi ohittaaksesi):
Viitteen tyyppi: 
Vuosi: 2008
Kirjoittaja: 
Löytyi 1 viitettä:
...
```

### Kategoria haku

Kategorioita voi lisätä viitteeseen aina yhden. Kategoria voi olla mitä tahansa.
Kategorian lisääminen tapahtuu `uusi` komennon kautta lisäämällä valinnainen tägi.

Viitteitä voi hakea kategorioittan komennolla `hae kategoriaa`. 
Komento kysyy käyttäjältä haettavan kategorian nimeä.

#### Käyttöesimerkki

Olemassa oleva viite: 

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}
```

Hae kategoriaa komento:

```
>hae kategoriaa
Haettava kategoria: tärkeä
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY},
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}  
```

### Viitteen haku nimellä 

Viitteitä voi haeka nimellä antamalla komennon `hea nimella`. Komento kysyy haettavan viitteen nimeä. Viitteen Koko nimeä ei tarvitse muistaa, vaan riittää vain osa nimestä.

Haun jälkeen käyttäjälle listataan kaikki viitteet joiden nimessä annettu hakusana on. Jos hakua vastaavia viitteitä ei ole, ohjelma kertoo, ettei vastaavia viitteitä löytynyt. 

Hakusanan täytyy olla vähintään yksi kirjain tei merkki. Jos näin ei ole, ohjelma ilmoittaa käyttäjälle "hakusanan täytyy olla vähintään yksi kirjain tai merkki".

#### Käyttöesimerkki

Olemassa oleva viite: 

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}
```

Hae viitettä nimellä komento:

```
>hae nimella
Haettavan viitteen nimi tai osa nimesta: puh
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}
```

### Viitteiden listaus 

Lisättyjä viitteitä voi tarkistella komennolla `listaa`. Se listaa kaikki olemassa olevat viitteet aakkosjärjestyksessä. Jos viitteitä ei ole, ohjelma ilmoittaa "Ei yhtään viitettä.".

#### Käyttöesimerkki

Olemassa olevat viitteet: 

```
@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}

@book{StephanieGarber2017,
  author = {Stephanie Garber},
  title = {Caraval},
  publisher = {WSOY}, 
  year = {2017},
  pages = {10-13},
  category = {tärkeä}
}
```

Listaa komento:

```
>listaa
@book{StephanieGarber2017,
  author = {Stephanie Garber},
  title = {Caraval},
  publisher = {WSOY}, 
  year = {2017},
  pages = {10-13},
  category = {tärkeä}
}

@book{SofiOksanen2008,
  author = {Sofi Oksanen},
  title = {Puhdistus},
  publisher = {WSOY}, 
  year = {2008},
  edition = {3},
  pages = {15-30},
  category = {tärkeä}
}
```

### Komentojen tarkastus

Käyettävissä olevat komennot voi tarkistaa komennolla `apua`. Se kertoo komentojen nimet. Kometojen toiminnan ja käyttöesimerkit voit katsoa tästä käyttöohjeesta. 

## Testaus

### Yksikkötestit (pytest)

Yksikkötestit ajetaan komennolla:

```bash
poetry run pytest
```

### Hyväksymistestit (Robot Framework)

Projekti sisältää Robot Framework -hyväksymistestit seuraaville user storyille:

| User Story | Testitiedosto |
|------------|---------------|
| Käyttäjä voi listata viitteet | `robot_tests/listaa_viitteet.robot` |
| Käyttäjä voi suodattaa viitteitä | `robot_tests/suodata_viitteet.robot` |
| Käyttäjä voi poistaa viitteitä | `robot_tests/poista_viite.robot` |

Robot Framework -testit ajetaan komennolla:

```bash
poetry run robot robot_tests
```

Testien suorituksen jälkeen yksityiskohtainen HTML-raportti löytyy tiedostosta `report.html`.
