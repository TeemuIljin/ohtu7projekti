*** Settings ***
Library  ../src/ViiteLibrary.py

*** Keywords ***
Luo Testiviite Kirja
    [Arguments]  ${kirjoittaja}  ${nimi}  ${vuosi}  ${julkaisija}
    Luo Viite  book  ${kirjoittaja}  ${nimi}  ${vuosi}  ${julkaisija}

Luo Testiviite Artikkeli
    [Arguments]  ${kirjoittaja}  ${nimi}  ${vuosi}
    Luo Viite  article  ${kirjoittaja}  ${nimi}  ${vuosi}

