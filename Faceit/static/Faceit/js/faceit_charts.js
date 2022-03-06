function generateCharts() {
    let room_id = document.getElementById('room_id').value
    let formData = new FormData()
    formData.append('room_id', room_id)
    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value
    const request = new Request('/faceit/get-room-stats/', {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': csrfTokenValue}
    })
    fetch(request)
        .then(response => response.json())
        .then(response => {
            populateCharts(response)
        })
}

function populateCharts(response) {
    let chartsDiv = document.getElementById('charts')

    document.getElementById('div_tmp')?.remove()

    let div = document.createElement('div_tmp')
    div.id = 'div_tmp'

    let canvas1 = createCanvas('100%', '27%')
    let canvas2 = createCanvas('100%', '27%')

    div.appendChild(canvas1)
    div.appendChild(canvas2)

    chartsDiv.append(div)

    createChart(canvas1.getContext('2d'), response.stats_team_1)
    createChart(canvas2.getContext('2d'), response.stats_team_2)
}

function createCanvas(width, height) {
    let canvas = document.createElement('canvas')
    canvas.setAttribute('width', width)
    canvas.setAttribute('height', height)
    return canvas
}

function createChart(canvas, team_info) {
    let mapsStats = team_info.team_info.maps_stats

    let winRate = Object.keys(mapsStats).map(csgo_map => {
        return mapsStats[csgo_map]['Win Rate %']
    })

    let timesPLayed = Object.keys(mapsStats).map(csgo_map => {
        return mapsStats[csgo_map]['times_played']
    })

    let winRateDataSet = {
        type: 'bar',
        label: 'Win rate',
        yAxisID: 'y-axis-wr',
        data: winRate,
        backgroundColor: '#ADD8E6',
        borderWidth: 1
    }

    let timesPLayedDataset = {
        type: 'bar',
        label: 'Times map played by the team',
        yAxisID: 'y-axis-tp',
        data: timesPLayed,
        backgroundColor: '#FF7F7F',
        borderWidth: 1
    }

    let datasets = [winRateDataSet, timesPLayedDataset]

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: Object.keys(mapsStats),
            datasets: datasets,
        },
        options: {
            scales: {
                'y-axis-wr': {
                    id: '',
                    position: 'left',
                    type: 'linear',
                    min: 20,
                    max: 80,

                },
                'y-axis-tp': {
                    id: '',
                    position: 'right',
                    type: 'linear',
                    min: 0,
                    grid: {
                        drawOnChartArea: false,
                    },
                },
            },

            plugins: {
                title: {
                    display: true,
                    text: team_info.team_name[0].toUpperCase() + team_info.team_name.slice(1)
                }
            }
        }
    })

}
