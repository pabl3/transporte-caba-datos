import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar archivo CSV
df = pd.read_csv('C:\\Users\\pabli\\OneDrive\\Desktop\\transporte-caba-datos\\data\\dataset_viajes_sube.csv',
                 header=0,
                 names=['TIPO_TRANSPORTE', 'DIA', 'PARCIAL', 'CANTIDAD'],
                 usecols=['TIPO_TRANSPORTE', 'DIA', 'PARCIAL', 'CANTIDAD']
                )
df.rename(columns={'TIPO_TRANSPORTE': 'tipo_transporte',
                   'DIA': 'fecha',
                   'PARCIAL': 'parcial',
                   'CANTIDAD': 'cantidad'}, inplace=True)

# Convertir tipos
df['fecha'] = pd.to_datetime(df['fecha'], format='%d%b%Y:%H:%M:%S', errors='coerce')
df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')

print("\nDEBUG: Información del DataFrame después de la conversión de tipos:")
print(df.info())
print("DEBUG: Conteo de valores nulos después de la conversión (esperamos 0 para 'fecha' si todo fue bien):")
print(df.isnull().sum())

# Filtrar datos completos
initial_rows = len(df)
df.dropna(subset=['fecha'], inplace=True)
print(f"\nDEBUG: Filas eliminadas por NaT en 'fecha': {initial_rows - len(df)}")

df.drop_duplicates(inplace=True)
print(f"DEBUG: Filas después de drop_duplicates: {len(df)}")


# Estadísticas básicas
if not df.empty:
    print("\nDEBUG: DataFrame NO está vacío. Procediendo con las estadísticas y gráficos.")
    print("\n--- Suma de 'cantidad' por 'tipo_transporte' ---")
    print(df.groupby('tipo_transporte')['cantidad'].sum())

    df['mes'] = df['fecha'].dt.to_period('M')
    print("\n--- Suma de 'cantidad' por 'mes' ---")
    print(df.groupby('mes')['cantidad'].sum())

    # Visualización por mes
    viajes_mensuales = df.groupby('mes')['cantidad'].sum()

    plt.figure(figsize=(12, 6))
    viajes_mensuales.plot(kind='bar', color='skyblue', title='Viajes mensuales con SUBE')
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de viajes")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    screenshots_dir = 'C:\\Users\\pabli\\OneDrive\\Desktop\\transporte-caba-datos\\screenshots\\'
    os.makedirs(screenshots_dir, exist_ok=True)
    plt.savefig(os.path.join(screenshots_dir, 'viajes_mensuales.png'))
    plt.close()

    # Exportar Excel limpio
    df = df.drop(columns=['mes'])
    excel_output_path = 'C:\\Users\\pabli\\OneDrive\\Desktop\\transporte-caba-datos\\data\\viajes_limpios.xlsx'
    df.to_excel(excel_output_path, index=False)
    print("\nProceso completado: DataFrame no vacío, estadísticas, gráfico y exportación realizados.")
