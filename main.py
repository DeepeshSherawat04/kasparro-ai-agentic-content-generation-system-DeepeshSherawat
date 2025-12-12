# main.py
from orchestrator.pipeline import PipelineOrchestrator

def main():
    """
    Run the LangChain + Ollama pipeline.
    """
    PipelineOrchestrator().run()

if __name__ == "__main__":
    main()
