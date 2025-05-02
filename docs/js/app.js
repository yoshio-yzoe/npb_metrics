// docs/js/app.js
async function main() {
    // ---------- 1. データ取得 ----------
    const [players, meta] = await Promise.all([
      fetch("data/players.json").then((r) => r.json()),
      fetch("last_update.txt").then((r) => r.text()).catch(() => ""),
    ]);
    document.getElementById("update").textContent = meta.trim();
  
    // ---------- 2. セレクトボックス生成 ----------
    const years = [...new Set(players.map((d) => d.year))].sort().reverse();
    const teams = [...new Set(players.map((d) => d.team))].sort();
  
    const yearSel = document.getElementById("year");
    const teamSel = document.getElementById("team");
  
    years.forEach((y) => (yearSel.innerHTML += `<option>${y}</option>`));
    teamSel.innerHTML += `<option value="">ALL</option>`;
    teams.forEach((t) => (teamSel.innerHTML += `<option>${t}</option>`));
  
    // ---------- 3. DataTable 初期化 ----------
    const table = new DataTable("#tbl", {
      data: [],
      columns: Object.keys(players[0]).map((k) => ({ title: k, data: k })),
      pageLength: 25,
      order: [[0, "asc"]], // デフォルト並び：Age 昇順（適宜変更）
    });
  
    // ---------- 4. 絞り込み関数 ----------
    function refresh() {
      const y = yearSel.value;
      const t = teamSel.value;
      const filtered = players.filter(
        (d) => d.year == y && (t === "" || d.team === t)
      );
      table.clear().rows.add(filtered).draw();
    }
  
    yearSel.addEventListener("change", refresh);
    teamSel.addEventListener("change", refresh);
  
    // 初期表示：最新年度 + ALL チーム
    yearSel.value = years[0];
    teamSel.value = "";
    refresh();
  }
  
  main();
  