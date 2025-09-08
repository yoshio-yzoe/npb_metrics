// docs/js/app.js
async function main() {
    // ---------- 1. データ取得 ----------
    const [allPlayers, batterData, pitcherData, meta] = await Promise.all([
      fetch("data/all_players.json").then((r) => r.json()),
      fetch("data/batter.json").then((r) => r.json()),
      fetch("data/pitcher.json").then((r) => r.json()),
      fetch("last_update.txt").then((r) => r.text()).catch(() => ""),
    ]);
    document.getElementById("update").textContent = meta.trim();
  
    let currentData = allPlayers;
    let table = null;
  
    // ---------- 2. セレクトボックス生成 ----------
    function setupSelects() {
      const years = [...new Set(currentData.map((d) => d.year))].sort().reverse();
      const teams = [...new Set(currentData.map((d) => d.team))].sort();
    
      const yearSel = document.getElementById("year");
      const teamSel = document.getElementById("team");
    
      yearSel.innerHTML = "";
      teamSel.innerHTML = "";
      
      years.forEach((y) => (yearSel.innerHTML += `<option>${y}</option>`));
      teamSel.innerHTML += `<option value="">ALL</option>`;
      teams.forEach((t) => (teamSel.innerHTML += `<option>${t}</option>`));
      
      // 初期値設定
      yearSel.value = years[0];
      teamSel.value = "";
    }
  
    // ---------- 3. DataTable 初期化 ----------
    function initTable() {
      if (table) {
        table.destroy();
        document.getElementById("tbl").innerHTML = "";
      }
      
      if (currentData.length === 0) return;
      
      table = new DataTable("#tbl", {
        data: [],
        columns: Object.keys(currentData[0]).map((k) => ({ title: k, data: k })),
        pageLength: 25,
        order: [[0, "asc"]],
        scrollX: true
      });
    }
  
    // ---------- 4. 絞り込み関数 ----------
    function refresh() {
      if (!table) return;
      
      const y = document.getElementById("year").value;
      const t = document.getElementById("team").value;
      const filtered = currentData.filter(
        (d) => d.year == y && (t === "" || d.team === t)
      );
      table.clear().rows.add(filtered).draw();
    }
  
    // ---------- 5. データタイプ切り替え ----------
    const typeSel = document.getElementById("dataType");
    typeSel.addEventListener("change", () => {
      switch(typeSel.value) {
        case "all":
          currentData = allPlayers;
          break;
        case "batter":
          currentData = batterData;
          break;
        case "pitcher":
          currentData = pitcherData;
          break;
      }
      setupSelects();
      initTable();
      refresh();
    });
    
    document.getElementById("year").addEventListener("change", refresh);
    document.getElementById("team").addEventListener("change", refresh);
  
    // 初期表示
    setupSelects();
    initTable();
    refresh();
  }
  
  main();
  