// AIMTV Fame Meter: shared counts from every viewer (Cloudflare Pages Function + D1, binding name "DB").
// GET  /api/score -> {likes:{id:n}, watch:{id:seconds}, boosts:{id:n}}
// POST /api/score  body {likes:{id:n}, watch:{id:seconds}, boosts:{id:n}}  (small batches; capped per request)
const IDS = new Set(["hema","jc","chaibot","tchu","animation","sarla","lata","mrst","fadarr","baba","tabla","dimpy","devi","aimtv","dalmatian","gutter","arnold"]);
const CAP = { likes: 5, watch: 120, boosts: 5, plays: 3 };
const PLAYID = /^(show|song):[a-z0-9_]{1,24}$/;
const KINDS = Object.keys(CAP);
const H = { "content-type": "application/json", "cache-control": "no-store", "access-control-allow-origin": "*" };

async function ensure(db) {
  await db.prepare("CREATE TABLE IF NOT EXISTS score (id TEXT NOT NULL, kind TEXT NOT NULL, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (id, kind))").run();
}
async function totals(db) {
  const out = { likes: {}, watch: {}, boosts: {}, plays: {} };
  const { results } = await db.prepare("SELECT id, kind, n FROM score").all();
  for (const r of results || []) if (out[r.kind]) out[r.kind][r.id] = r.n;
  return out;
}

export async function onRequestGet({ env }) {
  if (!env.DB) return new Response(JSON.stringify({ error: "no database bound" }), { status: 503, headers: H });
  await ensure(env.DB);
  return new Response(JSON.stringify(await totals(env.DB)), { headers: H });
}

export async function onRequestPost({ request, env }) {
  if (!env.DB) return new Response(JSON.stringify({ error: "no database bound" }), { status: 503, headers: H });
  let body;
  try { body = await request.json(); } catch { return new Response("{}", { status: 400, headers: H }); }
  const stmts = [];
  const up = env.DB.prepare("INSERT INTO score (id, kind, n) VALUES (?1, ?2, ?3) ON CONFLICT (id, kind) DO UPDATE SET n = n + ?3");
  for (const kind of KINDS) {
    const m = body && body[kind];
    if (!m || typeof m !== "object") continue;
    for (const [id, v] of Object.entries(m)) {
      const n = Math.floor(Number(v));
      if (!(kind === "plays" ? PLAYID.test(id) : IDS.has(id)) || !(n > 0)) continue;
      stmts.push(up.bind(id, kind, Math.min(n, CAP[kind])));
    }
  }
  await ensure(env.DB);
  if (stmts.length) await env.DB.batch(stmts.slice(0, 40));
  return new Response(JSON.stringify(await totals(env.DB)), { headers: H });
}

export async function onRequestOptions() {
  return new Response(null, { headers: { ...H, "access-control-allow-methods": "GET, POST, OPTIONS", "access-control-allow-headers": "content-type" } });
}
