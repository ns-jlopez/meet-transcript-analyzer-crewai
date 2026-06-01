import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


_REQUIRED_AWS_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]

_PRICING = {
    "claude-sonnet-4": {"input": 3.00, "output": 15.00, "cached_input": 0.30},
    "claude-haiku-4":  {"input": 0.80, "output": 4.00,  "cached_input": 0.08},
    "claude-opus-4":   {"input": 15.00, "output": 75.00, "cached_input": 1.50},
}


def _validate_aws_env():
    missing = [v for v in _REQUIRED_AWS_VARS if not os.environ.get(v)]
    if missing:
        print(f"Error: missing required environment variable(s): {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def _print_cost(usage, model_name):
    prices = _PRICING["claude-sonnet-4"]
    model = (model_name or "").lower()
    for key, p in _PRICING.items():
        if key in model:
            prices = p
            break

    uncached_input = usage.prompt_tokens - usage.cached_prompt_tokens
    input_cost = (uncached_input / 1_000_000) * prices["input"]
    cached_cost = (usage.cached_prompt_tokens / 1_000_000) * prices["cached_input"]
    output_cost = (usage.completion_tokens / 1_000_000) * prices["output"]
    total_cost = input_cost + cached_cost + output_cost

    print("\n--- Token Usage ---")
    print(usage)
    print("\n--- Estimated Cost ---")
    print(f"Input:  {uncached_input:,} tokens × ${prices['input']:.2f}/M = ${input_cost:.4f}")
    if usage.cached_prompt_tokens:
        print(f"Cached: {usage.cached_prompt_tokens:,} tokens × ${prices['cached_input']:.2f}/M = ${cached_cost:.4f}")
    print(f"Output: {usage.completion_tokens:,} tokens × ${prices['output']:.2f}/M = ${output_cost:.4f}")
    print(f"Total:  ${total_cost:.4f}")


def _write_report(result):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"report_{timestamp}.md"
    report_path.write_text(result.raw)
    print(f"\nReport written to: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Analyze a Google Meet transcript for language improvement.")
    parser.add_argument(
        "--folder",
        default=os.environ.get("GOOGLE_DRIVE_FOLDER_NAME", "Meet Recordings"),
        help="Google Drive folder name to search for transcripts (default: 'Meet Recordings')",
    )
    parser.add_argument(
        "--file",
        help="Path to a local transcript file (skips Google Drive)",
    )
    parser.add_argument(
        "--provider",
        default="bedrock",
        choices=["bedrock", "anthropic", "openai"],
        help="LLM provider (default: bedrock)",
    )
    parser.add_argument(
        "--model",
        help="Override the LLM model ID",
    )
    args = parser.parse_args()

    _validate_aws_env()

    if args.file:
        transcript = Path(args.file).read_text(encoding="utf-8")
        print(f"Using local transcript: {args.file} ({len(transcript):,} chars)")
    else:
        from meet_analyzer.drive.auth import get_credentials
        from meet_analyzer.drive.fetch import fetch_latest_transcript
        credentials = get_credentials()
        transcript = fetch_latest_transcript(args.folder, credentials)

    from meet_analyzer.crew.crew import TranscriptAnalyzerCrew
    analyzer = TranscriptAnalyzerCrew(transcript, llm_provider=args.provider, llm_model=args.model)
    result = analyzer.run()

    _write_report(result)

    if hasattr(result, "token_usage") and result.token_usage:
        model_name = args.model or ""
        _print_cost(result.token_usage, model_name)


if __name__ == "__main__":
    main()
