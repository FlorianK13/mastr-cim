from linkml_map.session import Session
import pandas as pd
import yaml
from open_mastr import Mastr


def get_mastr():
    """Get the raw data from the Marktstammdatenregister (short: MaStR) 
    using a previously downloaded database (downloaded with MaStR.download())"""
    db = Mastr()
    df = pd.read_sql('''
    SELECT
        EinheitMastrNummer,
        NameWindpark,
        Nettonennleistung,
        CAST(Hersteller AS VARCHAR(255)) AS Hersteller,
        Typenbezeichnung,
        Laengengrad,
        Breitengrad
    FROM wind_extended
    WHERE NameWindpark     IS NOT NULL
    AND Hersteller       IS NOT NULL
    AND Typenbezeichnung IS NOT NULL
    AND Laengengrad      IS NOT NULL
    AND Breitengrad      IS NOT NULL
    ;
    ''', con=db.engine)
    df["Laengengrad"] = df["Laengengrad"].astype(float)
    df["Breitengrad"] = df["Breitengrad"].astype(float)
    print(len(df))
    return df.to_dict(orient="records")

def map_to_cim(mastr_dict):

    session = Session()
    with open('schema/mastr.yml', 'r') as f:
        source_schema = yaml.load(f, Loader=yaml.SafeLoader)

    session.set_source_schema(source_schema)

    with open('schema/map.yml', 'r') as f:
        map_str = yaml.load(f, Loader=yaml.SafeLoader)
    session.set_object_transformer(map_str)


    transformed = []
    for index, obj in enumerate(mastr_dict):
        transformed.append(session.transform(obj, source_type="wind_extended"))
        if index%1000==0:
            print(index)
    return transformed





def main():
    mastr_dict = get_mastr()
    transformed = map_to_cim(mastr_dict)
    df_transformed = pd.DataFrame(transformed).set_index('mRID')
    df_transformed.to_csv("WindGeneratingUnits.csv")


if __name__ == "__main__":
    main()