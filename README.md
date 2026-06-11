# NAVA FP8 ComfyUI Wrapper

## Descrizione
Python wrapper per configurare e avviare ComfyUI con precisione FP8 per il modello NAVA, ottimizzato per RTX 3050 mantenendo Tesla P40 libero per compiti LLM.

## Architettura
- WrapperFP8 class in src/wrapper_fp8.py
- Gestisce variabili d'ambiente FP8 o configurazione dizionario
- Fornisce metodi per abilitare/disabilitare FP8, ottenere configurazione e convertire in env dict per subprocess
- Non esegue inferenza; prepara solo la configurazione per ComfyUI

## Installazione
### Prerequisiti
- Python 3.8+
- CUDA 11.8 o 12.1 (per torch con supporto FP8)
- ComfyUI installato (vedi requirements.txt)

### Setup
1. Clona il repository:
   ```bash
   git clone <repository-url>
   cd nava-fp8-comfyui-wrapper
   ```
2. Installa le dipendenze:
   ```bash
   python3 -m pip install --user --break-system-packages -r requirements.txt
   ```
3. (Opzionale) Crea un ambiente virtuale:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --break-system-packages -r requirements.txt
   ```

## Uso
### Come libreria
```python
from src.wrapper_fp8 import WrapperFP8
import os

# Carica configurazione da ambiente (o passa dizionario)
wrapper = WrapperFP8()

if wrapper.is_fp8_enabled():
    # Converte in variabili d'ambiente per subprocess
    env_vars = wrapper.to_env_dict()
    os.environ.update(env_vars)
    # Avvia ComfyUI con impostazioni FP8
    # Esempio: subprocess.Popen([...], env=env_vars)
```

### Script di test manuale
Vedere `scripts/run_manual_test.sh` per un esempio completo di configurazione e test FP8.

## Esempi
1. Imposta variabili d'ambiente FP8:
   ```bash
   export FP8_ENABLED=true
   export FP8_FORMAT=e4m3
   export FP8_COMPUTE_TYPE=bf16
   ```
2. Avvia ComfyUI:
   ```bash
   python3 -m comfyui.execution --listen --port 8188
   ```
3. Verifica l'uso FP8 tramite log di ComfyUI o strumenti di monitoraggio.

## Stato
✅ COMPLETATO — 2026-06-10
- Fase 2/5: Skeleton wrapper Python completata
- Fase 3/5: Definizione dipendenze completata
- Fase 4/5: README e script di test manuale completati
- Fase 5/5: Documentazione permanente e vault completata (questa voce)

## Licenza
MIT