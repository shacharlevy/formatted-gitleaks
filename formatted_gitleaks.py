import sys
import subprocess
import json
from pydantic import BaseModel


class Finding(BaseModel):
    filename: str
    line_range: str
    description: str


class GitleaksOutput(BaseModel):
    findings: list[Finding]


class ErrorOutput(BaseModel):
    exit_code: int
    error_message: str


class FormattedGitleaksException(Exception):

    def __init__(self, exit_code, message):
        self.exit_code = exit_code
        self.message = message
        super().__init__(message)


def write_error(exit_code, error_message, output_path="/code/output.json.json"):
    error_data = ErrorOutput(exit_code=exit_code, error_message=error_message)
    with open(output_path, 'w') as f:
        f.write(error_data.model_dump_json(indent=2))


def run_gitleaks(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # exit code 1 indicates leaks were found, not a failure
        if e.returncode == 1:
            return
        raise FormattedGitleaksException(
            exit_code=e.returncode,
            message=f"Gitleaks scan failed: {e.stderr or 'Unknown error'}"
        )
    except Exception as e:
        raise FormattedGitleaksException(exit_code=2, message=f"Gitleaks scan failed: {str(e)}")


def parse_gitleaks_output(report_path):
    try:
        with open(report_path, 'r') as f:
            results = json.load(f)

        findings = [
            Finding(
                filename=result.get('File', ''),
                line_range=f"{result.get('StartLine', '')}-{result.get('EndLine', '')}",
                description=result.get('Description', '')
            )
            for result in results
        ]

        return GitleaksOutput(findings=findings)

    except FileNotFoundError:
        raise FormattedGitleaksException(exit_code=2, message=f"Report file not found at {report_path}")
    except json.JSONDecodeError:
        raise FormattedGitleaksException(exit_code=2, message=f"Failed to parse JSON from {report_path}")


def main():
    if len(sys.argv) < 2:
        write_error(2, "Usage: python gitleaks_wrapper.py <command>")
        return

    command = ' '.join(sys.argv[1:])
    try:
        report_path_ind = sys.argv.index('--report-path')
        try:
            report_path = sys.argv[report_path_ind + 1]
        except IndexError:
            write_error(
                exit_code=1,
                error_message="'--report-path' specified but no path provided."
            )
    except ValueError:
        report_path = "/code/output.json"
        command += f' --report-path {report_path}'

    try:
        run_gitleaks(command)
        output = parse_gitleaks_output(report_path)
        print(output.model_dump_json(indent=2))
    except FormattedGitleaksException as e:
        write_error(e.exit_code, e.message, report_path)


if __name__ == "__main__":
    main()
