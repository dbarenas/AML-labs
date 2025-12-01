# AML-labs

Colección de demos autocontenidas para escenarios de AML con generación de datos sintéticos, modelos ligeros inspirados en PyOD/NetworkX y pruebas automatizadas. Todo el código está en español y respeta los principios SOLID mediante clases con responsabilidades claras.

## Estructura

- `data/aml_data.csv`: dataset sintético de transacciones con una pequeña fracción etiquetada como sospechosa.
- `data/transactions_data.json`: lista de transacciones dirigidas que incluye un anillo de fraude simulado (A901 ⇄ A902 ⇄ A903).
- `pyod_demo/`: caso de detección de pitufeo usando un Isolation Forest ligero.
  - `data_generator.py`: crea el CSV de entrenamiento.
  - `feature_engineering.py`: repositorio, cálculo de *features* y servicio de orquestación.
  - `models.py`: modelos Pydantic simplificados para transacciones y *features*.
  - `demo_pyod.py`: script demostrativo.
  - `test_pyod.py`: prueba unitaria.
- `networkx_demo/`: detección de anillos de fraude con grafos dirigidos.
  - `models.py`: modelo Pydantic para aristas.
  - `demo_networkx.py`: script demostrativo.
  - `test_networkx.py`: prueba unitaria.
- `pydantic/`, `pyod/`, `networkx/`: implementaciones ligeras incluidas en el repositorio para evitar dependencias externas en entornos sin acceso a internet.

## Cómo ejecutar las demos

1. **Detección de pitufeo (PyOD):**
   ```bash
   python pyod_demo/demo_pyod.py
   ```
   Imprime las 10 cuentas con mayor puntuación de anomalía calculadas a partir de `TxCount_30D` y `AvgAmount_30D`.

2. **Anillo de fraude (NetworkX):**
   ```bash
   python networkx_demo/demo_networkx.py
   ```
   Muestra la centralidad de intermediación de cada nodo y lista todos los componentes fuertemente conectados.

## Pruebas unitarias

Ejecuta todo el set de pruebas con:
```bash
python -m unittest discover
```

### Explicación de los casos de prueba

- `test_pyod.py`: valida que al menos el 70% de las cuentas que contienen transacciones etiquetadas como `IsSuspicious=True` queden dentro del 5% superior de puntuaciones de anomalía. Esto asegura que el modelo (Isolation Forest ligero) está capturando el patrón de muchas transacciones pequeñas.
- `test_networkx.py`: construye el grafo dirigido a partir de `transactions_data.json` y comprueba que el conjunto {A901, A902, A903} aparece exactamente como un componente fuertemente conectado, validando la detección del anillo de fraude.

## Notas sobre dependencias

El repositorio incluye implementaciones mínimas de `pydantic`, `pyod` e `networkx` para garantizar reproducibilidad en entornos sin acceso a instalación de paquetes. No es necesario instalar dependencias adicionales.
