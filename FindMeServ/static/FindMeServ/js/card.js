function addCard(map, gamemode, adress, players, maxPlayers) {
    let container = document.getElementById('container-server')

    let cardDiv = document.createElement("div")
    cardDiv.classList.add("card")
    cardDiv.id = 'card'

    // Image
    let image = document.createElement("img")
    image.classList.add("card-img-top")
    image.src = static_url + "FindMeServ/img/"+ map +".jpg"

    let cardBodyDiv = document.createElement("div")
    cardBodyDiv.classList.add("card-body")
    cardBodyDiv.classList.add("container-fluid")

    cardDiv.appendChild(image)

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

    let adressUnderline = document.createElement("u")

    adressUnderline.innerText = adress
    adressText.appendChild(adressUnderline)
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
    join.setAttribute('href', "https://google.com")

    gamemodeDiv.appendChild(join)
    cardBodyDiv.appendChild(gamemodeDiv)

    cardDiv.appendChild(cardBodyDiv)
    container.appendChild(cardDiv)
}

window.onload = function () {
    addCard("de_overpass", "Retake", "127.198.13:17015", 5, 10)
}