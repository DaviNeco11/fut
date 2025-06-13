from core.test_runner import run_validator
from core.parser import carregar_casos_teste
from core.report_generator import generate_report
from pathlib import Path
import shutil
import subprocess
import sys

def main():
    validator_path = "validator_cli.jar"
    yaml_path = Path(__file__).parent / "tests" / "suite1" / "testes.yaml"

    casos = carregar_casos_teste(yaml_path)

    total = len(casos)
    passed = 0
    failed = 0
    test_results = []

    for caso in casos:
        print(f"\n🔍 Executando teste: {caso.name}")
        print(f"📥 Entrada: {caso.input_path}")
        print(f"❓ Espera erros? {'Sim' if getattr(caso, 'espera_erros', False) else 'Não'}")

        result_path, result_info = run_validator(caso, validator_path)
        test_results.append(result_info)

        if result_path:
            print(f"📤 Resultado salvo em: {result_path}")
            if not caso.expected_path.exists():
                shutil.copy(result_path, caso.expected_path)
                print(f"[🆕] Esperado criado: {caso.expected_path}")
                passed += 1  # Consideramos como aprovado se for a primeira geração
            else:
                if result_info["status"] == "passed":
                    passed += 1
                else:
                    failed += 1
        else:
            print(f"❌ Falha na execução do validador para: {caso.name}")
            failed += 1

    print("\n📊 RESUMO FINAL")
    print(f"✔️ Testes passados: {passed}")
    print(f"❌ Testes falhados: {failed}")
    print(f"🔢 Total executado: {total}")

    # Gera o relatório JSON detalhado
    generate_report(test_results, output_path="outputs/report.json")
    
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "core/report_display_streamlit.py"],
        cwd=Path(__file__).parent
    )

if __name__ == "__main__":
    main()