function addCard(map, gamemode, ip, port, players, maxPlayers, host, name) {
    let container = document.getElementById('container-server')

    let cardDiv = document.createElement("div")
    cardDiv.classList.add("card")
    cardDiv.classList.add("m-4")
    cardDiv.id = 'card'

    // Image
    let image = document.createElement("img")
    image.classList.add("card-img-top")
    image.src = static_url + "FindMeServ/img/" + map + ".jpg"

    let cardBodyDiv = document.createElement("div")
    cardBodyDiv.classList.add("card-body")
    cardBodyDiv.classList.add("container-fluid")
    cardBodyDiv.classList.add("bg-light")

    cardDiv.appendChild(image)

    // Name
    let nameDiv = document.createElement("div")
    nameDiv.classList.add("row")

    let nameText = document.createElement("span")
    nameText.classList.add("justify-content-center")
    nameText.classList.add("card-title")
    nameText.classList.add("text-truncate")
    nameText.style.fontSize  = "small"
    nameText.setAttribute('data-bs-toggle', 'tooltip')
    nameText.setAttribute('title', name)
    nameText.innerText = name

    nameDiv.appendChild(nameText)
    cardBodyDiv.appendChild(nameDiv)

    // Host
    let hostDiv = document.createElement("div")
    hostDiv.classList.add("row")

    let hostText = document.createElement("p")
    hostText.classList.add("d-flex")
    hostText.classList.add("justify-content-center")
    hostText.classList.add("card-title")
    hostText.innerText = host

    hostDiv.appendChild(hostText)
    cardBodyDiv.appendChild(hostDiv)

    // Gamemode
    let gamemodeDiv = document.createElement("div")
    gamemodeDiv.classList.add("row")

    let gamemodeText = document.createElement("h5")
    gamemodeText.classList.add("d-flex")
    gamemodeText.classList.add("justify-content-center")
    gamemodeText.classList.add("card-title")
    gamemodeText.innerText = gamemode

    gamemodeDiv.appendChild(gamemodeText)
    cardBodyDiv.appendChild(gamemodeDiv)

    // Player
    let playerDiv = document.createElement("div")
    playerDiv.classList.add("row")

    let playerText = document.createElement("h2")
    playerText.classList.add("d-flex")
    playerText.classList.add("justify-content-center")
    playerText.classList.add("card-title")
    playerText.innerText = players + " / " + maxPlayers

    playerDiv.appendChild(playerText)
    cardBodyDiv.appendChild(playerDiv)

    // Adress
    let adressDiv = document.createElement("div")
    adressDiv.classList.add("row")

    let adressText = document.createElement("p")
    adressText.classList.add("d-flex")
    adressText.classList.add("justify-content-center")
    adressText.classList.add("card-title")
    adressText.classList.add("text-decoration-underline")
    adressText.innerText = ip + ":" + port

    adressDiv.appendChild(adressText)
    cardBodyDiv.appendChild(adressDiv)


    // Join
    let buttonDiv = document.createElement("div")
    gamemodeDiv.classList.add("row")

    let join = document.createElement("a")
    join.setAttribute('type', 'button')
    join.classList.add("d-flex")
    join.classList.add("justify-content-center")
    join.classList.add("btn")
    join.classList.add("btn-success")
    join.innerText = "Join"
    join.setAttribute('href', "steam://connect/" + ip + ":" + port)

    buttonDiv.appendChild(join)
    cardBodyDiv.appendChild(buttonDiv)

    cardDiv.appendChild(cardBodyDiv)
    container.appendChild(cardDiv)
}

window.onload = function () {
    servers.forEach(function (server) {
        addCard(server.map, server.gamemode, server.ip, server.port, server.player, server.max_player, server.host, server.name)
    })
}