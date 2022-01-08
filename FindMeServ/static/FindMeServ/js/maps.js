function checkMap(map) {
    if (map == 'all') {
        for (let map in maps) {
            if (maps[map] == 'all') continue
            document.getElementById('map_' + maps[map]).checked = false
        }
    } else {
        document.getElementById('map_all').checked = false
    }
}