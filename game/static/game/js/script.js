const gameCode = JSON.parse(document.getElementById('game-code').textContent)
const playerName = JSON.parse(document.getElementById('player-name').textContent)
const iHaveGameCode = JSON.parse(document.getElementById('i-have-game-code').textContent)
const gameMatrixId = JSON.parse(document.getElementById('game-matrix-id').textContent)

var ws = new WebSocket('ws://127.0.0.1:8000/ws/asc/pg/' + gameCode + '/' + gameMatrixId + '/' + playerName + '/' + iHaveGameCode + '/')

let playerSymbol = 'X'
if (iHaveGameCode == 'on') {
    playerSymbol = 'O'
}

ws.onopen = function(){
    console.log('connection established...')
}

function func(box_id){
    let box_content = document.getElementById(box_id.toString()).textContent
    if(box_content == ''){
        ws.send(box_id)
    }    
}

ws.onmessage = function(event){
    var data = JSON.parse(event.data)
    if (data.msg_type == 'result') {
        var result = (data.msg == 'game drawn') ? ('Game Drawn 😄😄') : (data.msg + ' Wins... 🥳🥳')
        document.getElementsByClassName('modal-body')[0].textContent = result
        document.getElementById('result').click()
        console.log(data.msg)
    }
    else if(data.msg_type == 'chance'){

        var symbol = data.symbol == 'null' ? 'X': 'O'
        document.getElementById(data.position).textContent = symbol
    }
}

ws.onerror = function (event) {
    console.log('connection aborted...', event)
}