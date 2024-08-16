# ------------------------------------------------------------------------------------------------------------
#   En el DAW cargar Referencia y Crudo. Normalizar Crudo y aplicar misma ganancia a Referencia.

#   En el DAW grabar la señal cruda normalizada con Bypass del audífono corroborando que en 
# Output Level de Sound Designer el nivel SPL sea coherente. El nivel de entrada en el DAW no es
# importante. Minimizar ruido eléctrico y no permitir recortes 

#   Normalizar la señal del Bypass y ver la de ganancia (G1)

#   Grabar la señal cruda normalizada a travéz del proceso del audífono y aplicar la ganancia anterior G1

#   Como el proceso del audifono incluye mucha ganancia, la señal procesada clipea. Por lo tanto hay que
# atenuar todas señales (Ref, Crudo, Bypass y proceso) con la misma ganancia G2. Para ello se puede 
# normalizar con ganancia común.
 
#   Exportar la referencia, la señal cruda y la señal procesada con las ganancias resultantes

#   Cargar las 3 en la carpeta del proyecto
# ------------------------------------------------------------------------------------------------------------

from clarity.evaluator.haspi import haspi_v2 as haspi
from clarity.utils.audiogram import Audiogram
from clarity.utils import signal_processing
from clarity.data import demo_data

import numpy as np
import librosa as lib
import os

SR = 24000

# os.system("cls")

# Descargar dataset
# demo_data.get_scenes_demo()
# demo_data.get_metadata_demo()

# Audiograma
hearing_loss = Audiogram([20, 30, 40, 40, 50, 50], [250, 500, 1000, 2000, 4000, 6000])

print("\tAUDIOGRAMA:")
print(*hearing_loss.frequencies, sep =' Hz\t', end=' Hz\n')
print(*hearing_loss.levels, sep =' dBHL\t', end=' dBHL\n')

N = "010" 
tar_sig1, _ = lib.load(path=f"Ezairo/Referencia{N}.wav", sr=SR, mono=True)
mix_sig1, _ = lib.load(path=f"Ezairo/Crudo{N}.wav", sr=SR, mono=True)
enh_sig1, _ = lib.load(path=f"Ezairo/Modo2{N}.wav", sr=SR, mono=True)

# La señal de referencia debe tener un RMS = 1
# Hay que amplificar la señal con ganancia...
gain1 = 1/signal_processing.compute_rms(tar_sig1)

# Aplicar misma ganancia para todas las señales
tar_sig1 *= gain1
mix_sig1 *= gain1
enh_sig1 *= gain1

# Calculo HASPI
print("\n\tHASPI: Hearing Aid Speech Inteligibility Index")
sii_orig, _ = haspi(reference=tar_sig1,
                        reference_sample_rate=SR,
                        processed=mix_sig1,
                        processed_sample_rate=SR,
                        audiogram=hearing_loss,
                        level1=65)
print(f"Inteligibilidad Original = {sii_orig}")

sii_proc, _ = haspi(reference=tar_sig1,
                        reference_sample_rate=SR,
                        processed=enh_sig1,
                        processed_sample_rate=SR,
                        audiogram=hearing_loss,
                        level1=65)
print(f"Inteligibilidad Mejorada = {sii_proc}")

mejora = sii_proc - sii_orig
print(f"Mejora del procesamiento = {mejora}")