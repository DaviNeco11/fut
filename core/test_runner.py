import subprocess
from pathlib import Path
from core.result_comparator import compare_results

def run_validator(test_case, validator_path, fhir_version="4.0.1", output_dir="outputs"):
    """
    Executa o validador FHIR e compara o resultado com o esperado.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{test_case.name}_result.json"
    command = [
        "java",
        "-jar", str(validator_path),
        "-version", fhir_version,
        "-output", str(output_path),
        str(test_case.input_path)
    ]

    try:
        subprocess.run(command, check=True)
        test_case.result_path = output_path

        print(f"✅ Validação executada para {test_case.name}")
        
        # Comparar o resultado com o esperado
       # if compare_results(test_case):
        #    print(f"Resultado esperado confirmado para {test_case.name}\n")
        #else:
         #   print(f"Resultado diferente do esperado para {test_case.name}\n")

        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o validador para {test_case.name}: {e}")
        return None
