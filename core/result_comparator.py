# Compara resultados obtidos vs esperados
import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_issue(issue):
    """
    Normaliza os campos principais do 'issue' para facilitar a comparação.
    Ignora campos como 'extension' e 'valueString' que podem mudar sem afetar a semântica.
    """
    return {
        "severity": issue.get("severity"),
        "code": issue.get("code"),
        "details": issue.get("details", {}).get("text"),
        "expression": issue.get("expression")
    }

def compare_results(expected_data, actual_data):
    """
    Retorna differences para relatório detalhado.
    """
    expected_issues = expected_data.get("issue", []) if expected_data else []
    actual_issues = actual_data.get("issue", []) if actual_data else []

    normalized_expected = [normalize_issue(issue) for issue in expected_issues]
    normalized_actual = [normalize_issue(issue) for issue in actual_issues]

    differences = []
    if normalized_expected != normalized_actual:
        differences.append("Issues diferentes entre esperado e obtido.")
        differences.append("Esperado: " + json.dumps(normalized_expected, ensure_ascii=False, indent=2))
        differences.append("Obtido: " + json.dumps(normalized_actual, ensure_ascii=False, indent=2))

    return differences
