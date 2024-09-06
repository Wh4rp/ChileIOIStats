import pandas as pd
from bs4 import BeautifulSoup
import requests

def main():
    url = "https://stats.ioinformatics.org/results/CHL"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todas las tablas en la página
    tables = soup.find_all('table')

    # Asumiendo que queremos la primera tabla encontrada
    table = tables[0]

    # Extrae datos de la tabla
    data = []
    headers = ['Year', 'Contestant', 'Country', 'Task1', 'Task2', 'Task3', 'Task4', 'Task5', 'Task6', 'Score Abs.', 'Score Rel.', 'Rank Abs.', 'Rank Rel.', 'Award']

    current_year = -1

    # Extrae filas
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if cols:
            cols_striped = [col.text.strip() for col in cols]
            # Arreglamos bug con los años
            if cols_striped[0].isnumeric():
                current_year = cols_striped[0]
            else:
                cols_striped = [current_year] + cols_striped[:-1]
            data.append(cols_striped)


    # Convierte a pandas DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Guarda en un archivo CSV
    df.to_csv('resultados_chile.csv', index=False)

    print("Tabla convertida y guardada como 'resultados_chile.csv'")


if __name__ == "__main__":
    main()
