"""Example usage for MultiAgentDebateConsensusSynthesizer."""
import json
from client import MultiAgentDebateConsensusSynthesizer

def main():
    print("=== Multi-Agent Debate & Consensus Demo ===")
    debate = MultiAgentDebateConsensusSynthesizer()
    
    topic = "Deploy automated email outreach campaign without human pre-review"
    personas = ["RiskAuditor", "SpeedOptimizer", "UserAdvocate", "SystemsArchitect"]
    
    res = debate.orchestrate_debate(topic=topic, personas=personas, rounds=2)
    print("Debate Rounds Executed:", res["rounds_executed"])
    print("Convergence Level:", res["convergence"]["convergence_level"])
    print("Final Verdict:", json.dumps(res["consensus_verdict"], indent=2))

if __name__ == "__main__":
    main()
