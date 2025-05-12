from core.test_runner import run_validator
from core.parser import carregar_casos_teste
from pathlib import Path
import shutil

def main():
    validator_path = "validator_cli.jar"
    yaml_path = Path(__file__).parent / "tests" / "suite1" / "testes.yaml"

    casos = carregar_casos_teste(yaml_path)

    total = len(casos)
    passed = 0
    failed = 0

    for caso in casos:
        print(f"\n Executando teste: {caso.name}")
        print(f" Entrada: {caso.input_path}")
        print(f" Espera erros? {'Sim' if getattr(caso, 'espera_erros', False) else 'Não'}")

        result_path = run_validator(caso, validator_path)

        if result_path:
            print(f" Resultado salvo em: {result_path}")
            if not caso.expected_path.exists():
                shutil.copy(result_path, caso.expected_path)
                print(f"Esperado criado: {caso.expected_path}")
                passed += 1  # Consideramos como aprovado se for a primeira geração
            else:
                # Resultado já foi comparado dentro de run_validator
                if caso.result_path:  # se for diferente de None, foi gerado e comparado
                    with open(caso.result_path, encoding='utf-8') as f:
                        resultado = f.read()
                        if "OperationOutcome" in resultado:
                            passed += 1
                        else:
                            failed += 1
                else:
                    failed += 1
        else:
            print(f"Falha na execução do validador para: {caso.name}")
            failed += 1

    print("\nRESUMO FINAL")
    print(f"Testes passados: {passed}")
    print(f"Testes falhados: {failed}")
    print(f"Total executado: {total}")

if __name__ == "__main__":
    main()
