"""Futuristic Sci-Fi React 18 + Vis Network Knowledge Graph with Live Data Flow.

Features:
- Live animated cybernetic data packets streaming along directional synapses
- Inward (Cyan 📥) vs Outward (Magenta 📤) data flow visualization for every node
- Preset architectural data pipelines (ML Feature Flow, Blockchain Audit, Db2 Toolkit)
- Interactive pipeline isolation mode (dims outside nodes, focuses on flow)
- Deep upstream & downstream data flow telemetry in the Node Inspector HUD
- Web Audio API synthesizer for cybernetic clicks, target locks, and warp navigation
- Fully standalone HTML output in graphify-out/graph.html
"""

import json
from pathlib import Path


def generate_react_html():
    graph_path = Path("graphify-out/graph.json")
    labels_path = Path("graphify-out/.graphify_labels.json")

    graph_data = (
        json.loads(graph_path.read_text(encoding="utf-8"))
        if graph_path.exists()
        else {"nodes": [], "links": [], "hyperedges": []}
    )
    labels_data = (
        json.loads(labels_path.read_text(encoding="utf-8"))
        if labels_path.exists()
        else {}
    )

    CYBER_PALETTE = [
        "#00f0ff", "#ff007f", "#7000ff", "#00ff88", "#ffb703", 
        "#ff0055", "#00e5ff", "#b5179e", "#3a86ff", "#39ff14", 
        "#ff5400", "#9d4edd", "#05f140", "#f72585", "#4cc9f0", 
        "#f15bb5", "#fee440", "#00bbf9", "#00f5d4", "#8338ec",
    ]

    nodes = graph_data.get("nodes", [])
    links = graph_data.get("links", [])
    hyperedges = graph_data.get("hyperedges", [])

    degree_map = {}
    in_degree_map = {}
    out_degree_map = {}
    adj_map = {}

    for n in nodes:
        nid = n["id"]
        degree_map[nid] = 0
        in_degree_map[nid] = 0
        out_degree_map[nid] = 0
        adj_map[nid] = []

    for l in links:
        src = l["source"]
        tgt = l["target"]
        if src in degree_map:
            degree_map[src] += 1
            out_degree_map[src] += 1
            adj_map[src].append({
                "target": tgt,
                "relation": l.get("relation", "linked"),
                "confidence": l.get("confidence", "EXTRACTED"),
                "direction": "out",
            })
        if tgt in degree_map:
            degree_map[tgt] += 1
            in_degree_map[tgt] += 1
            adj_map[tgt].append({
                "target": src,
                "relation": l.get("relation", "linked"),
                "confidence": l.get("confidence", "EXTRACTED"),
                "direction": "in",
            })

    comm_stats = {}
    for n in nodes:
        cid = n.get("community", 0)
        cname = labels_data.get(str(cid), n.get("community_name", f"Sector-{cid:02d}"))
        n["community_name"] = cname
        n["degree"] = degree_map.get(n["id"], 0)
        n["in_degree"] = in_degree_map.get(n["id"], 0)
        n["out_degree"] = out_degree_map.get(n["id"], 0)
        color = CYBER_PALETTE[cid % len(CYBER_PALETTE)]
        n["color"] = color

        if cid not in comm_stats:
            comm_stats[cid] = {"cid": cid, "name": cname, "count": 0, "color": color}
        comm_stats[cid]["count"] += 1

    communities_list = sorted(list(comm_stats.values()), key=lambda x: x["count"], reverse=True)
    god_nodes = sorted(nodes, key=lambda x: x["degree"], reverse=True)[:20]

    # Pre-defined Architectural Data Flow Pipelines
    pipelines = [
        {
            "id": "ml_pipeline",
            "name": "Machine Learning & Feature Engineering Flow",
            "description": "storage.py (market bars) ➔ feature_builder.py (cyclical & price features) ➔ train_pipeline.py ➔ predictor.py (real-time predictions)",
            "keywords": ["storage.py", "feature_builder.py", "build_latest_features()", "train_pipeline.py", "predictor.py", "predict_latest()"],
            "color": "#00f0ff"
        },
        {
            "id": "blockchain_pipeline",
            "name": "Cryptographic Blockchain Immutability Audit Flow",
            "description": "Price/Prediction snapshot ➔ AnchorService (keccak256 SHA-3) ➔ ChainClient (Web3.py) ➔ Smart Contracts",
            "keywords": ["storage.py", "insert_blockchain_anchor()", "anchor_service.py", "AnchorService", "chain_client.py", "ChainClient", "oracle_service.py"],
            "color": "#ff007f"
        },
        {
            "id": "db2_pipeline",
            "name": "IBM Db2 LUW Analytics & Multi-Agent Flow",
            "description": "SQL query ➔ dialect_transpiler.py ➔ Db2ConnectionManager ➔ dbt models ➔ LangChain Text-to-SQL & Vector Store ➔ CrewAI",
            "keywords": ["db2_routes.py", "dialect_transpiler.py", "Db2DialectTranspiler", "connection.py", "Db2ConnectionManager", "langchain_agent.py", "crewai_agents.py", "Db2Crew"],
            "color": "#9d4edd"
        },
        {
            "id": "frontend_pipeline",
            "name": "Full-Stack API Gateway & UI Telemetry Flow",
            "description": "FastAPI routes (routes.py / db2_routes.py) ➔ apiService (frontend) ➔ MarketAnalyticsPage / BlockchainAuditPage / OverviewPage",
            "keywords": ["routes.py", "db2_routes.py", "services/api.ts", "apiService", "AppLayout.tsx", "MarketAnalyticsPage.tsx", "BlockchainAuditPage.tsx", "OverviewPage.tsx"],
            "color": "#00ff88"
        }
    ]

    embedded_data_json = json.dumps(
        {
            "nodes": nodes,
            "links": links,
            "hyperedges": hyperedges,
            "communities": communities_list,
            "godNodes": [
                {
                    "id": n["id"],
                    "label": n["label"],
                    "degree": n["degree"],
                    "in_degree": n["in_degree"],
                    "out_degree": n["out_degree"],
                    "community_name": n["community_name"],
                    "color": n["color"],
                    "file_type": n.get("file_type", "code"),
                }
                for n in god_nodes
            ],
            "pipelines": pipelines,
            "totalNodes": len(nodes),
            "totalLinks": len(links),
            "totalCommunities": len(communities_list),
        },
        ensure_ascii=False,
    )

    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AEGIS // NEURAL DATA FLOW MATRIX [SCI-FI HUD]</title>
  
  <!-- Cybernetic Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <!-- Vis Network Core -->
  <script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"></script>
  
  <!-- React 18 & Babel -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <style>
    :root {
      --cyber-bg: #030611;
      --cyber-surface: rgba(6, 12, 28, 0.90);
      --cyber-card: rgba(10, 20, 44, 0.80);
      --cyber-card-hover: rgba(16, 32, 68, 0.92);
      --neon-cyan: #00f0ff;
      --neon-magenta: #ff007f;
      --neon-purple: #9d4edd;
      --neon-green: #00ff88;
      --neon-amber: #ffb703;
      --border-cyber: rgba(0, 240, 255, 0.28);
      --border-cyber-glow: rgba(0, 240, 255, 0.75);
      --text-main: #f0f6fc;
      --text-dim: #7d8da6;
      --glow-cyan: 0 0 16px rgba(0, 240, 255, 0.45);
      --glow-magenta: 0 0 16px rgba(255, 0, 127, 0.45);
      --glow-green: 0 0 16px rgba(0, 255, 136, 0.45);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      background: var(--cyber-bg);
      color: var(--text-main);
      font-family: 'Rajdhani', -apple-system, sans-serif;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .font-hud {
      font-family: 'Orbitron', monospace;
      letter-spacing: 0.08em;
    }

    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }

    /* Scanline & Grid */
    .cyber-grid {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: 
        linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 2;
    }

    .scanline {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        to bottom,
        rgba(255,255,255,0),
        rgba(255,255,255,0) 50%,
        rgba(0, 240, 255, 0.015) 50%,
        rgba(0, 240, 255, 0.015)
      );
      background-size: 100% 4px;
      pointer-events: none;
      z-index: 3;
    }

    .hud-panel {
      background: var(--cyber-surface);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--border-cyber);
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.6), inset 0 0 15px rgba(0, 240, 255, 0.05);
      position: relative;
    }

    .hud-panel-glow {
      border-color: var(--neon-cyan);
      box-shadow: var(--glow-cyan), inset 0 0 20px rgba(0, 240, 255, 0.12);
    }

    .corner-brackets::before {
      content: '';
      position: absolute;
      top: -1px;
      left: -1px;
      width: 8px;
      height: 8px;
      border-top: 2px solid var(--neon-cyan);
      border-left: 2px solid var(--neon-cyan);
      pointer-events: none;
    }
    .corner-brackets::after {
      content: '';
      position: absolute;
      bottom: -1px;
      right: -1px;
      width: 8px;
      height: 8px;
      border-bottom: 2px solid var(--neon-cyan);
      border-right: 2px solid var(--neon-cyan);
      pointer-events: none;
    }

    .cyber-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 6px 14px;
      font-family: 'Orbitron', monospace;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--neon-cyan);
      background: rgba(0, 240, 255, 0.06);
      border: 1px solid var(--border-cyber);
      clip-path: polygon(8px 0%, 100% 0%, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0% 100%, 0% 8px);
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .cyber-btn:hover {
      background: rgba(0, 240, 255, 0.22);
      border-color: var(--neon-cyan);
      box-shadow: var(--glow-cyan);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .cyber-btn-magenta {
      color: var(--neon-magenta);
      background: rgba(255, 0, 127, 0.06);
      border-color: rgba(255, 0, 127, 0.4);
    }

    .cyber-btn-magenta:hover {
      background: rgba(255, 0, 127, 0.25);
      border-color: var(--neon-magenta);
      box-shadow: var(--glow-magenta);
      color: #ffffff;
    }

    .cyber-btn-green {
      color: var(--neon-green);
      background: rgba(0, 255, 136, 0.06);
      border-color: rgba(0, 255, 136, 0.4);
    }

    .cyber-btn-green:hover {
      background: rgba(0, 255, 136, 0.25);
      border-color: var(--neon-green);
      box-shadow: var(--glow-green);
      color: #ffffff;
    }

    .cyber-btn-active {
      background: var(--neon-cyan);
      color: #030611 !important;
      border-color: var(--neon-cyan);
      box-shadow: var(--glow-cyan);
      font-weight: 700;
    }

    .cyber-input {
      background: rgba(3, 6, 17, 0.85);
      border: 1px solid var(--border-cyber);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 7px 12px;
      outline: none;
      transition: all 0.2s;
    }

    .cyber-input:focus {
      border-color: var(--neon-cyan);
      box-shadow: var(--glow-cyan);
      background: rgba(6, 12, 28, 0.95);
    }

    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(3, 6, 17, 0.6);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(0, 240, 255, 0.3);
      border-radius: 2px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--neon-cyan);
      box-shadow: var(--glow-cyan);
    }

    #root {
      width: 100vw;
      height: 100vh;
      position: relative;
      display: flex;
      flex-direction: column;
      z-index: 5;
    }

    #graph-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      background: radial-gradient(circle at 50% 50%, #061126 0%, #02040a 100%);
    }

    @keyframes pulse-cyan {
      0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.7); }
      70% { box-shadow: 0 0 0 8px rgba(0, 240, 255, 0); }
      100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--neon-cyan);
      animation: pulse-cyan 1.8s infinite;
    }

    .pulse-dot-magenta {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--neon-magenta);
      animation: pulse-cyan 1.4s infinite;
    }
  </style>
