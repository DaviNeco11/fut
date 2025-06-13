import json
from datetime import datetime
from pathlib import Path

def generate_report(test_results, output_path="outputs/report.json"):
    """
    Gera um relatório detalhado em formato JSON com estatísticas e detalhes dos testes.
    test_results: lista de dicts, cada um com:
        - name
        - description (opcional)
        - context (opcional)
        - input_path
        - expected_path
        - result_path
        - exec_time
        - expected_data
        - actual_data
        - differences (lista de strings)
        - status ("passed", "failed", "warning")
        - raw_output (opcional)
    """
    summary = {
        "total_tests": len(test_results),
        "passed": sum(1 for t in test_results if t["status"] == "passed"),
        "failed": sum(1 for t in test_results if t["status"] == "failed"),
        "warnings": sum(1 for t in test_results if t["status"] == "warning"),
        "start_time": datetime.now().isoformat(),
        "total_time_sec": sum(t.get("exec_time", 0) for t in test_results),
        "tests": []
    }

    for t in test_results:
        # Format OperationOutcome issues as table rows
        def extract_issues(data):
            return [
                {
                    "diagnostics": issue.get("details", {}).get("text", ""),
                    "location": ", ".join(issue.get("expression", [])) if issue.get("expression") else "",
                    "severity": issue.get("severity", "")
                }
                for issue in data.get("issue", [])
            ] if data else []

        summary["tests"].append({
            "test_id": t["name"],
            "description": t.get("description", ""),
            "context": t.get("context", ""),
            "input_instance": t.get("input_instance"),  # formatted JSON string
            "expected_results": extract_issues(t.get("expected_data")),
            "obtained_results": extract_issues(t.get("actual_data")),
            "differences": t.get("differences", []),
            "status": t["status"],
            "exec_time_sec": t.get("exec_time", 0),
            "raw_validator_output": t.get("raw_output", None)
        })

    # Optionally, add chart data (for frontend rendering)
    summary["charts"] = {
        "status_counts": {
            "passed": summary["passed"],
            "failed": summary["failed"],
            "warnings": summary["warnings"]
        },
        "exec_times": [
            {"test_id": t["name"], "exec_time_sec": t.get("exec_time", 0)}
            for t in test_results
        ]
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Relatório salvo em: {output_path}")