from core.test_runner import run_validator
from core.parser import carregar_casos_teste
from pathlib import Path
import shutil

def main():
    validator_path = "validator_cli.jar"
    yaml_path = Path(__file__).parent / "tests" / "suite1" / "testes.yaml"
    
    casos = carregar_casos_teste(yaml_path)

    for caso in casos:
        print(f"\n Executando teste: {caso.name}")
        print(f" Entrada: {caso.input_path}")
        print(f" Espera erros? {'Sim' if getattr(caso, 'espera_erros', False) else 'Não'}")

        result_path = run_validator(caso, validator_path)

        if result_path:
            print(f" Resultado salvo em: {result_path}")
            if not caso.expected_path.exists():
                shutil.copy(result_path, caso.expected_path)
                print(f"[INFO] Esperado criado: {caso.expected_path}")
            else:
                print(f"[INFO] Esperado já existe: {caso.expected_path}")
        else:
            print(f" Falha na execução do validador para: {caso.name}")

if __name__ == "__main__":
    main()
