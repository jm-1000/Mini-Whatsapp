var websocket
websocketClient()
const initialMsgSection = document.querySelector('.divtemp');

const usernav = document.getElementById('usernav')
const create = document.getElementById('create')
document.getElementById('userBtn').addEventListener('click', function(e) {
    e.stopPropagation()
    if (usernav.classList.value.match('moveUsernav') == null) {
        usernav.classList.add('moveUsernav')
    } else {
        usernav.classList.remove('moveUsernav')
    }
}) 

document.querySelectorAll('section').forEach(section => { 
  section.addEventListener('click', function(e) {
      if (!usernav.classList.value.match('moveUsernav')) {
        usernav.classList.add('moveUsernav');
      }
      if (!create.classList.value.match('moveCreate')) {
        create.classList.add('moveCreate');
        document.getElementById("createGr").style.display = 'none';
      }
    }) 
})
usernav.addEventListener('click', (e) => {e.stopPropagation()})
create.addEventListener('click', (e) => {e.stopPropagation()})

const fetchData = (url, func) => {
  fetch(url)
  .then(response => {
    if (!response.ok) {
    throw new Error('Problème de connexion');
    }
    return response.text();
  })
  .then(data => {
    func(data)
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
}

let createChat, submitGrBtn, createGrInput, checkInputs
const usersSelected = []

document.getElementById('createChatBtn').addEventListener('click', function(e) {
  e.stopPropagation()
  if (create.classList.value.match('moveCreate') != null){
    fetchData('chat/create/', getUsers)
    create.classList.remove('moveCreate')
    document.getElementById('createChat').style.display = 'block'
  }else {
    document.getElementById('createGr').style.display = 'none'
    create.classList.add('moveCreate')
  }
})

function getUsers(data) {
  create.innerHTML = data;

  createChat = document.getElementById('createChat')
  submitGrBtn = create.querySelector('img')
  createGrInput = create.querySelector('input')
  checkInputs = create.querySelectorAll('label input')

  createChat.style.display = 'block';
  createChat.querySelectorAll('.user').forEach(element => {
    element.addEventListener('click', websocketSendChat)
  })
  document.getElementById('createGrBtn').addEventListener('click', createGrDisplay)

  checkInputs.forEach(item => {
    item.addEventListener('click', pushSliceUser)
  })
  createGrInput.addEventListener('input', displayBtn)
  submitGrBtn.addEventListener('click', websocketSendGr)
}

function websocketSendChat() {
  var data = {
    'action':'createChat',
    'username':this.innerHTML
  }
  websocket.send(JSON.stringify(data))
}

function websocketSendGr() {
  if (createGrInput.value != '' && usersSelected.length != 0) {
    var data = {
      'action' : 'createGr',
      'usernames' : usersSelected,
      'namegr' : createGrInput.value 
    }
    websocket.send(JSON.stringify(data))
  }
}

function createGrDisplay() {
  document.getElementById('createGr').style.display = 'block';
  createChat.style.display = 'none';
}

function displayBtn() {
  if (createGrInput.value != '' && usersSelected.length != 0) {
    submitGrBtn.style.display = 'block';
  } else {
    submitGrBtn.style.display = 'none'
  }
}

function pushSliceUser() {
  if (usersSelected.includes(this.value)) {
    var index = usersSelected.indexOf(this.value);
    if (index !== -1) {
      usersSelected.splice(index, 1);
    }
  } else {
    usersSelected.push(this.value);
  }
  displayBtn()
} 

const displayMsgAtBottom = () => {
  var readMsg = document.querySelector('.readMsg')
  readMsg.scrollTop = readMsg.scrollHeight
}
const websocketConnectChat = (uuid) => {
  websocket.send(JSON.stringify({
    'action':'connect',
    'uuid':uuid
  }))
} 
const autoSizeTextarea = () => {
  document.getElementById('id_text').addEventListener('input', (e) => {
  e.target.style.height = '0';
  e.target.style.height = (e.target.scrollHeight) + "px";  
 })
}

const handleMobileScreen = () => {  
    const mediaQuery = window.matchMedia("(min-width: 768px)");
    if (!mediaQuery.matches) {
        let chat = document.querySelector('.chat')
        if (chat.checkVisibility()){
          document.querySelector('.chat').style.display = 'none';
        } else {
          document.querySelector('.chat').style.display = 'block';
        }
        document.getElementById('backBtn').addEventListener('click', function(e) {
          chat.style.display = 'block';
        })
    } 
}

const handleMsg = () => {
  document.getElementById('inputMsgBtn').addEventListener('click', function(e) {
    let uuid = document.querySelector(".readMsg ul").getAttribute('id').split('id')[1]
    let input = document.getElementById('id_text').value
    if (input.trim() != "") {
      data = {
        'action':'message',
        'text': input,
        'uuid': uuid
      }
      input = ''
      websocket.send(JSON.stringify(data))
    }
  })
}

const displayUserList = (e) => {
  members.forEach(element => {
    if (element.checkVisibility()) {
      element.style.display = 'none';
    }else {
      element.style.display = 'block';
    }
  })
  if (asideadm.checkVisibility()) {
    asideadm.style.display = 'none';
    addUserGrBtn.style.display = 'none';
  }else {
    asideadm.style.display = 'block';
    addUserGrBtn.style.display = 'block';
  }
}

let aside, inputGr, renameGr, deleteGr, addUserGr, addUserGrBtn, checkboxes,
    members,asideadm, usersDelBtns, uuid, data
const menuGrAdmOperation = () => {
  aside = document.querySelector("aside")
  inputGr = document.getElementById('inputGr')
  renameGr = document.getElementById('renameGr')
  deleteGr = document.getElementById('deleteGr')
  addUserGr = document.getElementById('addUserGr')
  addUserGrBtn = document.getElementById('addUserGrBtn')
  checkboxes = document.querySelectorAll('.aside .option')
  members = document.querySelectorAll('.aside .members')
  asideadm = document.querySelector('.asideadm')
  usersDelBtns = document.querySelectorAll('.aside .user img')

  renameGr.addEventListener('click', (e) => {
    if(inputGr.value) {
      data = {
        'action' : 'renameGr',
        'namegr' : inputGr.value,
        'uuid': uuid
      }
      websocket.send(JSON.stringify(data))
      aside.classList.add('moveAside');
    }
  })
  deleteGr.addEventListener('click', (e) => {
    data = {'action':'deleteGr', 'uuid': uuid}
    websocket.send(JSON.stringify(data))
    aside.classList.add('moveAside');
  })
  addUserGr.addEventListener('click', (e) => {
    displayUserList()
  })
  addUserGrBtn.addEventListener('click', (e) => {
    data = {
      'action' : 'addUsersGr',
      'usernames' : [],
      'uuid': uuid
    }
    checkboxes.forEach(element => {
      if (element.checked) {
        data['usernames'].push(element.value);
        element.checked = false;
      }
    })
    if (data['usernames'].length > 0) {
      websocket.send(JSON.stringify(data)); 
      aside.classList.add('moveAside');
      displayUserList();
    }
  })
  usersDelBtns.forEach(element => {
    element.addEventListener('click', (e) => {
      data = {
        'action' : 'deleteUserGr',
        'username' : e.target.getAttribute('id'),
        'uuid': uuid
      }
    websocket.send(JSON.stringify(data));
  })
  })
}

const menuListenner = () => {
  uuid = document.querySelector(".readMsg ul").getAttribute('id').split('id')[1]
  deleteGr = document.getElementById('deleteGr')
  const aside = document.querySelector("aside")

  document.addEventListener('click', (e) => {
    aside.classList.add('moveAside')
  })
  const callback = (e) => {
    e.stopPropagation()
    if (aside.classList.value.match('moveAside') == null) {
        aside.classList.add('moveAside')
    } else {
        aside.classList.remove('moveAside')
    } 
  }
  document.querySelector('.message header').addEventListener('click', callback)
  aside.addEventListener('click', (e) => {e.stopPropagation()})
  
  if (aside.querySelector('#inputGr')) {
    menuGrAdmOperation()
  } else {
    deleteGr.addEventListener('click', (e) => {
    data = {'action':'deleteGr', 'uuid': uuid}
    websocket.send(JSON.stringify(data))
    aside.classList.add('moveAside');
    handleMobileScreen()
    document.querySelector('.message').innerHTML = initialMsgSection.outerHTML
    }) 
  }
  
}

const sectionTemp = document.createElement('section');
let readMsg, lastMsg, chats

const getNewMsg = (data) => {
  sectionTemp.innerHTML = data;
  lastMsg = sectionTemp.querySelector('.readMsg ul li:last-child');
  readMsg.append(lastMsg);
  displayMsgAtBottom();
}

const updateChatList = (data, uuid) => {
  sectionTemp.innerHTML = data;
  let target = chats.querySelector('#id' + uuid);
  if (target) {
    target.remove();
    target.innerHTML = sectionTemp.querySelector('#id' + uuid).innerHTML;
    chats.prepend(target);
  } else {
    getChats();
  }
}

function websocketClient() {
  websocket = new WebSocket('ws://' + window.location.host);
  websocket.onopen = function(e){
    console.log('Websocket connection established')
  }
  websocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    switch (data.action) {
      case "getChats":
        getChats();
        break
      case "message":
        console.log('ok1')
        updateChat(data.chat);
        break
      case "createChat":
        console.log('ok2')
        newChat(data.chat);
        break
      case "newChat":
        websocketConnectChat(data.chat);
        break
      case "deleteChat":
        postDeleteChat(data.chat);
        break
      case "changeChat":
        postChangeChat(data.chat);
        break
      case 'connected':
        userStatus(data.status);
        break
    }
  }
  websocket.onclose = function(e) {
    console.log('Websocket connection not established or lost, trying in 2s')
    setTimeout(() => {
      websocketClient();
      getChats()
      }, 2000);
  }
}

function userStatus(status) {
  document.querySelector('.message header p').innerHTML = status;
}

function postChangeChat(uuid) {
  getChats()
  fetchData('/chat/' + uuid, function(data) {
    document.querySelector('.message').innerHTML = data;
    displayMsgAtBottom()
    handleMsg();
    autoSizeTextarea();
    menuListenner()
    document.getElementById('backBtn').addEventListener('click', function(e) {
      chats.parentNode.style.display = 'block';
    })
  })
}

function postDeleteChat(uuid) {
  getChats()
  let readMsg = document.querySelector('.readMsg ul');
  let chat = document.querySelector('.chat #' + readMsg.getAttribute('id'));
  if (readMsg && chat) {
    handleMobileScreen()
    let div = initialMsgSection.cloneNode(true), text;
    text = "Le chat ou groupe a été supprimé!<br>";
    div.firstElementChild.innerHTML = text + div.firstElementChild.innerHTML
    readMsg.parentNode.parentNode.innerHTML = div.outerHTML;
  }
}

function getChats(){
  fetchData('/chat/', function(data) {
    document.querySelector('.chat > ul').innerHTML = data;
    linkChat()
  })
}

function updateChat(uuid) {
  chats = document.querySelector('.chat > ul');
  readMsg = document.querySelector('.readMsg > ul');
  if (readMsg){
    if (readMsg.getAttribute('id') === ('id' + uuid)){
      fetchData('/chat/' + uuid, getNewMsg);
    }
  }  
  fetchData('/chat/', (data) => {updateChatList(data, uuid)});
}

const setupChat = (uuid) => {
  websocketConnectChat(uuid)
  fetchData('/chat/' + uuid, function(data) {
    document.querySelector('.message').innerHTML = data;
    displayMsgAtBottom()
    handleMobileScreen()        
    handleMsg();
    autoSizeTextarea();
    menuListenner()
    websocket.send(JSON.stringify({'action':'connected', 'uuid':uuid}))
  })
}

function newChat(uuid) {
  setupChat(uuid)
  document.getElementById('create').classList.add('moveCreate')
}

function linkChat(){
  document.querySelectorAll('.chat > ul li').forEach(element => {
    var uuid = element.getAttribute("id").split('id')[1]
    websocketConnectChat(uuid)
    element.addEventListener('click', function(e) {
      setupChat(uuid)
    })
  })
}

let initialHeight = window.visualViewport.height
window.addEventListener('resize', () => {
  if (!window.visualViewport) {
  return;
  }
  let adjustedH = window.visualViewport.height/initialHeight * 100 - 5
  document.querySelector('body').style.gridTemplateRows = "2rem " + (adjustedH < 57 ? adjustedH : 95) + "%"
});

try {
  document.getElementById('updateUser').addEventListener('click', function(e) {
    document.getElementById('createUser').style.display = 'block'
    usernav.classList.add('moveUsernav')
  }) 

  document.getElementById('createUserBtn').addEventListener('click', function(e) {
    document.getElementById('createUser').style.display = 'block'
  }) 
} catch {}
