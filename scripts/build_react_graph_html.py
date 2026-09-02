import json
from pathlib import Path

def generate_react_html():
    graph_path = Path('graphify-out/graph.json')
    labels_path = Path('graphify-out/.graphify_labels.json')
    
    graph_data = json.loads(graph_path.read_text(encoding="utf-8")) if graph_path.exists() else {"nodes": [], "links": [], "hyperedges": []}
    labels_data = json.loads(labels_path.read_text(encoding="utf-8")) if labels_path.exists() else {}
    
    # Calculate community colors and counts
    PALETTE = [
        "#6366F1", "#EC4899", "#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", 
        "#EF4444", "#06B6D4", "#14B8A6", "#84CC16", "#F97316", "#A855F7", 
        "#D946EF", "#0EA5E9", "#64748B", "#E11D48", "#059669", "#D97706", 
        "#7C3AED", "#2563EB", "#DB2777", "#4F46E5", "#0284C7", "#16A34A", 
        "#CA8A04", "#DC2626", "#9333EA", "#C026D3", "#0891B2", "#475569"
    ]
    
    nodes = graph_data.get('nodes', [])
    links = graph_data.get('links', [])
    hyperedges = graph_data.get('hyperedges', [])
    
    # Degree calculation
    degree_map = {}
    in_degree_map = {}
    out_degree_map = {}
    adj_map = {}
    
    for n in nodes:
        nid = n['id']
        degree_map[nid] = 0
        in_degree_map[nid] = 0
        out_degree_map[nid] = 0
        adj_map[nid] = []
        
    for l in links:
        src = l['source']
        tgt = l['target']
        if src in degree_map:
            degree_map[src] += 1
            out_degree_map[src] += 1
            adj_map[src].append({'target': tgt, 'relation': l.get('relation', 'connected'), 'confidence': l.get('confidence', 'EXTRACTED'), 'direction': 'out'})
        if tgt in degree_map:
            degree_map[tgt] += 1
            in_degree_map[tgt] += 1
            adj_map[tgt].append({'target': src, 'relation': l.get('relation', 'connected'), 'confidence': l.get('confidence', 'EXTRACTED'), 'direction': 'in'})
            
    # Community stats
    comm_stats = {}
    for n in nodes:
        cid = n.get('community', 0)
        cname = labels_data.get(str(cid), n.get('community_name', f"Community {cid}"))
        n['community_name'] = cname
        n['degree'] = degree_map.get(n['id'], 0)
        n['in_degree'] = in_degree_map.get(n['id'], 0)
        n['out_degree'] = out_degree_map.get(n['id'], 0)
        color = PALETTE[cid % len(PALETTE)]
        n['color'] = color
        
        if cid not in comm_stats:
            comm_stats[cid] = {'cid': cid, 'name': cname, 'count': 0, 'color': color}
        comm_stats[cid]['count'] += 1

    communities_list = sorted(list(comm_stats.values()), key=lambda x: x['count'], reverse=True)
    
    # God nodes
    god_nodes = sorted(nodes, key=lambda x: x['degree'], reverse=True)[:15]
    
    embedded_data_json = json.dumps({
        'nodes': nodes,
        'links': links,
        'hyperedges': hyperedges,
        'communities': communities_list,
        'godNodes': [{'id': n['id'], 'label': n['label'], 'degree': n['degree'], 'community_name': n['community_name'], 'color': n['color'], 'file_type': n.get('file_type', 'code')} for n in god_nodes],
        'totalNodes': len(nodes),
        'totalLinks': len(links),
        'totalCommunities': len(communities_list)
    }, ensure_ascii=False)

    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aegis Analytics — Graphify Knowledge Explorer</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <!-- Vis Network -->
  <script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"></script>
  
  <!-- React 18 & Babel CDN -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <style>
    :root {
      --bg-primary: #07080d;
      --bg-secondary: #0f1019;
      --bg-card: rgba(18, 20, 32, 0.85);
      --bg-card-hover: rgba(28, 31, 50, 0.9);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-bright: rgba(99, 102, 241, 0.35);
      --accent-indigo: #6366f1;
      --accent-purple: #a855f7;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --text-primary: #f1f5f9;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --glow-primary: 0 0 25px rgba(99, 102, 241, 0.25);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background: var(--bg-primary);
      color: var(--text-primary);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    code, pre, .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(99, 102, 241, 0.5);
    }

    #root {
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* Glassmorphism Classes */
    .glass-panel {
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
    }

    .glass-panel-glow {
      background: var(--bg-card);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-bright);
      box-shadow: var(--glow-primary);
    }

    .gradient-text {
      background: linear-gradient(135deg, #a5b4fc 0%, #6366f1 50%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      border: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-primary);
    }

    .btn:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }

    .btn-primary {
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      border-color: rgba(255, 255, 255, 0.2);
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.02em;
    }

    /* Graph Canvas */
    #graph-container {
      flex: 1;
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
      background: radial-gradient(circle at 50% 50%, #111322 0%, #07080d 100%);
    }
  </style>
