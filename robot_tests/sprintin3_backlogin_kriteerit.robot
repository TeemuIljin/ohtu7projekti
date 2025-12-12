*** Test Cases ***
Käyttäjänä tiedän tapahtuneista virheistä
[Documentation]     Hyväksymiskriteerit
...     Ohjelma ei heitä virheen tapahtuessa ohjelmasta ulos
...     Ohjelma ilmoittaa virheen tapahtuneen

Käyttäjänä voin lisätä minkä tahansa tyypin viitteen
[Documentation]     Hyväksymiskriteerit
...     Viite voi olla arvoltaan "muu"
...     Viite tallentuu samalla tyylillä, kuin muutkin viitteet

Käyttäjä voi lisätä olemassaolevaan viitteeseen tägejä
[Documentation]     Hyväksymiskriteerit
...     Jo olemassa olevaa vitettä on mahdollista muokata
...     Muokkauksessa voi lisätä kokonaan uusia tägejä

Käyttäjä voi lisätä olemassaolevaan viitteeseen kategorioita
[Documentation]     Hyväksymiskriteerit
...     Jo olemassa olevaa viitettä on mahdollista muokata
...     Muokkauksessa voi lisätä kokonaan uuden kategorian

Käyttäjänä voin antaa ohjelmalle vapaampaa dataa, jonka se hyväksyy
[Documentation]     Hyväksymiskriteerit
...     Viitteeseen on mahdollista lisätä muitakin kuin standardisoituja tägejä
...     Tägin otsikko voi olla mikä tahansa
...     Tägin sisältö voi olla mitä tahansa
...     Ohjelma tallentaa täysin uudet tägit samalla tavalla kuin standartoidut