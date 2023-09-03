Dobrý den, vítejte v projektu číslo 3 - Elections Scraper
---------------------------------------------------------------------------------------------
Hlavním cílem celého projektu je získat data s internetového webu zaměřeného na vyhodnocování 
volebních výsledků.
---------------------------------------------------------------------------------------------
Krok číslo 1:
---------------------------------------------------------------------------------------------
Prvním krokem při tvorbě projektu bylo vytvořit si virtuální prostředí (virtual environment) venv 
a následně do něj nahrát příslušné knihovny třetích stran, společně se zabudovanými
>>> instalace virtuálního prostředí pomocí příkazu: python3 -m venv venv
>>> následná aktivace virtuálního prostředí pomocí příkazu: source venv/bin/activate

Do virtuálního prostředí poté pomocí funkce import naimporotvat knihovny: csv a sys

Následně je potřeba naimportovat několik knihoven třetích stran: requests a bs4, které
jsou potřeba pro získání informací z URL adresy.

>>> knihovny třetích stran lze nahrát pomocí příkazu: pip install + název knihovny.

Poté je třeba vytvořit soubor requirements.txt
---------------------------------------------------------------------------------------------
Krok číslo 2:
---------------------------------------------------------------------------------------------
K vytvoření souboru requirements.txt je vhodné použít příkaz: pip freeze > requirements.txt, který
vytvoří .txt soubor se všemi knihovnami použitými v rámci virtuálního prostředí

Následně je důležité celý program zapsat do dílčích funkcí, které jsou následně spouštěny přes 
hlavní funkci main().
---------------------------------------------------------------------------------------------
Fungování programu
---------------------------------------------------------------------------------------------
Samotný program funguje díky dvoum skupinám funkcí. První skupina vydefinovaných funkcí ověří správnost 
vstupních argumentů do konzole, který se musí rovnat dvěma, přičemž první musí být URL adresa začínající na:
"https://volby.cz/pls/ps2017nss" a druhý může být libovolný název souboru, do kterého jsou data z argumetu
číslo jedna exportovány.

Druhá skupina funkcí "scrapuje" data z webové stránky, jejíž URL jsme do konzole zadali v prvním vstupním argumentu a vypíše je do csv souboru, se kterým lze pracovat v rámci tabulkoých editorů (např. MS Excel).
---------------------------------------------------------------------------------------------
Testování programu
---------------------------------------------------------------------------------------------
Program je spouštěn přes soubor main.py.
Pro otestování potřebujeme zadat 2 argumenty:
První argument bude URL, například Volební výsledky Pardubického kraje, okresu Svitavy.
--> "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5303"
Druhý argument bude název našeho souboru, například:
-->  Okres_Svitavy_volby_2017

Po spuštění stačí do terminálu zadat následující příkaz:
--> python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5303" Okres_Svitavy_volby_2017

Po nějaké chvíly se vytvoří soubor obsahující data z volebních výsledků pro námi zvolný okres. Soubor
je ve formátu .csv a nese název námi zvolený na základě argumentu č.2.
---------------------------------------------------------------------------------------------
Encoding
---------------------------------------------------------------------------------------------
Při otevření .csv v souboru může nastat špatná vizualizace dat. V Python prostředí je tetnto poblém vyřešen pomocí encoding='utf-8', avšak po otevření souboru v excelu můžou být data graficky zkreslená.

Problému lze předejít v prostředí MS excel --> Záložka Data --> Načíst Data (Power Query) --> zvolit Text/CSV 
--> zvolit soubor Okres_Svitavy_volby_2017 --> tlačítko Procházet

Pomocí tohoto postupu lze zmíněný problém vyřešit.
