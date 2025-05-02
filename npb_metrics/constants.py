ROOT_URL = "https://www.baseball-reference.com"

JPCL_TEAMS = {
    "Chunichi Dragons",
    "Hanshin Tigers",
    "Hiroshima Carp",
    "Yakult Swallows",
    "Yokohama Bay Stars",
    "Yomiuri Giants",
}
JPPL_TEAMS = {
    "Chiba Lotte Marines",
    "Fukuoka Softbank Hawks",
    "Hokkaido Nippon Ham Fighters",
    "Orix Buffaloes",
    "Saitama Seibu Lions",
    "Tohoku Rakuten Golden Eagles",
}

TEAM_TO_LEAGUE = {t: "JPCL" for t in JPCL_TEAMS} | {t: "JPPL" for t in JPPL_TEAMS}
VALID_LEAGUES = {"JPCL", "JPPL"}
