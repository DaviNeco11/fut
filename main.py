from core.test_runner import run_validator
from core.parser import carregar_casos_teste
from core.report_generator import generate_report
from pathlib import Path
import shutil
import subprocess
import sys

def executar_todos(casos, validator_path):
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
                passed += 1
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
    print(f"🔢 Total executado: {len(casos)}")

    generate_report(test_results, output_path="outputs/report.json")

    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "core/report_display_streamlit.py"],
        cwd=Path(__file__).parent
    )

def listar_testes(casos):
    print("\n📋 Lista de testes disponíveis:")
    for i, caso in enumerate(casos, start=1):
        print(f"{i}. {caso.name}")

def executar_teste_especifico(casos, validator_path):
    listar_testes(casos)
    nome = input("\nDigite o nome exato do teste que deseja executar: ")
    encontrado = next((caso for caso in casos if caso.name == nome), None)

    if not encontrado:
        print("❌ Teste não encontrado!")
        return

    print(f"\n🔍 Executando teste: {encontrado.name}")
    result_path, result_info = run_validator(encontrado, validator_path)
    if result_path:
        print(f"📤 Resultado salvo em: {result_path}")
    else:
        print("❌ Falha ao executar o teste.")
    
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "core/report_display_streamlit.py"],
        cwd=Path(__file__).parent
    )

def main():
    validator_path = "validator_cli.jar"
    yaml_path = Path(__file__).parent / "tests" / "suite1" / "testes.yaml"
    casos = carregar_casos_teste(yaml_path)

    while True:
        print("\n===== MENU =====")
        print("1. Executar todos os testes")
        print("2. Listar todos os testes")
        print("3. Executar um teste específico")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            executar_todos(casos, validator_path)
        elif opcao == "2":
            listar_testes(casos)
        elif opcao == "3":
            executar_teste_especifico(casos, validator_path)
        elif opcao == "0":
            print("👋 Encerrando o programa.")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
