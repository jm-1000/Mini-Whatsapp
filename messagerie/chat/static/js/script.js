
document.getElementById('userBtn').addEventListener('click', function(e) {
    let usernav = document.getElementById('usernav')
    if (usernav.classList.value.match('moveUsernav') == null) {
        usernav.classList.add('moveUsernav')
    } else {
        usernav.classList.remove('moveUsernav')
    }
}) 

document.querySelectorAll('section').forEach(section => { 
    section.childNodes.forEach(child => {  
        child.addEventListener('click', function(e) {
            let usernav = document.getElementById('usernav')
            if (usernav.classList.value.match('moveUsernav') == null &&
                this != document.getElementById("userBtn") && this != usernav) {
                usernav.classList.add('moveUsernav')
            }
            let createUser = document.getElementById('createUser')
            if (document.querySelector('.header').checkVisibility &&
                this.parentElement != createUser && this != usernav) {
                createUser.style.display = 'none';
            }
            if (this.nodeName != 'HEADER' && this != document.getElementById("create")) {
                document.getElementById('create').classList.add('moveCreate')
                document.getElementById("createGr").style.display = 'none'
            }
        }) 
    })
})

document.querySelectorAll('#logout').forEach(element => { 
    element.addEventListener('click', function(e) {
        document.getElementById('login').style.display = 'block'  
        document.getElementById('usernav').classList.add('moveUsernav')
        document.getElementById('createUser').style.display = 'none'
        let sections = [".header", ".chat", ".message"]
        sections.forEach(section => {
            console.log(document.querySelector(section))
            document.querySelector(section).style.display = 'none';
        })
    })
}) 

document.getElementById('updateUser').addEventListener('click', function(e) {
    document.getElementById('createUser').style.display = 'block'
    document.getElementById('usernav').classList.add('moveUsernav')
}) 

document.getElementById('createUserBtn').addEventListener('click', function(e) {
    document.getElementById('createUser').style.display = 'block'
}) 

document.getElementById('createChatBtn').addEventListener('click', function(e) {
    let create = document.getElementById('create')
    if (create.classList.value.match('moveCreate') != null){
        create.classList.remove('moveCreate')
        document.getElementById('createChat').style.display = 'block'
    } else {
        create.classList.add('moveCreate')
    }
})

document.getElementById('createGrBtn').addEventListener('click', function(e) {
    document.getElementById('createGr').style.display = 'block'
    document.getElementById('createChat').style.display = 'none'
})
document.getElementById('backBtn').addEventListener('click', function(e) {
    document.querySelector('.chat').style.display = 'block'
})
document.querySelectorAll('.chat > ul li').forEach(element => {
    element.addEventListener('click', function(e) {
        setTimeout(function() {
            document.querySelector('.chat').style.display = 'none'
            }, 
        50)
    })
})

document.getElementById('id_text').addEventListener('input', function() {
    this.style.height = '0';
    this.style.height = (this.scrollHeight) + "px";  
});

let initialHeight = window.visualViewport.height
window.addEventListener('resize', () => {
    if (!window.visualViewport) {
      return;
    }
    let adjustedH = window.visualViewport.height/initialHeight * 100 - 5
    document.querySelector('body').style.gridTemplateRows = "2rem " + (adjustedH < 57 ? adjustedH : 95) + "%"
});
