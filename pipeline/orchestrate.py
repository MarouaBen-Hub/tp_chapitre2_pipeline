from dagster import job, op
import os

@op
def ingest():
    # Exécute le script d'ingestion Python
    return_code = os.system("python pipeline/ingest.py")
    if return_code != 0:
        raise Exception("L'étape d'ingestion a échoué.")

@op
def validate(ingest_result):
    # Exécute le script de validation minimale
    return_code = os.system("python pipeline/validate.py")
    if return_code != 0:
        raise Exception("L'étape de validation a échoué.")

@op
def transform(validate_result):
    # Se déplace dans le dossier dbt et lance la transformation
    return_code = os.system("cd dbt_pipeline && dbt run --profiles-dir .")
    if return_code != 0:
        raise Exception("La transformation dbt a échoué.")

@op
def test_data(transform_result):
    # Lance les tests de qualité dbt
    return_code = os.system("cd dbt_pipeline && dbt test --profiles-dir .")
    if return_code != 0:
        raise Exception("Les tests dbt ont échoué.")

@job
def ventes_pipeline():
    # Définition de l'ordre d'exécution (la dépendance des tâches)
    test_data(transform(validate(ingest())))
