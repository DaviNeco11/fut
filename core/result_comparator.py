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

def compare_issues(expected_issues, actual_issues):
    """
    Compara listas de issues esperadas e atuais.
    """
    normalized_expected = [normalize_issue(issue) for issue in expected_issues]
    normalized_actual = [normalize_issue(issue) for issue in actual_issues]

    return normalized_expected == normalized_actual

def compare_results(test_case):
    if test_case.result_path is None:
        print(f"Nenhum resultado encontrado para o teste {test_case.name}.")
        return False

    expected_data = test_case.load_expected()
    actual_data = load_json(test_case.result_path)

    expected_issues = expected_data.get("issue", [])
    actual_issues = actual_data.get("issue", [])

    is_equal = compare_issues(expected_issues, actual_issues)

    if not is_equal:
        print(f"Diferenças encontradas no teste {test_case.name}:")
        print("Esperado:", json.dumps(expected_issues, indent=2, ensure_ascii=False))
        print("Obtido:", json.dumps(actual_issues, indent=2, ensure_ascii=False))

    return is_equal
