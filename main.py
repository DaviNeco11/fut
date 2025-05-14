from core.test_case import TestCase
from core.test_runner import run_validator
from core.result_comparator import compare_results
from pathlib import Path
import shutil

def main():
    # Caminhos dos arquivos
    input_path = "tests/suite1/test1.json"
    expected_path = "tests/suite1/test1_expected.json"
    validator_path = "validator_cli.jar"

    # Criar instância do caso de teste
    test_case = TestCase(name="test1", input_path=input_path, expected_path=expected_path)

    # Executar validador
    print(f"🚀 Executando o teste: {test_case.name}")
    result_path = run_validator(test_case, validator_path)

    if result_path:
        print(f"✅ Resultado salvo em: {result_path}")

        # Se o expected ainda não existir, criamos com base no primeiro resultado
        if not Path(expected_path).exists():
            shutil.copy(result_path, expected_path)
            print(f"📄 Arquivo esperado criado automaticamente: {expected_path}")
        else:
            # Comparar resultado com o esperado
            passed, messages = compare_results(expected_path, result_path)
            status = "✅ TESTE APROVADO" if passed else "❌ TESTE FALHOU"
            print(f"\n📊 Resultado da comparação: {status}")
            for msg in messages:
                print(f" - {msg}")

    else:
        print("❌ Falha ao executar o validador.")

if __name__ == "__main__":
    main()
