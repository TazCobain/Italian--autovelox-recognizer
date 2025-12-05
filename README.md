# 📸 Verifica Censimento Autovelox (MIT)

Questo strumento in Python interagisce con la piattaforma ufficiale del **Ministero delle Infrastrutture e dei Trasporti Italiano**. 

Lo scopo è verificare se un dispositivo di rilevamento della velocità (Autovelox), identificato tramite il suo "Codice Accertatore" (o matricola), è regolarmente presente nel **Censimento dei Dispositivi**.

## ⚠️ Requisiti Fondamentali

**IMPORTANTE:** Attualmente il sistema è configurato per funzionare **esclusivamente con Mozilla Firefox**.

Per utilizzare questo script è necessario avere installato sul proprio sistema:
1.  **Python** (3.8 o superiore)
2.  **Mozilla Firefox** (Il browser deve essere installato nel sistema operativo)

> *Nota: Il driver necessario per l'automazione (Geckodriver) verrà scaricato e gestito automaticamente dallo script, ma il browser Firefox è indispensabile.*

## 📦 Installazione e Librerie

Il progetto richiede specifiche librerie Python per funzionare (Selenium, Pandas, ecc.).

1.  **Clona o scarica la repository.**
2.  **Crea un ambiente virtuale (consigliato):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Mac/Linux
    # oppure
    .\venv\Scripts\activate   # Su Windows
    ```
3.  **Installa le dipendenze:**
    Tutte le librerie necessarie sono elencate nel file `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### Le librerie principali includono:
* `selenium`: Per l'automazione del browser.
* `pandas`: Per la gestione e il salvataggio dei dati tabellari.
* `webdriver-manager`: Per la gestione automatica dei driver del browser.

## 🚀 Utilizzo

Lo script si esegue da riga di comando. Utilizare il tag -h o --help vedere la sintassi
```bash
python get_data.py --help