</head>
<body>
  <div class="cyber-grid"></div>
  <div class="scanline"></div>
  <div id="root"></div>

  <script>
    window.GRAPH_DATA = __GRAPH_DATA_PLACEHOLDER__;
  </script>

  <script type="text/babel">
    const { useState, useEffect, useRef, useMemo } = React;

    // Web Audio Synthesizer
    const playCyberSfx = (type) => {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        const t = ctx.currentTime;

        if (type === 'click') {
          osc.type = 'sine';
          osc.frequency.setValueAtTime(900, t);
          osc.frequency.exponentialRampToValueAtTime(1400, t + 0.04);
          gain.gain.setValueAtTime(0.06, t);
          gain.gain.linearRampToValueAtTime(0.001, t + 0.04);
          osc.start(t);
          osc.stop(t + 0.04);
        } else if (type === 'lock') {
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(320, t);
          osc.frequency.setValueAtTime(640, t + 0.04);
          gain.gain.setValueAtTime(0.05, t);
          gain.gain.linearRampToValueAtTime(0.001, t + 0.08);
          osc.start(t);
          osc.stop(t + 0.08);
        } else if (type === 'warp') {
          osc.type = 'sine';
          osc.frequency.setValueAtTime(220, t);
          osc.frequency.exponentialRampToValueAtTime(1800, t + 0.22);
          gain.gain.setValueAtTime(0.08, t);
          gain.gain.linearRampToValueAtTime(0.001, t + 0.22);
          osc.start(t);
          osc.stop(t + 0.22);
        }
      } catch (e) {}
    };

    function App() {
      const data = window.GRAPH_DATA || { nodes: [], links: [], communities: [], godNodes: [], pipelines: [] };

      // State
      const [network, setNetwork] = useState(null);
      const [selectedNodeId, setSelectedNodeId] = useState(null);
      const [searchQuery, setSearchQuery] = useState('');
      const [activeTab, setActiveTab] = useState('flows');
      const [visibleCommunities, setVisibleCommunities] = useState(new Set(data.communities.map(c => c.cid)));
      const [minDegree, setMinDegree] = useState(0);
      const [physicsEnabled, setPhysicsEnabled] = useState(false);
      const [sfxEnabled, setSfxEnabled] = useState(true);
      const [isSidebarOpen, setIsSidebarOpen] = useState(true);
      const [isInspectorOpen, setIsInspectorOpen] = useState(false);
      const [pathStart, setPathStart] = useState(null);
      const [pathEnd, setPathEnd] = useState(null);
      const [shortestPath, setShortestPath] = useState(null);
      const [cursorCoords, setCursorCoords] = useState({ x: 0, y: 0 });

      // Live Data Flow Specific State
      const [dataFlowStreaming, setDataFlowStreaming] = useState(true);
      const [isolatedFlowMode, setIsolatedFlowMode] = useState(false);
      const [activePipelineId, setActivePipelineId] = useState(null);

      const containerRef = useRef(null);
      const nodesDSRef = useRef(null);
      const edgesDSRef = useRef(null);
      const animPhaseRef = useRef(0);
      const animReqRef = useRef(null);

      const triggerSfx = (type) => {
        if (sfxEnabled) playCyberSfx(type);
      };

      const nodeMap = useMemo(() => {
        const m = new Map();
        data.nodes.forEach(n => m.set(n.id, n));
        return m;
      }, [data.nodes]);

      // Map links for quick lookup
      const linksByEndpoint = useMemo(() => {
        const outMap = new Map();
        const inMap = new Map();
        data.links.forEach(l => {
          if (!outMap.has(l.source)) outMap.set(l.source, []);
          outMap.get(l.source).push(l);
          if (!inMap.has(l.target)) inMap.set(l.target, []);
          inMap.get(l.target).push(l);
        });
        return { outMap, inMap };
      }, [data.links]);

      // Adjacency graph for pathfinding
      const adjGraph = useMemo(() => {
        const adj = new Map();
        data.nodes.forEach(n => adj.set(n.id, []));
        data.links.forEach(l => {
          const u = l.source;
          const v = l.target;
          if (adj.has(u) && adj.has(v)) {
            adj.get(u).push({ node: v, relation: l.relation, confidence: l.confidence, dir: 'out' });
            adj.get(v).push({ node: u, relation: l.relation, confidence: l.confidence, dir: 'in' });
          }
        });
        return adj;
      }, [data.nodes, data.links]);

      // Active pipeline nodes set
      const activePipelineNodeSet = useMemo(() => {
        if (!activePipelineId) return new Set();
        const pipe = data.pipelines.find(p => p.id === activePipelineId);
        if (!pipe) return new Set();
        const matched = new Set();
        data.nodes.forEach(n => {
          if (pipe.keywords.some(kw => n.label.includes(kw) || n.id.includes(kw))) {
            matched.add(n.id);
          }
        });
        return matched;
      }, [activePipelineId, data.pipelines, data.nodes]);

      // Initialize Network
      useEffect(() => {
        if (!containerRef.current) return;

        const visNodes = data.nodes.map(n => ({
          id: n.id,
          label: n.label,
          color: {
            background: n.color,
            border: '#ffffff',
            highlight: { background: '#00f0ff', border: '#ffffff' },
            hover: { background: '#ffffff', border: '#00f0ff' }
          },
          size: Math.max(8, Math.min(30, 8 + Math.sqrt(n.degree || 1) * 3)),
          font: { size: n.degree > 12 ? 11 : 0, color: '#f0f6fc', face: 'Orbitron', strokeWidth: 2, strokeColor: '#030611' },
          shadow: { enabled: true, color: n.color, size: 10, x: 0, y: 0 },
          _raw: n
        }));

        const visEdges = data.links.map((e, idx) => ({
          id: idx,
          from: e.source,
          to: e.target,
          dashes: e.confidence === 'INFERRED',
          width: e.confidence === 'INFERRED' ? 1.2 : 1.8,
          color: {
            color: e.confidence === 'INFERRED' ? '#ff007f' : 'rgba(0, 240, 255, 0.45)',
            highlight: '#00f0ff',
            opacity: 0.7
          },
          arrows: { to: { enabled: true, scaleFactor: 0.55 } },
          _raw: e
        }));

        const nodesDS = new vis.DataSet(visNodes);
        const edgesDS = new vis.DataSet(visEdges);
        nodesDSRef.current = nodesDS;
        edgesDSRef.current = edgesDS;

        const options = {
          physics: {
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
              gravitationalConstant: -65,
              centralGravity: 0.005,
              springLength: 120,
              springConstant: 0.07,
              damping: 0.48,
              avoidOverlap: 0.8
            },
            stabilization: { iterations: 200, fit: true }
          },
          interaction: {
            hover: true,
            tooltipDelay: 100,
            hideEdgesOnDrag: true,
            zoomView: true,
            dragView: true
          },
          nodes: { shape: 'dot', borderWidth: 1.5 },
          edges: { smooth: { type: 'continuous', roundness: 0.2 } }
        };

        const net = new vis.Network(containerRef.current, { nodes: nodesDS, edges: edgesDS }, options);
        setNetwork(net);

        net.on('stabilizationIterationsDone', () => {
          net.setOptions({ physics: { enabled: false } });
          setPhysicsEnabled(false);
        });

        net.on('selectNode', (params) => {
          if (params.nodes.length > 0) {
            const nid = params.nodes[0];
            setSelectedNodeId(nid);
            setIsInspectorOpen(true);
            triggerSfx('lock');
          }
        });

        net.on('deselectNode', () => {
          setSelectedNodeId(null);
          setIsolatedFlowMode(false);
        });

        return () => net.destroy();
      }, []);

      // ── Live Cybernetic Data Packets Canvas Drawing Loop ───────────────────
      useEffect(() => {
        if (!network) return;

        const handleAfterDrawing = (ctx) => {
          if (!dataFlowStreaming) return;

          const phase = animPhaseRef.current;
          let edgesToAnimate = [];

          if (selectedNodeId) {
            // Animate exact incoming and outgoing edges for the selected target node
            edgesToAnimate = data.links.filter(
              l => l.source === selectedNodeId || l.target === selectedNodeId
            );
          } else if (activePipelineNodeSet.size > 0) {
            // Animate edges within active data pipeline
            edgesToAnimate = data.links.filter(
              l => activePipelineNodeSet.has(l.source) && activePipelineNodeSet.has(l.target)
            );
          } else {
            // Default: animate subset of key directional edges across the mesh
            edgesToAnimate = data.links.slice(0, 160);
          }

          if (edgesToAnimate.length === 0) return;

          ctx.save();
          edgesToAnimate.forEach((edge, idx) => {
            const pos1 = network.getPosition(edge.source);
            const pos2 = network.getPosition(edge.target);
            if (!pos1 || !pos2) return;

            // Inward data flow = Cyan (#00f0ff), Outward data flow = Magenta (#ff007f)
            const isOut = selectedNodeId ? (edge.source === selectedNodeId) : (idx % 2 === 0);
            const color = isOut ? '#ff007f' : '#00f0ff';

            // 2 glowing data packets travelling from source ➔ target
            for (let p = 0; p < 2; p++) {
              const offset = p * 0.5;
              const t = (phase + offset + (idx * 0.05)) % 1.0;
              const x = pos1.x + (pos2.x - pos1.x) * t;
              const y = pos1.y + (pos2.y - pos1.y) * t;

              ctx.beginPath();
              ctx.arc(x, y, 3.5, 0, 2 * Math.PI);
              ctx.fillStyle = color;
              ctx.shadowColor = color;
              ctx.shadowBlur = 10;
              ctx.fill();
            }
          });
          ctx.restore();
        };

        network.on('afterDrawing', handleAfterDrawing);

        let running = true;
        const loop = () => {
          if (!running) return;
          if (dataFlowStreaming) {
            animPhaseRef.current = (animPhaseRef.current + 0.012) % 1.0;
            network.redraw();
          }
          animReqRef.current = requestAnimationFrame(loop);
        };
        animReqRef.current = requestAnimationFrame(loop);

        return () => {
          running = false;
          if (animReqRef.current) cancelAnimationFrame(animReqRef.current);
          network.off('afterDrawing', handleAfterDrawing);
        };
      }, [network, dataFlowStreaming, selectedNodeId, activePipelineNodeSet]);

      const handleMouseMove = (e) => {
        setCursorCoords({ x: e.clientX, y: e.clientY });
      };

      const focusOnNode = (nodeId) => {
        if (!network || !nodeId) return;
        triggerSfx('warp');
        setSelectedNodeId(nodeId);
        setIsInspectorOpen(true);
        network.selectNodes([nodeId]);
        network.focus(nodeId, {
          scale: 1.5,
          animation: { duration: 700, easingFunction: 'easeInOutQuad' }
        });
      };

      // Isolate Data Flow around selected node
      const toggleIsolateFlow = () => {
        if (!selectedNodeId || !nodesDSRef.current) return;
        triggerSfx('lock');
        const nextMode = !isolatedFlowMode;
        setIsolatedFlowMode(nextMode);

        if (nextMode) {
          const directNeighbors = new Set([selectedNodeId]);
          (adjGraph.get(selectedNodeId) || []).forEach(nb => directNeighbors.add(nb.node));

          const updates = data.nodes.map(n => ({
            id: n.id,
            hidden: !directNeighbors.has(n.id)
          }));
          nodesDSRef.current.update(updates);
          network.fit({ nodes: Array.from(directNeighbors), animation: { duration: 600 } });
        } else {
          // Restore all nodes
          const updates = data.nodes.map(n => ({ id: n.id, hidden: false }));
          nodesDSRef.current.update(updates);
        }
      };

      // Activate Pre-configured Pipeline
      const activatePipeline = (pipe) => {
        triggerSfx('warp');
        setActivePipelineId(pipe.id);
        setSelectedNodeId(null);

        const matched = [];
        data.nodes.forEach(n => {
          if (pipe.keywords.some(kw => n.label.includes(kw) || n.id.includes(kw))) {
            matched.push(n.id);
          }
        });

        if (matched.length > 0 && network && nodesDSRef.current) {
          network.selectNodes(matched);
          network.fit({ nodes: matched, animation: { duration: 700 } });
        }
      };

      const fitNetwork = () => {
        if (network) {
          triggerSfx('click');
          setActivePipelineId(null);
          setIsolatedFlowMode(false);
          const updates = data.nodes.map(n => ({ id: n.id, hidden: false }));
          if (nodesDSRef.current) nodesDSRef.current.update(updates);
          network.fit({ animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
        }
      };

      const togglePhysics = () => {
        triggerSfx('click');
        const next = !physicsEnabled;
        setPhysicsEnabled(next);
        if (network) network.setOptions({ physics: { enabled: next } });
      };

      const searchResults = useMemo(() => {
        if (!searchQuery.trim()) return [];
        const q = searchQuery.toLowerCase();
        return data.nodes
          .filter(n => n.label.toLowerCase().includes(q) || n.id.toLowerCase().includes(q))
          .slice(0, 15);
      }, [searchQuery, data.nodes]);

      const selectedNode = selectedNodeId ? nodeMap.get(selectedNodeId) : null;
      
      // Separate Upstream (Inward Data) vs Downstream (Outward Data)
      const dataFlowBreakdown = useMemo(() => {
        if (!selectedNodeId) return { upstream: [], downstream: [] };
        const rawIn = linksByEndpoint.inMap.get(selectedNodeId) || [];
        const rawOut = linksByEndpoint.outMap.get(selectedNodeId) || [];

        const upstream = rawIn.map(l => ({
          node: nodeMap.get(l.source) || { id: l.source, label: l.source, color: '#00f0ff' },
          relation: l.relation || 'feeds_into'
        }));

        const downstream = rawOut.map(l => ({
          node: nodeMap.get(l.target) || { id: l.target, label: l.target, color: '#ff007f' },
          relation: l.relation || 'consumes_output'
        }));

        return { upstream, downstream };
      }, [selectedNodeId, linksByEndpoint, nodeMap]);

      return (
        <div onMouseMove={handleMouseMove} style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
          
          <div id="graph-container" ref={containerRef}></div>

          {/* ── Top Cybernetic HUD Header ───────────────────────────────────── */}
          <header className="hud-panel corner-brackets" style={{
            position: 'absolute', top: 12, left: 16, right: 16, height: 58,
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '0 20px', zIndex: 10
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <div className={dataFlowStreaming ? "pulse-dot" : "pulse-dot-magenta"}></div>
              <div>
                <div className="font-hud" style={{ fontSize: 14, fontWeight: 800, color: '#00f0ff', letterSpacing: '0.12em', display: 'flex', alignItems: 'center', gap: 8 }}>
                  AEGIS // NEURAL DATA FLOW
                  <span style={{ fontSize: 9, padding: '2px 6px', background: 'rgba(0, 240, 255, 0.15)', border: '1px solid var(--neon-cyan)', borderRadius: 2 }}>
                    SYNAPSE STREAMING
                  </span>
                </div>
                <div className="font-mono" style={{ fontSize: 10, color: 'var(--text-dim)' }}>
                  DATA FLOW PIPELINE MATRIX // DIRECTIONAL TRACING
                </div>
              </div>
            </div>

            {/* Central Telemetry Stats */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
              <div style={{ textAlign: 'center' }}>
                <div className="font-hud" style={{ fontSize: 16, fontWeight: 700, color: '#00f0ff' }}>{data.totalNodes}</div>
                <div className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>NODES</div>
              </div>
              <div style={{ width: 1, height: 24, background: 'var(--border-cyber)' }}></div>
              <div style={{ textAlign: 'center' }}>
                <div className="font-hud" style={{ fontSize: 16, fontWeight: 700, color: '#ff007f' }}>{data.totalLinks}</div>
                <div className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>SYNAPSES</div>
              </div>
              <div style={{ width: 1, height: 24, background: 'var(--border-cyber)' }}></div>
              <div style={{ textAlign: 'center' }}>
                <div className="font-hud" style={{ fontSize: 16, fontWeight: 700, color: '#00ff88' }}>{data.totalCommunities}</div>
                <div className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>SECTORS</div>
              </div>
            </div>

            {/* Global Controls & SFX Toggle */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <button
                className={`cyber-btn ${dataFlowStreaming ? 'cyber-btn-active' : ''}`}
                onClick={() => { triggerSfx('click'); setDataFlowStreaming(!dataFlowStreaming); }}
                title="Toggle Live Synapse Data Packets"
              >
                FLOW: {dataFlowStreaming ? 'STREAMING' : 'PAUSED'}
              </button>
              <button
                className={`cyber-btn ${sfxEnabled ? 'cyber-btn-green' : ''}`}
                onClick={() => setSfxEnabled(!sfxEnabled)}
              >
                SFX: {sfxEnabled ? 'ON' : 'OFF'}
              </button>
              <button className="cyber-btn" onClick={fitNetwork}>
                RESET VIEW
              </button>
              <button
                className={`cyber-btn ${physicsEnabled ? 'cyber-btn-magenta' : ''}`}
                onClick={togglePhysics}
              >
                {physicsEnabled ? 'FREEZE' : 'ORBIT'}
              </button>
            </div>
          </header>

          {/* ── Left Navigation Deck ──────────────────────────────────────── */}
          <aside className="hud-panel corner-brackets" style={{
            position: 'absolute', top: 82, bottom: 54, left: 16, width: isSidebarOpen ? 340 : 44,
            display: 'flex', flexDirection: 'column', zIndex: 10, transition: 'width 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
          }}>
            <div style={{
              height: 44, borderBottom: '1px solid var(--border-cyber)', display: 'flex',
              alignItems: 'center', justifyContent: 'space-between', padding: '0 12px'
            }}>
              {isSidebarOpen && (
                <span className="font-hud" style={{ fontSize: 11, fontWeight: 700, color: 'var(--neon-cyan)' }}>
                  // FLOW NAVIGATOR
                </span>
              )}
              <button
                className="cyber-btn"
                style={{ padding: '3px 8px', fontSize: 10 }}
                onClick={() => { triggerSfx('click'); setIsSidebarOpen(!isSidebarOpen); }}
              >
                {isSidebarOpen ? '◄' : '►'}
              </button>
            </div>

            {isSidebarOpen && (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 12 }}>
                
                {/* Search Bar */}
                <div style={{ position: 'relative', marginBottom: 12 }}>
                  <input
                    type="text"
                    className="cyber-input"
                    style={{ width: '100%', paddingLeft: 10 }}
                    placeholder="LOCATE FLOW NODE..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery('')}
                      style={{ position: 'absolute', right: 8, top: 8, background: 'none', border: 'none', color: 'var(--neon-cyan)', cursor: 'pointer' }}
                    >
                      ✕
                    </button>
                  )}
                </div>

                {searchResults.length > 0 && (
                  <div className="hud-panel" style={{
                    maxHeight: 180, overflowY: 'auto', marginBottom: 12, border: '1px solid var(--neon-cyan)', padding: 4
                  }}>
                    {searchResults.map(n => (
                      <div
                        key={n.id}
                        onClick={() => { focusOnNode(n.id); setSearchQuery(''); }}
                        style={{
                          padding: '6px 8px', fontSize: 11, cursor: 'pointer', display: 'flex',
                          alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(0, 240, 255, 0.1)'
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(0, 240, 255, 0.12)'}
                        onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                      >
                        <span style={{ fontWeight: 600, color: '#ffffff' }}>{n.label}</span>
                        <span className="font-mono" style={{ fontSize: 9, color: 'var(--neon-cyan)' }}>DEG: {n.degree}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Navigation Tabs */}
                <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
                  {[
                    { id: 'flows', label: 'FLOWS' },
                    { id: 'sectors', label: 'SECTORS' },
                    { id: 'nexus', label: 'NEXUS' },
                  ].map(tab => (
                    <button
                      key={tab.id}
                      className={`cyber-btn ${activeTab === tab.id ? 'cyber-btn-active' : ''}`}
                      style={{ flex: 1, fontSize: 10, padding: '5px 0' }}
                      onClick={() => { triggerSfx('click'); setActiveTab(tab.id); }}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>

                {/* Tab 1: DATA FLOW PIPELINES */}
                {activeTab === 'flows' && (
                  <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 8 }}>
                    <div style={{ fontSize: 11, color: 'var(--text-dim)', marginBottom: 4 }}>
                      Select a pipeline to trace end-to-end data flow:
                    </div>

                    {data.pipelines.map(pipe => {
                      const isActive = activePipelineId === pipe.id;
                      return (
                        <div
                          key={pipe.id}
                          onClick={() => activatePipeline(pipe)}
                          style={{
                            padding: '10px 12px', background: isActive ? 'rgba(0, 240, 255, 0.12)' : 'rgba(0, 240, 255, 0.03)',
                            border: `1px solid ${isActive ? pipe.color : 'var(--border-cyber)'}`,
                            cursor: 'pointer', transition: 'all 0.15s'
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
                            <span className="font-hud" style={{ fontSize: 11, fontWeight: 700, color: pipe.color }}>
                              {pipe.name}
                            </span>
                            {isActive && (
                              <span style={{ fontSize: 9, padding: '1px 5px', background: pipe.color, color: '#030611', fontWeight: 800 }}>
                                ACTIVE
                              </span>
                            )}
                          </div>
                          <div style={{ fontSize: 10, color: 'var(--text-dim)', lineHeight: 1.4 }}>
                            {pipe.description}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Tab 2: Sectors */}
                {activeTab === 'sectors' && (
                  <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {data.communities.map(c => (
                      <div
                        key={c.cid}
                        style={{
                          padding: '8px 10px', background: 'rgba(0, 240, 255, 0.03)',
                          border: `1px solid ${c.color}`, cursor: 'pointer'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                          <span style={{ fontSize: 12, fontWeight: 700, color: '#ffffff' }}>{c.name}</span>
                          <span className="font-mono" style={{ fontSize: 10, color: c.color }}>{c.count} NODES</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Tab 3: Nexus Cores */}
                {activeTab === 'nexus' && (
                  <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {data.godNodes.map((n, idx) => (
                      <div
                        key={n.id}
                        onClick={() => focusOnNode(n.id)}
                        style={{
                          padding: '8px 10px', background: 'rgba(0, 240, 255, 0.03)',
                          border: '1px solid var(--border-cyber)', cursor: 'pointer',
                          display: 'flex', alignItems: 'center', justifyContent: 'space-between'
                        }}
                      >
                        <div>
                          <div style={{ fontSize: 12, fontWeight: 700, color: '#ffffff' }}>{n.label}</div>
                          <div className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>{n.community_name}</div>
                        </div>
                        <span className="font-mono" style={{ fontSize: 10, color: '#00f0ff', fontWeight: 600 }}>
                          PWR {n.degree}
                        </span>
                      </div>
                    ))}
                  </div>
                )}

              </div>
            )}
          </aside>

          {/* ── Right Target Diagnostic Inspector (HUD) ────────────────────── */}
          {selectedNode && isInspectorOpen && (
            <section className="hud-panel corner-brackets hud-panel-glow" style={{
              position: 'absolute', top: 82, right: 16, width: 360, maxHeight: 'calc(100vh - 150px)',
              display: 'flex', flexDirection: 'column', zIndex: 10, padding: 16
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                <div>
                  <div className="font-hud" style={{ fontSize: 9, color: 'var(--neon-cyan)', letterSpacing: '0.1em' }}>
                    TARGET NODE // {selectedNode.file_type || 'CODE'}
                  </div>
                  <h2 className="font-hud" style={{ fontSize: 17, fontWeight: 800, color: '#ffffff', wordBreak: 'break-all' }}>
                    {selectedNode.label}
                  </h2>
                </div>
                <button
                  className="cyber-btn"
                  style={{ padding: '2px 6px', fontSize: 11 }}
                  onClick={() => setIsInspectorOpen(false)}
                >
                  ✕
                </button>
              </div>

              {/* Data Flow Telemetry Metrics */}
              <div style={{
                background: 'rgba(0, 240, 255, 0.05)', border: '1px solid var(--border-cyber)',
                padding: 10, marginBottom: 12, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 6, textAlign: 'center'
              }}>
                <div>
                  <div className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>TOTAL</div>
                  <div className="font-hud" style={{ fontSize: 14, color: '#00f0ff', fontWeight: 700 }}>{selectedNode.degree}</div>
                </div>
                <div>
                  <div className="font-mono" style={{ fontSize: 9, color: '#00f0ff' }}>📥 INWARD</div>
                  <div className="font-hud" style={{ fontSize: 14, color: '#00f0ff', fontWeight: 700 }}>{selectedNode.in_degree}</div>
                </div>
                <div>
                  <div className="font-mono" style={{ fontSize: 9, color: '#ff007f' }}>📤 OUTWARD</div>
                  <div className="font-hud" style={{ fontSize: 14, color: '#ff007f', fontWeight: 700 }}>{selectedNode.out_degree}</div>
                </div>
              </div>

              {/* Isolate Flow Mode Button */}
              <button
                className={`cyber-btn ${isolatedFlowMode ? 'cyber-btn-magenta' : 'cyber-btn-active'}`}
                style={{ width: '100%', marginBottom: 12 }}
                onClick={toggleIsolateFlow}
              >
                {isolatedFlowMode ? 'RESTORE FULL MESH' : 'ISOLATE DATA FLOW PATH'}
              </button>

              {/* 📥 UPSTREAM DATA FLOW (Inputs & Callers) */}
              <div style={{ marginBottom: 10 }}>
                <div className="font-hud" style={{ fontSize: 10, color: '#00f0ff', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span>📥 INCOMING DATA FLOW (SOURCES)</span>
                  <span className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>({dataFlowBreakdown.upstream.length})</span>
                </div>
                <div style={{ maxHeight: 110, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {dataFlowBreakdown.upstream.length === 0 ? (
                    <div style={{ fontSize: 10, color: 'var(--text-dim)', fontStyle: 'italic' }}>No incoming flows detected (Root Source)</div>
                  ) : (
                    dataFlowBreakdown.upstream.map((item, i) => (
                      <div
                        key={i}
                        onClick={() => focusOnNode(item.node.id)}
                        style={{
                          padding: '4px 6px', background: 'rgba(0, 240, 255, 0.05)',
                          borderLeft: `2px solid #00f0ff`, cursor: 'pointer', fontSize: 10,
                          display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                        }}
                      >
                        <span style={{ color: '#ffffff', fontWeight: 600 }}>← {item.node.label}</span>
                        <span className="font-mono" style={{ color: 'var(--text-dim)', fontSize: 9 }}>{item.relation}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* 📤 DOWNSTREAM DATA FLOW (Outputs & Callees) */}
              <div style={{ marginBottom: 10 }}>
                <div className="font-hud" style={{ fontSize: 10, color: '#ff007f', marginBottom: 4, display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span>📤 OUTGOING DATA FLOW (TARGETS)</span>
                  <span className="font-mono" style={{ fontSize: 9, color: 'var(--text-dim)' }}>({dataFlowBreakdown.downstream.length})</span>
                </div>
                <div style={{ maxHeight: 110, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 3 }}>
                  {dataFlowBreakdown.downstream.length === 0 ? (
                    <div style={{ fontSize: 10, color: 'var(--text-dim)', fontStyle: 'italic' }}>No outgoing flows detected (Leaf Target)</div>
                  ) : (
                    dataFlowBreakdown.downstream.map((item, i) => (
                      <div
                        key={i}
                        onClick={() => focusOnNode(item.node.id)}
                        style={{
                          padding: '4px 6px', background: 'rgba(255, 0, 127, 0.05)',
                          borderLeft: `2px solid #ff007f`, cursor: 'pointer', fontSize: 10,
                          display: 'flex', justifyContent: 'space-between', alignItems: 'center'
                        }}
                      >
                        <span style={{ color: '#ffffff', fontWeight: 600 }}>→ {item.node.label}</span>
                        <span className="font-mono" style={{ color: 'var(--text-dim)', fontSize: 9 }}>{item.relation}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>

            </section>
          )}

          {/* ── Bottom Telemetry Status Bar ───────────────────────────────── */}
          <footer className="hud-panel corner-brackets" style={{
            position: 'absolute', bottom: 10, left: 16, right: 16, height: 34,
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '0 16px', zIndex: 10, fontSize: 11
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <span className="font-mono" style={{ color: 'var(--text-dim)' }}>
                DATA_FLOW: <b style={{ color: dataFlowStreaming ? '#00f0ff' : '#ff007f' }}>{dataFlowStreaming ? 'ACTIVE STREAM' : 'STATIC'}</b>
              </span>
              <span style={{ color: 'var(--border-cyber)' }}>&middot;</span>
              <span className="font-mono" style={{ color: 'var(--text-dim)' }}>
                PACKETS: <b style={{ color: '#00ff88' }}>DIRECTIONAL [SRC ➔ TGT]</b>
              </span>
              <span style={{ color: 'var(--border-cyber)' }}>&middot;</span>
              <span className="font-mono" style={{ color: 'var(--text-dim)' }}>
                COLOR CODE: <b style={{ color: '#00f0ff' }}>CYAN=INFLOW</b> | <b style={{ color: '#ff007f' }}>MAGENTA=OUTFLOW</b>
              </span>
            </div>

            <div className="font-mono" style={{ color: 'var(--neon-cyan)', fontSize: 10 }}>
              COORDINATES: [X: {cursorCoords.x}px | Y: {cursorCoords.y}px]
            </div>
          </footer>

        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""
    final_html = template.replace("__GRAPH_DATA_PLACEHOLDER__", embedded_data_json)
    Path("graphify-out/graph.html").write_text(final_html, encoding="utf-8")
    print("Successfully built Sci-Fi Data Flow React graph in graphify-out/graph.html!")


if __name__ == "__main__":
    generate_react_html()
