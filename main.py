# main.py
"""
Entry point for the Multi-Agent Content Generation System.
Run with: python main.py
"""

from orchestrator.pipeline import PipelineOrchestrator


def main():
    """Main entry point."""
    orchestrator = PipelineOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()