</head>
<body>
  <div id="root"></div>

  <script>
    window.GRAPH_DATA = __GRAPH_DATA_PLACEHOLDER__;
  </script>

  <script type="text/babel">
    const { useState, useEffect, useRef, useMemo } = React;

    // SVG Icons
    const Icons = {
      Logo: () => (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" style={{ color: '#818cf8' }}>
          <circle cx="12" cy="12" r="3" />
          <path d="M12 3v3m0 12v3M3 12h3m12 0h3M5.6 5.6l2.1 2.1m8.6 8.6l2.1 2.1M5.6 18.4l2.1-2.1m8.6-8.6l2.1-2.1" />
        </svg>
      ),
      Search: () => (
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      ),
      Layers: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
      ),
      Filter: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
        </svg>
      ),
      Zap: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
      ),
      Route: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="6" cy="19" r="3"></circle>
          <path d="M9 19h8.5a4.5 4.5 0 0 0 0-9H5a4 4 0 0 1 0-8h10"></path>
          <circle cx="18" cy="5" r="3"></circle>
        </svg>
      ),
      ZoomIn: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          <line x1="11" y1="8" x2="11" y2="14"></line>
          <line x1="8" y1="11" x2="14" y2="11"></line>
        </svg>
      ),
      ZoomOut: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          <line x1="8" y1="11" x2="14" y2="11"></line>
        </svg>
      ),
      Fit: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"></path>
        </svg>
      ),
      Play: () => (
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
      ),
      Pause: () => (
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
          <rect x="6" y="4" width="4" height="16"></rect>
          <rect x="14" y="4" width="4" height="16"></rect>
        </svg>
      ),
      Camera: () => (
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
          <circle cx="12" cy="13" r="4"></circle>
        </svg>
      ),
      Close: () => (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      ),
      Copy: () => (
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      )
    };

    function App() {
      const data = window.GRAPH_DATA || { nodes: [], links: [], hyperedges: [], communities: [], godNodes: [] };
      
      // State
      const [network, setNetwork] = useState(null);
      const [selectedNodeId, setSelectedNodeId] = useState(null);
      const [searchQuery, setSearchQuery] = useState('');
      const [activeTab, setActiveTab] = useState('communities');
      const [visibleCommunities, setVisibleCommunities] = useState(new Set(data.communities.map(c => c.cid)));
      const [typeFilters, setTypeFilters] = useState({ code: true, document: true, image: true, concept: true });
      const [minDegree, setMinDegree] = useState(0);
      const [physicsEnabled, setPhysicsEnabled] = useState(false);
      const [isSidebarOpen, setIsSidebarOpen] = useState(true);
      const [isInspectorOpen, setIsInspectorOpen] = useState(false);
      const [pathStart, setPathStart] = useState(null);
      const [pathEnd, setPathEnd] = useState(null);
      const [shortestPath, setShortestPath] = useState(null);
      const [copySuccess, setCopySuccess] = useState(false);
      
      const containerRef = useRef(null);
      const nodesDSRef = useRef(null);
      const edgesDSRef = useRef(null);

      // Node Map for instant lookup
      const nodeMap = useMemo(() => {
        const map = new Map();
        data.nodes.forEach(n => map.set(n.id, n));
        return map;
      }, [data.nodes]);

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

      // Initialize Vis Network
      useEffect(() => {
        if (!containerRef.current) return;

        const visNodes = data.nodes.map(n => ({
          id: n.id,
          label: n.label,
          color: {
            background: n.color,
            border: n.color,
            highlight: { background: '#ffffff', border: n.color }
          },
          size: Math.max(10, Math.min(32, 10 + Math.sqrt(n.degree || 1) * 3)),
          font: { size: n.degree > 10 ? 12 : 0, color: '#ffffff', face: 'Inter' },
          title: `${n.label} (${n.community_name})`,
          _raw: n
        }));

        const visEdges = data.links.map((e, idx) => ({
          id: idx,
          from: e.source,
          to: e.target,
          dashes: e.confidence === 'INFERRED',
          width: e.confidence === 'INFERRED' ? 1.5 : 2,
          color: { color: e.confidence === 'INFERRED' ? '#818cf8' : 'rgba(148, 163, 184, 0.45)', opacity: 0.7 },
          arrows: { to: { enabled: true, scaleFactor: 0.5 } },
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
              gravitationalConstant: -70,
              centralGravity: 0.006,
              springLength: 130,
              springConstant: 0.08,
              damping: 0.45,
              avoidOverlap: 0.85
            },
            stabilization: { iterations: 220, fit: true }
          },
          interaction: {
            hover: true,
            tooltipDelay: 100,
            hideEdgesOnDrag: true,
            zoomView: true,
            dragView: true
          },
          nodes: {
            shape: 'dot',
            borderWidth: 1.5,
            shadow: { enabled: true, color: 'rgba(0,0,0,0.6)', size: 8, x: 2, y: 2 }
          },
          edges: {
            smooth: { type: 'continuous', roundness: 0.2 },
            selectionWidth: 3
          }
        };

        const net = new vis.Network(containerRef.current, { nodes: nodesDS, edges: edgesDS }, options);

        net.once('stabilizationIterationsDone', () => {
          net.setOptions({ physics: { enabled: false } });
          setPhysicsEnabled(false);
        });

        net.on('click', (params) => {
          if (params.nodes.length > 0) {
            const nid = params.nodes[0];
            setSelectedNodeId(nid);
            setIsInspectorOpen(true);
          } else {
            setSelectedNodeId(null);
          }
        });

        // Hyperedge convex hull overlay
        net.on('afterDrawing', (ctx) => {
          (data.hyperedges || []).forEach(h => {
            const positions = h.nodes
              .map(nid => net.getPositions([nid])[nid])
              .filter(p => p !== undefined);
            if (positions.length < 2) return;
            
            ctx.save();
            ctx.globalAlpha = 0.15;
            ctx.fillStyle = '#6366f1';
            ctx.strokeStyle = '#818cf8';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            const cx = positions.reduce((s, p) => s + p.x, 0) / positions.length;
            const cy = positions.reduce((s, p) => s + p.y, 0) / positions.length;
            
            positions.forEach((p, i) => {
              if (i === 0) ctx.moveTo(p.x, p.y);
              else ctx.lineTo(p.x, p.y);
            });
            ctx.closePath();
            ctx.fill();
            ctx.globalAlpha = 0.5;
            ctx.stroke();
            
            ctx.globalAlpha = 0.9;
            ctx.fillStyle = '#c7d2fe';
            ctx.font = 'bold 12px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(h.label, cx, cy - 8);
            ctx.restore();
          });
        });

        setNetwork(net);

        return () => {
          net.destroy();
        };
      }, []);

      // Filter updates to Vis DataSet
      useEffect(() => {
        if (!nodesDSRef.current) return;

        const updates = data.nodes.map(n => {
          const commVisible = visibleCommunities.has(n.community);
          const typeVisible = typeFilters[n.file_type || 'code'] !== false;
          const degVisible = (n.degree || 0) >= minDegree;
          const isHidden = !(commVisible && typeVisible && degVisible);

          return {
            id: n.id,
            hidden: isHidden
          };
        });

        nodesDSRef.current.update(updates);
      }, [visibleCommunities, typeFilters, minDegree]);

      // Focus node helper
      const focusOnNode = (nodeId) => {
        if (!network) return;
        network.focus(nodeId, {
          scale: 1.5,
          animation: { duration: 700, easingFunction: 'easeInOutQuad' }
        });
        network.selectNodes([nodeId]);
        setSelectedNodeId(nodeId);
        setIsInspectorOpen(true);
      };

      // Toggle Physics
      const togglePhysics = () => {
        if (!network) return;
        const next = !physicsEnabled;
        network.setOptions({ physics: { enabled: next } });
        setPhysicsEnabled(next);
      };

      // Fit Screen
      const fitScreen = () => {
        if (network) network.fit({ animation: { duration: 600 } });
      };

      // Take Screenshot
      const takeScreenshot = () => {
        if (!containerRef.current) return;
        const canvas = containerRef.current.querySelector('canvas');
        if (!canvas) return;
        const image = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = 'aegis-knowledge-graph.png';
        link.href = image;
        link.click();
      };

      // Selected Node details
      const selectedNode = useMemo(() => {
        return selectedNodeId ? nodeMap.get(selectedNodeId) : null;
      }, [selectedNodeId, nodeMap]);

      // Neighbors of selected node
      const neighbors = useMemo(() => {
        if (!selectedNodeId) return [];
        const conns = adjGraph.get(selectedNodeId) || [];
        return conns.map(c => ({
          ...c,
          targetNode: nodeMap.get(c.node)
        })).filter(c => c.targetNode);
      }, [selectedNodeId, adjGraph, nodeMap]);

      // Shortest Path Finder (BFS)
      const findShortestPath = (srcId, dstId) => {
        if (!srcId || !dstId || srcId === dstId) return;
        
        const queue = [[srcId]];
        const visited = new Set([srcId]);
        let foundPath = null;

        while (queue.length > 0) {
          const path = queue.shift();
          const curr = path[path.length - 1];

          if (curr === dstId) {
            foundPath = path;
            break;
          }

          const conns = adjGraph.get(curr) || [];
          for (const c of conns) {
            if (!visited.has(c.node)) {
              visited.add(c.node);
              queue.push([...path, c.node]);
            }
          }
        }

        setShortestPath(foundPath);

        if (foundPath && nodesDSRef.current && network) {
          const pathSet = new Set(foundPath);
          const updates = data.nodes.map(n => ({
            id: n.id,
            color: pathSet.has(n.id) 
              ? { background: '#f59e0b', border: '#ffffff' }
              : { background: 'rgba(255,255,255,0.05)', border: 'rgba(255,255,255,0.1)' },
            font: { size: pathSet.has(n.id) ? 14 : 0, color: '#ffffff' }
          }));
          nodesDSRef.current.update(updates);
          network.fit({ nodes: foundPath, animation: true });
        }
      };

      // Reset Path Highlight
      const resetHighlight = () => {
        setShortestPath(null);
        if (nodesDSRef.current) {
          const updates = data.nodes.map(n => ({
            id: n.id,
            color: {
              background: n.color,
              border: n.color,
              highlight: { background: '#ffffff', border: n.color }
            },
            font: { size: n.degree > 10 ? 12 : 0, color: '#ffffff' }
          }));
          nodesDSRef.current.update(updates);
        }
      };

      // Search matching nodes
      const searchMatches = useMemo(() => {
        if (!searchQuery.trim()) return [];
        const q = searchQuery.toLowerCase();
        return data.nodes.filter(n => 
          n.label.toLowerCase().includes(q) || 
          (n.source_file && n.source_file.toLowerCase().includes(q))
        ).slice(0, 12);
      }, [searchQuery, data.nodes]);

      // Copy helper
      const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      };

      return (
        <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
          
          {/* Main Canvas */}
          <div id="graph-container" ref={containerRef} />

          {/* Top Navbar */}
          <header className="glass-panel" style={{
            position: 'absolute', top: 12, left: 16, right: 16, height: 56,
            borderRadius: 14, zIndex: 10, display: 'flex', alignItems: 'center',
            justifyContent: 'space-between', padding: '0 16px', border: '1px solid var(--border-subtle)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{
                  width: 34, height: 34, borderRadius: 10, background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 15px rgba(99,102,241,0.4)'
                }}>
                  <Icons.Logo />
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 14, letterSpacing: '-0.01em' }}>
                    <span className="gradient-text">AEGIS</span> <span style={{ color: '#94a3b8', fontWeight: 500 }}>GRAPH</span>
                  </div>
                  <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Project Knowledge Graph</div>
                </div>
              </div>

              {/* Stats badges */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginLeft: 12 }}>
                <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
                  {data.totalNodes} Nodes
                </span>
                <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.15)', color: '#67e8f9', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                  {data.totalLinks} Edges
                </span>
                <span className="badge" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#d8b4fe', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
                  {data.totalCommunities} Communities
                </span>
              </div>
            </div>

            {/* Center Live Search Bar */}
            <div style={{ position: 'relative', width: 340 }}>
              <div style={{
                display: 'flex', alignItems: 'center', gap: 8, background: 'rgba(0, 0, 0, 0.35)',
                border: '1px solid var(--border-subtle)', borderRadius: 10, padding: '7px 12px'
              }}>
                <span style={{ color: 'var(--text-muted)' }}><Icons.Search /></span>
                <input
                  type="text"
                  placeholder="Search functions, classes, models, files..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{
                    background: 'transparent', border: 'none', color: '#f8fafc',
                    fontSize: 13, width: '100%', outline: 'none'
                  }}
                />
                {searchQuery && (
                  <button onClick={() => setSearchQuery('')} style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer' }}>
                    <Icons.Close />
                  </button>
                )}
              </div>

              {/* Autocomplete Dropdown */}
              {searchMatches.length > 0 && (
                <div className="glass-panel" style={{
                  position: 'absolute', top: 46, left: 0, right: 0, maxHeight: 280,
                  overflowY: 'auto', borderRadius: 10, padding: 6, zIndex: 50,
                  boxShadow: '0 10px 25px rgba(0,0,0,0.5)', border: '1px solid var(--border-bright)'
                }}>
                  {searchMatches.map(m => (
                    <div
                      key={m.id}
                      onClick={() => {
                        focusOnNode(m.id);
                        setSearchQuery('');
                      }}
                      style={{
                        padding: '8px 10px', borderRadius: 6, cursor: 'pointer',
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        transition: 'background 0.15s', fontSize: 13
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.08)'}
                      onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div style={{ width: 8, height: 8, borderRadius: '50%', background: m.color }} />
                        <span style={{ fontWeight: 600, color: '#f1f5f9' }}>{m.label}</span>
                      </div>
                      <span style={{ fontSize: 11, color: '#94a3b8' }}>{m.community_name}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Right Quick Controls */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <button 
                className="btn" 
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                style={{ background: isSidebarOpen ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255,255,255,0.04)', borderColor: isSidebarOpen ? '#6366f1' : 'var(--border-subtle)' }}
              >
                <Icons.Layers />
                <span>Explorer</span>
              </button>

              <button className="btn" onClick={fitScreen} title="Fit Entire Graph to View">
                <Icons.Fit />
                <span>Fit</span>
              </button>

              <button 
                className="btn" 
                onClick={togglePhysics}
                style={{ background: physicsEnabled ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255,255,255,0.04)', borderColor: physicsEnabled ? '#10b981' : 'var(--border-subtle)' }}
                title="Toggle Real-Time Force Simulation"
              >
                {physicsEnabled ? <Icons.Pause /> : <Icons.Play />}
                <span>{physicsEnabled ? 'Stabilizing' : 'Simulate'}</span>
              </button>

              <button className="btn" onClick={takeScreenshot} title="Save High-Res PNG Screenshot">
                <Icons.Camera />
              </button>
            </div>
          </header>

          {/* Left Floating Sidebar */}
          {isSidebarOpen && (
            <aside className="glass-panel" style={{
              position: 'absolute', top: 80, left: 16, width: 320, bottom: 20,
              borderRadius: 14, zIndex: 10, display: 'flex', flexDirection: 'column',
              overflow: 'hidden', border: '1px solid var(--border-subtle)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.4)'
            }}>
              {/* Tab Selector */}
              <div style={{ display: 'flex', borderBottom: '1px solid var(--border-subtle)', background: 'rgba(0,0,0,0.2)' }}>
                {[
                  { id: 'communities', label: 'Clusters', icon: <Icons.Layers /> },
                  { id: 'intelligence', label: 'God Nodes', icon: <Icons.Zap /> },
                  { id: 'pathfinder', label: 'Path', icon: <Icons.Route /> },
                  { id: 'filters', label: 'Filters', icon: <Icons.Filter /> }
                ].map(t => (
                  <button
                    key={t.id}
                    onClick={() => setActiveTab(t.id)}
                    style={{
                      flex: 1, padding: '10px 4px', background: activeTab === t.id ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
                      border: 'none', borderBottom: activeTab === t.id ? '2px solid #6366f1' : '2px solid transparent',
                      color: activeTab === t.id ? '#f1f5f9' : '#94a3b8', fontSize: 12, fontWeight: 600,
                      cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
                      transition: 'all 0.2s'
                    }}
                  >
                    {t.icon}
                    <span>{t.label}</span>
                  </button>
                ))}
              </div>

              {/* Tab Contents */}
              <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
                
                {/* 1. Communities Tab */}
                {activeTab === 'communities' && (
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
                        Architectural Communities
                      </span>
                      <div style={{ display: 'flex', gap: 6 }}>
                        <button
                          onClick={() => setVisibleCommunities(new Set(data.communities.map(c => c.cid)))}
                          style={{ background: 'none', border: 'none', color: '#818cf8', fontSize: 11, cursor: 'pointer' }}
                        >
                          Show All
                        </button>
                        <span style={{ color: 'var(--text-muted)' }}>&middot;</span>
                        <button
                          onClick={() => setVisibleCommunities(new Set())}
                          style={{ background: 'none', border: 'none', color: '#f43f5e', fontSize: 11, cursor: 'pointer' }}
                        >
                          Clear
                        </button>
                      </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                      {data.communities.map(c => {
                        const isVisible = visibleCommunities.has(c.cid);
                        return (
                          <div
                            key={c.cid}
                            style={{
                              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                              padding: '6px 8px', borderRadius: 8, cursor: 'pointer',
                              background: isVisible ? 'rgba(255,255,255,0.03)' : 'transparent',
                              opacity: isVisible ? 1 : 0.45, transition: 'all 0.15s',
                              borderLeft: `3px solid ${c.color}`
                            }}
                            onClick={() => {
                              const next = new Set(visibleCommunities);
                              if (next.has(c.cid)) next.delete(c.cid);
                              else next.add(c.cid);
                              setVisibleCommunities(next);
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8, overflow: 'hidden' }}>
                              <input
                                type="checkbox"
                                checked={isVisible}
                                onChange={() => {}}
                                style={{ accentColor: c.color, cursor: 'pointer' }}
                              />
                              <span style={{ fontSize: 12, fontWeight: 500, color: '#f1f5f9', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                                {c.name}
                              </span>
                            </div>
                            <span style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, paddingLeft: 6 }}>
                              {c.count}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* 2. God Nodes & Intelligence Tab */}
                {activeTab === 'intelligence' && (
                  <div>
                    <div style={{ marginBottom: 12 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
                        Core Abstractions (Top God Nodes)
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                      {data.godNodes.map((n, i) => (
                        <div
                          key={n.id}
                          onClick={() => focusOnNode(n.id)}
                          style={{
                            padding: '8px 10px', borderRadius: 8, background: 'rgba(255,255,255,0.03)',
                            border: '1px solid var(--border-subtle)', cursor: 'pointer', transition: 'all 0.15s'
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.borderColor = 'rgba(99,102,241,0.4)'}
                          onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-subtle)'}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 2 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                              <span style={{ fontSize: 11, fontWeight: 700, color: '#818cf8' }}>#{i+1}</span>
                              <span style={{ fontSize: 13, fontWeight: 600, color: '#f8fafc' }}>{n.label}</span>
                            </div>
                            <span className="badge" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }}>
                              {n.degree} edges
                            </span>
                          </div>
                          <div style={{ fontSize: 11, color: '#94a3b8' }}>
                            {n.community_name}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 3. Shortest Path Finder */}
                {activeTab === 'pathfinder' && (
                  <div>
                    <div style={{ marginBottom: 10 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
                        Shortest Path Finder
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                      <div>
                        <label style={{ fontSize: 11, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Source Node</label>
                        <select
                          value={pathStart || ''}
                          onChange={(e) => setPathStart(e.target.value)}
                          style={{
                            width: '100%', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-subtle)',
                            color: '#f8fafc', padding: '6px 8px', borderRadius: 6, fontSize: 12, outline: 'none'
                          }}
                        >
                          <option value="">Select origin node...</option>
                          {data.nodes.map(n => <option key={n.id} value={n.id}>{n.label} ({n.community_name})</option>)}
                        </select>
                      </div>

                      <div>
                        <label style={{ fontSize: 11, color: '#94a3b8', display: 'block', marginBottom: 4 }}>Target Node</label>
                        <select
                          value={pathEnd || ''}
                          onChange={(e) => setPathEnd(e.target.value)}
                          style={{
                            width: '100%', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-subtle)',
                            color: '#f8fafc', padding: '6px 8px', borderRadius: 6, fontSize: 12, outline: 'none'
                          }}
                        >
                          <option value="">Select target node...</option>
                          {data.nodes.map(n => <option key={n.id} value={n.id}>{n.label} ({n.community_name})</option>)}
                        </select>
                      </div>

                      <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
                        <button
                          className="btn btn-primary"
                          style={{ flex: 1 }}
                          onClick={() => findShortestPath(pathStart, pathEnd)}
                          disabled={!pathStart || !pathEnd}
                        >
                          Find Route
                        </button>
                        <button
                          className="btn"
                          onClick={resetHighlight}
                        >
                          Reset
                        </button>
                      </div>

                      {shortestPath && (
                        <div style={{ marginTop: 10, padding: 10, borderRadius: 8, background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.3)' }}>
                          <div style={{ fontSize: 12, fontWeight: 700, color: '#f59e0b', marginBottom: 6 }}>
                            Path Found ({shortestPath.length - 1} hops)
                          </div>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                            {shortestPath.map((nid, idx) => {
                              const node = nodeMap.get(nid);
                              return (
                                <div key={nid} style={{ fontSize: 12, color: '#f1f5f9', display: 'flex', alignItems: 'center', gap: 6 }}>
                                  <span style={{ color: '#94a3b8' }}>{idx + 1}.</span>
                                  <span style={{ fontWeight: 600, cursor: 'pointer', color: '#67e8f9' }} onClick={() => focusOnNode(nid)}>
                                    {node ? node.label : nid}
                                  </span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* 4. Filters Tab */}
                {activeTab === 'filters' && (
                  <div>
                    <div style={{ marginBottom: 12 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
                        Graph Filtering
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                      <div>
                        <label style={{ fontSize: 12, color: '#94a3b8', display: 'block', marginBottom: 6 }}>Entity File Type</label>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                          {['code', 'document', 'image', 'concept'].map(t => (
                            <button
                              key={t}
                              className="btn"
                              onClick={() => setTypeFilters(prev => ({ ...prev, [t]: !prev[t] }))}
                              style={{
                                fontSize: 11, padding: '4px 8px',
                                background: typeFilters[t] ? 'rgba(99,102,241,0.2)' : 'rgba(0,0,0,0.3)',
                                borderColor: typeFilters[t] ? '#6366f1' : 'var(--border-subtle)'
                              }}
                            >
                              {t}
                            </button>
                          ))}
                        </div>
                      </div>

                      <div>
                        <label style={{ fontSize: 12, color: '#94a3b8', display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <span>Min Connections (Degree)</span>
                          <span style={{ fontWeight: 700, color: '#f8fafc' }}>{minDegree}</span>
                        </label>
                        <input
                          type="range"
                          min="0"
                          max="20"
                          value={minDegree}
                          onChange={(e) => setMinDegree(parseInt(e.target.value))}
                          style={{ width: '100%', accentColor: '#6366f1' }}
                        />
                      </div>
                    </div>
                  </div>
                )}

              </div>
            </aside>
          )}

          {/* Right Floating Node Inspector */}
          {isInspectorOpen && selectedNode && (
            <div className="glass-panel" style={{
              position: 'absolute', top: 80, right: 16, width: 340, bottom: 20,
              borderRadius: 14, zIndex: 10, display: 'flex', flexDirection: 'column',
              overflow: 'hidden', border: '1px solid var(--border-bright)',
              boxShadow: '0 10px 40px rgba(0,0,0,0.6)'
            }}>
              {/* Inspector Header */}
              <div style={{
                padding: '14px 16px', borderBottom: '1px solid var(--border-subtle)',
                background: 'rgba(0,0,0,0.25)', display: 'flex', alignItems: 'flex-start',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
                    <div style={{ width: 10, height: 10, borderRadius: '50%', background: selectedNode.color }} />
                    <span className="badge" style={{ background: 'rgba(255,255,255,0.08)', color: '#94a3b8' }}>
                      {selectedNode.file_type || 'code'}
                    </span>
                    <span className="badge" style={{ background: 'rgba(99,102,241,0.15)', color: '#a5b4fc' }}>
                      {selectedNode.community_name}
                    </span>
                  </div>
                  <h3 style={{ fontSize: 16, fontWeight: 700, color: '#f8fafc', wordBreak: 'break-all' }}>
                    {selectedNode.label}
                  </h3>
                </div>
                <button
                  onClick={() => setIsInspectorOpen(false)}
                  style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: 4 }}
                >
                  <Icons.Close />
                </button>
              </div>

              {/* Inspector Body */}
              <div style={{ flex: 1, overflowY: 'auto', padding: 16, display: 'flex', flexDirection: 'column', gap: 14 }}>
                
                {/* File Location */}
                {selectedNode.source_file && (
                  <div>
                    <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Source File</span>
                    <div style={{
                      marginTop: 4, padding: '6px 10px', background: 'rgba(0,0,0,0.3)',
                      borderRadius: 8, border: '1px solid var(--border-subtle)',
                      display: 'flex', alignItems: 'center', justifyContent: 'space-between'
                    }}>
                      <span className="font-mono" style={{ fontSize: 11, color: '#67e8f9', wordBreak: 'break-all' }}>
                        {selectedNode.source_file} {selectedNode.source_location ? `:${selectedNode.source_location}` : ''}
                      </span>
                      <button
                        onClick={() => copyToClipboard(selectedNode.source_file)}
                        style={{ background: 'none', border: 'none', color: copySuccess ? '#10b981' : '#94a3b8', cursor: 'pointer' }}
                        title="Copy Path"
                      >
                        <Icons.Copy />
                      </button>
                    </div>
                  </div>
                )}

                {/* Metrics */}
                <div>
                  <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Node Metrics</span>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 6 }}>
                    <div style={{ padding: '8px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, textAlign: 'center' }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: '#f8fafc' }}>{selectedNode.degree || 0}</div>
                      <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Total Edges</div>
                    </div>
                    <div style={{ padding: '8px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, textAlign: 'center' }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: '#67e8f9' }}>{selectedNode.in_degree || 0}</div>
                      <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Inbound</div>
                    </div>
                    <div style={{ padding: '8px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, textAlign: 'center' }}>
                      <div style={{ fontSize: 16, fontWeight: 700, color: '#a5b4fc' }}>{selectedNode.out_degree || 0}</div>
                      <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Outbound</div>
                    </div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div style={{ display: 'flex', gap: 6 }}>
                  <button
                    className="btn"
                    style={{ flex: 1, fontSize: 11 }}
                    onClick={() => {
                      setPathStart(selectedNode.id);
                      setActiveTab('pathfinder');
                      setIsSidebarOpen(true);
                    }}
                  >
                    Set as Path Origin
                  </button>
                  <button
                    className="btn"
                    style={{ flex: 1, fontSize: 11 }}
                    onClick={() => {
                      setPathEnd(selectedNode.id);
                      setActiveTab('pathfinder');
                      setIsSidebarOpen(true);
                    }}
                  >
                    Set as Target
                  </button>
                </div>

                {/* Connected Neighbors List */}
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                    <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                      Connected Neighbors ({neighbors.length})
                    </span>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: 4, maxHeight: 220, overflowY: 'auto' }}>
                    {neighbors.map((nb, i) => (
                      <div
                        key={i}
                        onClick={() => focusOnNode(nb.targetNode.id)}
                        style={{
                          padding: '6px 8px', borderRadius: 6, background: 'rgba(255,255,255,0.02)',
                          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                          cursor: 'pointer', transition: 'background 0.15s',
                          borderLeft: `2px solid ${nb.targetNode.color}`
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.07)'}
                        onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                      >
                        <div style={{ overflow: 'hidden' }}>
                          <div style={{ fontSize: 12, fontWeight: 600, color: '#f1f5f9', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                            {nb.targetNode.label}
                          </div>
                          <div style={{ fontSize: 10, color: '#94a3b8' }}>
                            {nb.dir === 'out' ? '→' : '←'} {nb.relation}
                          </div>
                        </div>
                        <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>
                          {nb.targetNode.community_name}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            </div>
          )}

          {/* Bottom Floating Status Bar */}
          <footer className="glass-panel" style={{
            position: 'absolute', bottom: 12, left: 16, right: 16, height: 36,
            borderRadius: 10, zIndex: 10, display: 'flex', alignItems: 'center',
            justifyContent: 'space-between', padding: '0 14px', fontSize: 11,
            color: 'var(--text-muted)', border: '1px solid var(--border-subtle)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span>Engine: <b>React 18 + Vis Network</b></span>
              <span>&middot;</span>
              <span>Layout: <b>ForceAtlas2</b></span>
              <span>&middot;</span>
              <span>Extraction: <b style={{ color: '#10b981' }}>98% Extracted</b></span>
            </div>
            <div>
              <span>Tip: Click any node to open Inspector &middot; Use mousewheel to zoom</span>
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
    Path('graphify-out/graph.html').write_text(final_html, encoding="utf-8")
    print("Successfully reconstructed graphify-out/graph.html using React 18 + Vis Network!")

if __name__ == "__main__":
    generate_react_html()
