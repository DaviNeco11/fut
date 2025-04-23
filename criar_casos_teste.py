import os
import json

def criar_caso_teste(base_dir, nome_caso, input_data, expected_data):
    caso_path = os.path.join(base_dir, nome_caso)
    os.makedirs(caso_path, exist_ok=True)

    with open(os.path.join(caso_path, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_data, f, indent=2)

    with open(os.path.join(caso_path, "expected.json"), "w", encoding="utf-8") as f:
        json.dump(expected_data, f, indent=2)

    print(f"\n✅ Caso de teste '{nome_caso}' criado com sucesso em '{caso_path}'.")

def main():
    print(" Criador de Casos de Teste FHIR")

    base = input("Digite o caminho da pasta base (ex: tests/suite1): ").strip()
    nome = input("Nome do caso de teste (ex: test_case_05): ").strip()

    print("\n Criando input.json")
    resource_type = input("resourceType (ex: Patient): ").strip()
    patient_id = input("id do paciente: ").strip()
    family_name = input("Sobrenome: ").strip()
    given_name = input("Nome(s): ").strip()

    input_data = {
        "resourceType": resource_type,
        "id": patient_id,
        "name": [
            {
                "use": "official",
                "family": family_name,
                "given": [given_name]
            }
        ]
    }

    print("\n📋 Criando expected.json")
    status = input("Resultado esperado (pass/fail): ").strip().lower()

    issues = []
    if status == "fail":
        while True:
            severity = input("  Severidade do erro (error/warning): ").strip()
            diagnostics = input("  Mensagem de erro: ").strip()
            issues.append({"severity": severity, "diagnostics": diagnostics})

            more = input("  Adicionar outro erro? (s/n): ").strip().lower()
            if more != 's':
                break

    expected_data = {
        "status": status,
        "issues": issues
    }

    criar_caso_teste(base, nome, input_data, expected_data)

if __name__ == "__main__":
    main()
