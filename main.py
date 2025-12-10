from orchestrator.pipeline import PipelineOrchestrator

def main():
    """
    This is the Entry point for running the entire pipeline.
    Keeping this simple ensures all workflow logic stays in the orchestrator.
    """
    PipelineOrchestrator().run()


if __name__ == "__main__":
    main()
