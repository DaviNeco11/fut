import json

def compare_results(expected_path, result_path):
    with open(expected_path, 'r', encoding='utf-8') as f:
        expected = json.load(f)

    with open(result_path, 'r', encoding='utf-8') as f:
        actual = json.load(f)

    # Verifica se a estrutura do resultado contém issues
    if actual.get("resourceType") != "OperationOutcome":
        return False, ["Resultado inválido: resourceType não é OperationOutcome"]

    actual_issues = actual.get("issue", [])
    expected_issues = expected.get("issues", [])
    expected_status = expected.get("status", "pass")

    messages = []

    if expected_status == "pass" and actual_issues:
        messages.append("Esperado sucesso, mas foram encontrados problemas na validação.")
        return False, messages

    if expected_status == "fail":
        for expected_issue in expected_issues:
            match = any(
                expected_issue["severity"] == issue.get("severity") and
                expected_issue["diagnostics"] in issue.get("diagnostics", "")
                for issue in actual_issues
            )
            if not match:
                messages.append(f"Issue esperada não encontrada: {expected_issue}")
        if messages:
            return False, messages

    return True, ["Validação bem-sucedida e compatível com o esperado."]
