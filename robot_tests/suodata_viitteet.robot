*** Settings ***
Resource  resource.robot

*** Test Cases ***
Suodata Viitteet Tyypilla
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    Luo Viite  article  Tutkija  Artikkeli  2020
    ${tulokset}=  Suodata Tyypilla  book
    Suodatettujen Maara On  ${tulokset}  2
    Suodatetuissa On Viite  ${tulokset}  Sinuhe
    Suodatetuissa On Viite  ${tulokset}  Tuntematon sotilas

Suodata Viitteet Vuodella
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    Luo Testiviite Kirja  Sofi Oksanen  Puhdistus  2008  Like
    ${tulokset}=  Suodata Vuodella  1945
    Suodatettujen Maara On  ${tulokset}  1
    Suodatetuissa On Viite  ${tulokset}  Sinuhe

Suodata Viitteet Kirjoittajalla
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Mika Waltari  Turms kuolematon  1955  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    ${tulokset}=  Suodata Kirjoittajalla  Mika Waltari
    Suodatettujen Maara On  ${tulokset}  2
    Suodatetuissa On Viite  ${tulokset}  Sinuhe
    Suodatetuissa On Viite  ${tulokset}  Turms kuolematon

Suodata Viitteet Osittaisella Kirjoittajalla
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    Luo Testiviite Kirja  Vaino Linna  Tuntematon sotilas  1954  WSOY
    ${tulokset}=  Suodata Kirjoittajalla  Waltari
    Suodatettujen Maara On  ${tulokset}  1
    Suodatetuissa On Viite  ${tulokset}  Sinuhe

Suodata Ei Tuloksia
    Luo Testiviite Kirja  Mika Waltari  Sinuhe  1945  WSOY
    ${tulokset}=  Suodata Vuodella  2020
    Suodatettujen Maara On  ${tulokset}  0

