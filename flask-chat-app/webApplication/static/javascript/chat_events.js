const socket = io(window.origin + '/chatroom')

class message_type{
    constructor(username,message,timestamp){
        this.username = username
        this.message = message
        this.timestamp = timestamp
    }

    user(){
        return `
        <h4 class="color-bl text-end"><strong>${this.username}</strong></h4>
        <div class="chat-member d-flex flex-column shadow-df bg-df p-3 cursor no-pt-events border-rd">
            <p class="lead color-bl">${this.message}</p>
        </div>
        <p class="text-muted text-end" style="font-style: italic">${this.timestamp}</p>`
    }

    global_member(){
        return `
        <h4 class="color-3"><strong>${this.username}</strong></h4>
        <div class="chat-member d-flex flex-column bg-5 shadow-df p-3 cursor no-pt-events border-rd">    
            <p class="lead color-df">${this.message}</p>
        </div>
        <p class="text-muted" style="font-style: italic">${this.timestamp}</p>`
    }
}


// socket-events

socket.on('global_message', data =>{
    if(data[0] !== socket.id){
        $('.messages-content').append(new message_type(data[1],data[2],data[3]).global_member())
    }else{
        $('.messages-content').append(new message_type(data[1],data[2],data[3]).user())
    }
    document.querySelector('.global-chat p').innerText = `${data[1]}: ${data[2]}`
  
})

// chat-app functions

document.onkeydown = (e) =>{
    if(e.keyCode === 13){
        send_message()
    }
}

document.querySelector('.send-btn').onclick = () =>{
    send_message()
}

const send_message = () =>{
   const message = document.querySelector('.message-input input')

   socket.emit('global_message', message.value)
   message.value = ''
}