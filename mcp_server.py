"""MCP JSON-RPC stdio server for genpark-multi-agent-debate-consensus-synthesizer-skill."""
import sys
import json
from client import MultiAgentDebateConsensusSynthesizer

synthesizer = MultiAgentDebateConsensusSynthesizer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "orchestrate_multi_agent_debate":
        return {"error": f"Unknown tool '{name}'"}
        
    action = args.get("action")
    topic = args.get("topic", "Autonomous Deployment Approval")
    
    if action == "run_debate":
        return synthesizer.orchestrate_debate(
            topic=topic,
            personas=args.get("personas"),
            rounds=args.get("rounds", 2)
        )
    elif action == "evaluate_convergence":
        speeches = args.get("arguments", {})
        return synthesizer.evaluate_convergence(speeches)
    elif action == "synthesize_verdict":
        speeches = args.get("arguments", {})
        conv = synthesizer.evaluate_convergence(speeches)
        return synthesizer.synthesize_verdict(topic, speeches, conv)
    else:
        return {"error": f"Unknown action '{action}'"}

def main():
    if "--test" in sys.argv:
        print("[TEST] Running self-test for MultiAgentDebateConsensusSynthesizer...")
        res = synthesizer.orchestrate_debate("Automate production database migration", rounds=2)
        assert res["status"] == "success"
        assert "consensus_verdict" in res
        print(f"[TEST] Success! Final Decision: {res['consensus_verdict']['final_decision']}")
        return

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "orchestrate_multi_agent_debate",
                                "description": "Run multi-persona agent debate rounds, evaluate convergence, and synthesize consensus verdict.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "action": {"type": "string", "enum": ["run_debate", "evaluate_convergence", "synthesize_verdict"]},
                                        "topic": {"type": "string"},
                                        "personas": {"type": "array", "items": {"type": "string"}},
                                        "rounds": {"type": "integer"},
                                        "arguments": {"type": "object"}
                                    },
                                    "required": ["action", "topic"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
