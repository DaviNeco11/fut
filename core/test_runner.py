import subprocess
from pathlib import Path
from core.result_comparator import compare_results, load_json
import time

def run_validator(test_case, validator_path, fhir_version="4.0.1", output_dir="outputs"):
    """
    Executa o validador FHIR e compara o resultado com o esperado.
    Retorna um dict com informações detalhadas para o relatório.
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

    start = time.perf_counter()
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=True)
        exec_time = time.perf_counter() - start
        test_case.result_path = output_path

        # Carregar dados esperados e obtidos
        expected_data = None
        if test_case.expected_path.exists():
            expected_data = load_json(test_case.expected_path)
        actual_data = load_json(test_case.result_path)

        # Diferenças e status
        differences = compare_results(expected_data, actual_data)
        passed = len(differences) == 0
        status = "passed" if passed else "failed"

        # Instância de entrada formatada
        try:
            with open(test_case.input_path, encoding="utf-8") as f:
                input_instance = f.read()
        except Exception:
            input_instance = None

        result = {
            "name": test_case.name,
            "description": getattr(test_case, "description", ""),
            "context": getattr(test_case, "context", ""),
            "input_instance": input_instance,
            "expected_data": expected_data,
            "actual_data": actual_data,
            "differences": differences,
            "status": status,
            "exec_time": exec_time,
            "raw_output": proc.stdout + proc.stderr
        }

        print(f"✅ Validação executada para {test_case.name}")
        if passed:
            print(f"Resultado esperado confirmado para {test_case.name}\n")
        else:
            print(f"Resultado diferente do esperado para {test_case.name}\n")

        return output_path, result
    except subprocess.CalledProcessError as e:
        exec_time = time.perf_counter() - start
        print(f"Erro ao executar o validador para {test_case.name}: {e}")
        return None, {
            "name": test_case.name,
            "description": getattr(test_case, "description", ""),
            "context": getattr(test_case, "context", ""),
            "input_instance": None,
            "expected_data": None,
            "actual_data": None,
            "differences": [str(e)],
            "status": "failed",
            "exec_time": exec_time,
            "raw_output": getattr(e, "output", "")
        }