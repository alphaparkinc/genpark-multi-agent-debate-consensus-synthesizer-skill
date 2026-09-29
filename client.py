"""Client module for MultiAgentDebateConsensusSynthesizer (100% Python Standard Library)."""
import json
import time
import math
from typing import Dict, Any, List, Optional

class MultiAgentDebateConsensusSynthesizer:
    """Orchestrates structured debate rounds across distinct agent personas,
    evaluating argument convergence, trade-offs, and final consensus verdicts."""
    
    DEFAULT_PERSONAS = {
        "RiskAuditor": {
            "perspective": "Identify safety, compliance, failure modes, and catastrophic downside.",
            "bias": "conservative",
            "weight": 1.2
        },
        "SpeedOptimizer": {
            "perspective": "Maximize execution speed, minimize latency, and remove unnecessary friction.",
            "bias": "aggressive",
            "weight": 1.0
        },
        "UserAdvocate": {
            "perspective": "Ensure maximum user delight, intuitive ergonomics, and trust preservation.",
            "bias": "empathic",
            "weight": 1.1
        },
        "SystemsArchitect": {
            "perspective": "Ensure long-term maintainability, modularity, and resource scalability.",
            "bias": "structural",
            "weight": 1.0
        }
    }

    def __init__(self):
        self.debate_history: List[Dict[str, Any]] = []

    def orchestrate_debate(self, topic: str, personas: Optional[List[str]] = None, rounds: int = 2) -> Dict[str, Any]:
        """Runs simulated or structured debate across chosen persona viewpoints."""
        active_persona_names = personas or ["RiskAuditor", "SpeedOptimizer", "UserAdvocate"]
        debate_rounds = []
        
        for r in range(1, rounds + 1):
            round_data = {"round_number": r, "speeches": {}}
            for p_name in active_persona_names:
                meta = self.DEFAULT_PERSONAS.get(p_name, {"perspective": "General evaluation", "bias": "neutral", "weight": 1.0})
                speech = self._generate_persona_position(topic, p_name, meta["bias"], r)
                round_data["speeches"][p_name] = speech
            debate_rounds.append(round_data)
            
        convergence_info = self.evaluate_convergence(debate_rounds[-1]["speeches"])
        verdict = self.synthesize_verdict(topic, debate_rounds[-1]["speeches"], convergence_info)
        
        result = {
            "status": "success",
            "topic": topic,
            "rounds_executed": rounds,
            "personas_involved": active_persona_names,
            "debate_rounds": debate_rounds,
            "convergence": convergence_info,
            "consensus_verdict": verdict
        }
        self.debate_history.append(result)
        return result

    def _generate_persona_position(self, topic: str, persona: str, bias: str, round_num: int) -> Dict[str, Any]:
        """Generates deterministic structured argument points based on persona stance."""
        if bias == "conservative":
            score = 6.5 + (0.5 * round_num)
            stance = "Cautious conditional approval with rigorous fallback triggers."
            risks = ["Unmonitored failure state", "Edge-case budget runaway"]
        elif bias == "aggressive":
            score = 9.0 - (0.3 * round_num)
            stance = "Immediate phased rollout to optimize execution velocity."
            risks = ["Slight initial latency jitter"]
        else:
            score = 8.0
            stance = "Approved provided user is notified with transparent controls."
            risks = ["User confusion if unexplained"]
            
        return {
            "persona": persona,
            "stance_summary": stance,
            "support_score": round(score, 1),
            "primary_concerns": risks,
            "recommended_amendment": f"Add sanity telemetry check for {persona} criteria."
        }

    def evaluate_convergence(self, final_speeches: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates variance and standard deviation of support scores to determine consensus level."""
        scores = [s.get("support_score", 7.0) for s in final_speeches.values()]
        if not scores:
            return {"convergence_level": "unknown", "consensus_score": 0.0}
            
        mean_score = sum(scores) / len(scores)
        variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
        std_dev = math.sqrt(variance)
        
        if std_dev < 1.0:
            level = "high_consensus"
        elif std_dev < 2.0:
            level = "moderate_consensus"
        else:
            level = "divergent_deadlock"
            
        return {
            "mean_support_score": round(mean_score, 2),
            "std_deviation": round(std_dev, 2),
            "convergence_level": level,
            "consensus_reached": std_dev < 2.0
        }

    def synthesize_verdict(self, topic: str, final_speeches: Dict[str, Dict[str, Any]], convergence: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregates all arguments into a balanced, actionable executive resolution."""
        all_concerns = []
        amendments = []
        for p, s in final_speeches.items():
            all_concerns.extend(s.get("primary_concerns", []))
            amendments.append(f"[{p}] {s.get('recommended_amendment', '')}")
            
        status = "APPROVED_WITH_GUARDRAILS" if convergence.get("mean_support_score", 0) >= 7.0 else "REJECTED_FOR_REVISION"
        
        return {
            "final_decision": status,
            "executive_summary": f"Consensus synthesized for '{topic}'. Decision: {status}.",
            "required_guardrails": list(set(all_concerns)),
            "persona_amendments": amendments,
            "dissenting_notes": [p for p, s in final_speeches.items() if s.get("support_score", 10) < 7.0]
        }
