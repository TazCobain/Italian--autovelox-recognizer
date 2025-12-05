from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import argparse

MINISTERO_TRASPORTI_URI = "https://velox.mit.gov.it/dispositivi" # URL del sito del Ministero dei Trasporti
SEARCH_ID_FIELD = "dt-search-0"  # ID del campo di ricerca



def get_data(autovelox_code, save_to_csv = False):
    print("1. Inizializzazione driver...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Extra per headless
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)  # Timeout pagina 30s
    wait = WebDriverWait(driver, 10)

    try:
        print("2. Caricamento sito...")
        driver.get(MINISTERO_TRASPORTI_URI)
        
        print("3. Ricerca campo...")
        campo_ricerca = wait.until(EC.element_to_be_clickable((By.ID, SEARCH_ID_FIELD)))
        campo_ricerca.clear()
        campo_ricerca.send_keys(autovelox_code)
        print("4. Submit...")
        campo_ricerca.send_keys(Keys.ENTER)
        time.sleep(3)  # Attesa filtro JS

        # Fallback se non funziona: ActionChains
        try:
            actions = ActionChains(driver)
            actions.move_to_element(campo_ricerca).send_keys(Keys.ENTER).perform()
            time.sleep(3)
        except:
            pass
        
        print("5. Attesa risultati...")
        # Aspetta tabella risultati invece di sleep
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        print("6. Estrazione dati...")
        # Estrai intestazione da <thead>
        thead = driver.find_element(By.TAG_NAME, "thead")
        header_row = thead.find_element(By.TAG_NAME, "tr")
        headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th")]

        dati = [headers]  # Prima riga: intestazioni
        
        # Estrai dati da <tbody> (solo <td>)
        tbody = driver.find_element(By.TAG_NAME, "tbody")
        tabella = tbody.find_elements(By.TAG_NAME, "tr")
        for riga in tabella:
            celle = riga.find_elements(By.TAG_NAME, "td")
            if celle:  # Salta righe vuote
                dati.append([cella.text.strip() for cella in celle])

        # print(f"Dati estratti: {dati}") # stampa di controllo

        if response(dati, autovelox_code):
            if save_to_csv is not False:
                df = pd.DataFrame(dati[1:], columns=dati[0])
                df.to_csv("risultati.csv", index=False, encoding='utf-8')
                print(f"CSV salvato: {len(df)} righe estratte")
            return True       
        else:
            return False
        
    
    except Exception as e:
        print(f"ERRORE: {e}")
        
    finally:
        print("7. Chiusura driver...")
        driver.quit()
        print("FINITO!")

def response(out, mat):
    # 1. Trova l'indice della colonna "Codice Accertatore"
    try:
        # out[0] è l'intestazione
        indice_colonna = out[0].index("Codice Accertatore")
    except (IndexError, ValueError):
        # IndexError: La lista è vuota (out non ha out[0])
        # ValueError: La colonna non è stata trovata nell'intestazione
        print("ATTENZIONE: Colonna 'Codice Accertatore' non trovata nell'intestazione.")
        return "Errore di configurazione dati."

    # 2. Iterazione sui Dati (Salto l'intestazione)
    # out[1:] contiene tutte le righe di dati.
    for riga in out[1:]:
        # Controlla se la matricola cercata (mat) corrisponde al valore
        # nella colonna "Codice Accertatore" (indice_colonna)
        if riga[indice_colonna] == mat:
            return True # Trovato

    # 3. Se il ciclo finisce senza trovare corrispondenze
    return False # Non trovato

def main():
    """
    Gestisce il parsing degli argomenti da linea di comando e chiama la funzione.
    """
    # 1. Creare il parser
    parser = argparse.ArgumentParser(
        description="Uno script che interagisce dalla piattaforma nazionale del censimento degli autovelox. Inserisci il codice dell'autovelox definito come 'Codice Accertatore'. verrà fatta una vverifica sul censimento per verificare se è presente."
    )

    # 2. Aggiungere gli argomenti attesi
    parser.add_argument(
        'a',
        type=str, # Specifichiamo il tipo atteso
        help='Matricola del autovelox da cercare nel censimento'
    )

    parser.add_argument(
        '--print-raw',
        action='store_true',
        help='Se specificato, salva i dati grezzi estratti in un file CSV.'
    )

    # 3. Parsare gli argomenti
    args = parser.parse_args()

    # 4. Chiamare la funzione X con gli argomenti parsati CMAGP007
    output = get_data(
            autovelox_code = args.a,
            save_to_csv = args.print_raw # nel caso non si voglia salvare il csv il valore di default è False
            )

    # 5. Stampare il risultato
    if output:
        resp = "Sì, spiacente"
    else:
        resp = "No, fortunello"

    print(f"L'autovelox è presente nel censimento?: {resp}")


if __name__ == "__main__":
    main()