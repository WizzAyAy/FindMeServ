function add_players_list(response) {
    if (response['players'].length == 0) {
        showToast()
        return
    }

    let players_list_div = document.getElementById('players_list')
    players_list_div.classList.add('user-select-none')
    players_list_div.classList.remove('visually-hidden')
    players_list_div.innerHTML = ''

    let table = document.createElement('table')
    table.classList.add('table')
    table.classList.add('table-hover')
    table.classList.add('table-borderless')
    table.classList.add('m-0')

    let tableHeader = document.createElement('thead')
    let rowHeader = document.createElement('tr')

    let headers = response['players'] ? response['players'][0] : []
    for (let header in headers) {
        let cell = document.createElement('th')
        cell.setAttribute('scope', 'col')
        let cellText = document.createTextNode(header.toUpperCase())
        cell.appendChild(cellText)
        rowHeader.appendChild(cell)
    }

    tableHeader.appendChild(rowHeader)

    let tableBody = document.createElement('tbody')

    response['players'].forEach((player) => {
        let row = document.createElement('tr')

        for (let attribute in player) {
            let cell = document.createElement('td')
            cell.setAttribute('scope', 'row')
            let cellText = document.createTextNode(player[attribute])

            cell.appendChild(cellText)
            row.appendChild(cell)
        }
        tableBody.appendChild(row)
    })

    table.appendChild(tableHeader)
    table.appendChild(tableBody)
    players_list_div.appendChild(table)
}

function addCard(map, gamemode, ip, port, players, maxPlayers, host, name) {
    let container = document.getElementById('container-server')

    let cardDiv = document.createElement('div')
    cardDiv.classList.add('card')
    cardDiv.classList.add('m-4')
    cardDiv.id = 'card'
    cardDiv.onclick = function (event) {
        closeToast()
        // prevent open list if click join
        if(event.target.nodeName == 'A') return
        let formData = new FormData()
        formData.append('ip', ip)
        formData.append('port', port)
        let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request('/get-players-info/', {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': csrfTokenValue}
        })
        fetch(request)
            .then(response => response.json())
            .then(response => {
                add_players_list(response)
            })
    }


    // Image
    let image = document.createElement('img')
    image.classList.add('card-img-top')
    let image_path = imageExists(static_url + 'FindMeServ/img/' + map + '.jpg') ?
        static_url + 'FindMeServ/img/' + map + '.jpg' :
        static_url + 'FindMeServ/img/de_custom.jpg'

    image.src = image_path

    let cardBodyDiv = document.createElement('div')
    cardBodyDiv.classList.add('card-body')
    cardBodyDiv.classList.add('container-fluid')
    cardBodyDiv.classList.add('bg-light')

    cardDiv.appendChild(image)

    // Name
    let nameDiv = document.createElement('div')
    nameDiv.classList.add('row')

    let nameText = document.createElement('span')
    nameText.classList.add('justify-content-center')
    nameText.classList.add('card-title')
    nameText.classList.add('text-truncate')
    nameText.style.fontSize = 'small'
    nameText.setAttribute('data-bs-toggle', 'tooltip')
    nameText.setAttribute('title', name)
    nameText.innerText = name

    nameDiv.appendChild(nameText)
    cardBodyDiv.appendChild(nameDiv)

    // Host
    let hostDiv = document.createElement('div')
    hostDiv.classList.add('row')

    let hostText = document.createElement('p')
    hostText.classList.add('d-flex')
    hostText.classList.add('justify-content-center')
    hostText.classList.add('card-title')
    hostText.innerText = host

    hostDiv.appendChild(hostText)
    cardBodyDiv.appendChild(hostDiv)

    // Gamemode
    let gamemodeDiv = document.createElement('div')
    gamemodeDiv.classList.add('row')

    let gamemodeText = document.createElement('h5')
    gamemodeText.classList.add('d-flex')
    gamemodeText.classList.add('justify-content-center')
    gamemodeText.classList.add('card-title')
    gamemodeText.innerText = gamemode

    gamemodeDiv.appendChild(gamemodeText)
    cardBodyDiv.appendChild(gamemodeDiv)

    // Player
    let playerDiv = document.createElement('div')
    playerDiv.classList.add('row')

    let playerText = document.createElement('h2')
    playerText.classList.add('d-flex')
    playerText.classList.add('justify-content-center')
    playerText.classList.add('card-title')
    playerText.innerText = players + ' / ' + maxPlayers

    playerDiv.appendChild(playerText)
    cardBodyDiv.appendChild(playerDiv)

    // Adress
    let adressDiv = document.createElement('div')
    adressDiv.classList.add('row')

    let adressText = document.createElement('p')
    adressText.classList.add('d-flex')
    adressText.classList.add('justify-content-center')
    adressText.classList.add('card-title')
    adressText.classList.add('text-decoration-underline')
    adressText.innerText = ip + ':' + port

    adressDiv.appendChild(adressText)
    cardBodyDiv.appendChild(adressDiv)


    // Join
    let buttonDiv = document.createElement('div')
    buttonDiv.classList.add('row')

    let join = document.createElement('a')
    join.setAttribute('type', 'button')
    join.classList.add('d-flex')
    join.classList.add('justify-content-center')
    join.classList.add('btn')
    join.classList.add('btn-success')
    join.innerText = 'Join'
    join.setAttribute('href', 'steam://connect/' + ip + ':' + port)

    buttonDiv.appendChild(join)
    cardBodyDiv.appendChild(buttonDiv)

    cardDiv.appendChild(cardBodyDiv)
    container.appendChild(cardDiv)
}

window.onload = function () {
    servers.forEach(function (server) {
        addCard(server.map, server.gamemode, server.ip, server.port, server.player, server.max_player, server.host, server.name)
    })


    document.onclick = function (event) {
        let playersListDiv = document.getElementById('players_list')
        if (!htmlElementClicked(event, 'players_list')) {
            playersListDiv.classList.add('visually-hidden')
        }
    }
}

function closeToast() {
    document.getElementById('toast').classList.add('visually-hidden')
}

function showToast() {
    document.getElementById('toast').classList.remove('visually-hidden')
}

function imageExists(image_url) {
    let http = new XMLHttpRequest()
    http.open('HEAD', image_url, false)
    http.send()
    return http.status != 404
}

function htmlElementClicked(event, id){
    let clickPlayersListDiv = false
        for (let indexElement in event['path']) {
            if (event['path'][indexElement].id == id) clickPlayersListDiv = true
        }
    return clickPlayersListDiv
}
