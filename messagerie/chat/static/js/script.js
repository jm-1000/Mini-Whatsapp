let createChat, submitGrBtn, createGrInput, checkInputs, usersSelected, 
  inputGr, renameGr, deleteGr, addUserGr, addUserGrBtn, checkboxes,
  members,asideadm, usersDelBtns, uuid, data, readMsg, lastMsg, setupChat
const usernav = document.getElementById('usernav')
const create = document.getElementById('create')
const noSelectedChatMsg = document.querySelector('.divtemp');
const createChatBtn = document.getElementById('createChatBtn')
const chatList = document.querySelector('.chat > ul')
const msgClass = document.querySelector('.message')
const createChatUrl = 'chat/create/'
const getChatUrl = '/chat/'
const mediaScreen = window.matchMedia("(min-width: 768px)");
const sectionTemp = document.createElement('section');
const alert = document.getElementById('alert');


document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', onPageClick)
  document.getElementById('userBtn').addEventListener('click', userBtnClick)
  usernav.addEventListener('click', (e) => {e.stopPropagation()})
  create.addEventListener('click', (e) => {e.stopPropagation()}) 
  createChatBtn.addEventListener('click', createChatBtnClick)

  function onPageClick(e) {
    if (!usernav.classList.value.match('moveUsernav')) {
      usernav.classList.add('moveUsernav');
    }
    if (!create.classList.value.match('moveCreate')) {
      create.classList.add('moveCreate');
      document.getElementById("createGr").style.display = 'none';
    }
  }

  function userBtnClick(e) {
    e.stopPropagation()
    if (usernav.classList.value.match('moveUsernav')) {
        usernav.classList.remove('moveUsernav')
    } else {
        usernav.classList.add('moveUsernav')
    }
  }

  function createChatBtnClick(e) {
    e.stopPropagation()
    if (create.classList.value.match('moveCreate')){
      fetchData(createChatUrl, createChatOperations)
      create.classList.remove('moveCreate')
      document.getElementById('createChat').style.display = 'block'
    }else {
      document.getElementById('createGr').style.display = 'none'
      create.classList.add('moveCreate')
    }
  }
})

function fetchData(url, func) {
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
    console.error('Erreur en fetching:', error);
  });
}

function websocketClient() {
  websocket = new WebSocket('ws://' + window.location.host);
  websocket.onopen = function(e){
    console.log('Connexion Websocket réussi.')
  }
  websocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log(data.action)
    switch (data.action) {
      case "getChats":
        getChats();
        break
      case "message":
        updateChat(data.chat);
        break
      case "createChat":
        newChat(data.chat);
        break
      case "newChat":
        websocketSend(data.chat);
        break
      case "deleteChat":
        postDeleteChat(data.chat);
        break
      case "changeChat":
        postChangeChat(data.chat);
        break
      case 'connected':
        userStatus(data.status, data.chat);
        break
      }
  }
  websocket.onclose = function(e) {
    console.log('Connexion Websocket non réussi ou perdu, reessayer en 2s.')
    setTimeout(() => {
      websocketClient();
      getChats()
      }, 2000);
  }

  function websocketSend(uuid, action='connect', text=null, usernames=null) {
    const data = {
      'action' : action,
      'usernames' : usernames,
      'text' : text, 
      'uuid':uuid
    }
    websocket.send(JSON.stringify(data))
  }

  function getChats(){
    fetchData(getChatUrl, function(data) {
      chatList.innerHTML = data;
      Array.from(chatList.children).forEach(item => {
        websocketSend(item.getAttribute("id").split('id')[1])
      })
      chatList.addEventListener('click', (e) => {
          try {
            setupChat.init(e.target.getAttribute("id").split('id')[1])
          } catch {
            try { 
              setupChat.init(e.target.parentElement.getAttribute("id").split('id')[1])
            } catch {
              try{
                setupChat.init(e.target.parentElement.parentElement.getAttribute("id").split('id')[1])
              } catch {}
            } 
          }
      })
    })
  } 
  
  function updateChat(uuid) {
    readMsg = document.querySelector('.readMsg > ul');
    if (readMsg){
      if (readMsg.getAttribute('id') === ('id' + uuid)){
        fetchData(getChatUrl + uuid, getNewMsg);
      }
    }  
    fetchData(getChatUrl, (data) => {updateChatList(data, uuid)});
  }
  
  function getNewMsg(data) {
    sectionTemp.innerHTML = data;
    lastMsg = sectionTemp.querySelector('.readMsg ul li:last-child');
    readMsg.append(lastMsg);       
    setupChat.moveScrollAtBottom();
  }

  function updateChatList(data, uuid) {
    sectionTemp.innerHTML = data;
    let target = chatList.querySelector('#id' + uuid);
    if (!document.querySelector('.readMsg #id' + uuid)) {
      mobileAlert(sectionTemp.querySelector('#id' + uuid + ' div'))
    }
    if (target) {
      target.remove();
      target.innerHTML = sectionTemp.querySelector('#id' + uuid).innerHTML;
      chatList.prepend(target);
    } else {
      // getChats();
      chatList.prepend(sectionTemp.querySelector('#id' + uuid));
    }
  }

  function userStatus(status, uuid) {
    if (msgClass.querySelector('#id' + uuid)){
      msgClass.querySelector('header p').innerHTML = status;
    }
  }

  function postChangeChat(uuid) {
    const aside = document.querySelector("aside")
    readMsg = document.querySelector('.readMsg > ul');
    if (readMsg){
      if (readMsg.getAttribute('id') === ('id' + uuid)){
        // setupChat.init(uuid, false)
        console.log('ok')
        fetchData(getChatUrl + uuid, function(data) {
          sectionTemp.innerHTML = data;
          let ul = msgClass.querySelector(".readMsg ul")
          ul.innerHTML = sectionTemp.querySelector(".readMsg ul").innerHTML
          let header = msgClass.querySelector("header")
          header.innerHTML = sectionTemp.querySelector("header").innerHTML
          let create = msgClass.querySelector(".aside")
          create.innerHTML = sectionTemp.querySelector(".aside").innerHTML
          if (aside.querySelector('#inputGr')) {
            console.log(uuid)
            menuGrAdmOperation(uuid)
          }
        })
      }
    // getChats()
    }
  }

  function postDeleteChat(uuid) {
    websocketSend(uuid, 'disconnect');
    getChats();
    let readMsg = document.querySelector('.readMsg ul');
    let chat = chatList.querySelector('#' + readMsg.getAttribute('id'));
    if (readMsg && chat) {
      setupChat.switchTabMobileScreen()
      let div = noSelectedChatMsg.cloneNode(true), text;
      text = "Le chat ou groupe a été supprimé!<br>";
      div.firstElementChild.innerHTML = text + div.firstElementChild.innerHTML
      readMsg.parentNode.parentNode.innerHTML = div.outerHTML;
    }
  }

  alert.addEventListener('click', (e) => {
    postChangeChat(e.target.getAttribute('id').split('id')[1]);
  })
  
  const mobileAlert = (alertTag) => {  
    const mediaQuery = window.matchMedia("(min-width: 768px)");
    if (!mediaQuery.matches && !document.querySelector('.chat').checkVisibility()) {
      alert.innerHTML = alertTag.innerHTML;
        alert.style.display = 'block';
        alert.classList.add('alert');
      setTimeout(() => {
        alert.classList.remove('alert');
        alert.style.display = 'none';
      }, 5050);
    }
  }

  function newChat(uuid) {
    setupChat.init(uuid)
    document.getElementById('create').classList.add('moveCreate')
  }
    
  return websocketSend;
}


setupChat = (function() {
  
  function init(uuid, switchTab=true) {
    websocketSend(uuid)
    fetchData(getChatUrl + uuid, function(data) {
      msgClass.innerHTML = data;
      moveScrollAtBottom()
      switchTabMobileScreen(switchTab);        
      sendingMsg();
      autoSizeTextarea();
      menuListenner()
      websocketSend(uuid, 'connected')
    })
  }

  function moveScrollAtBottom() {
    var readMsg = msgClass.querySelector('.readMsg')
    readMsg.scrollTop = readMsg.scrollHeight
  }

  function autoSizeTextarea() {
    msgClass.addEventListener('input', (e) => {
      if (e.target.tagName === 'TEXTAREA') {
        e.target.style.height = '0';
        e.target.style.height = (e.target.scrollHeight) + "px";  
      }
    })
  }

  function switchTabMobileScreen(switchTab) {  
    if (!mediaScreen.matches ) {
        if (chatList.checkVisibility() && switchTab){
          chatList.parentElement.style.display = 'none';
        } else {
          chatList.parentElement.style.display = 'block';
        }
        msgClass.addEventListener('click', function(e) {
          if (e.target.tagName === 'IMG' && e.target.parentElement.classList.contains('backBtn')) {
            chatList.parentElement.style.display = 'block';
          }
        }, true)
    } 
  }

  function sendingMsg() {
    let uuid = msgClass.querySelector(".readMsg ul").getAttribute('id').split('id')[1]
    let input = msgClass.querySelector('#id_text')
    let send = () => {
        if (input.value.trim() != "") {
          websocketSend(uuid, 'message', input.value);
          input.value = '';
        }
    }
    msgClass.addEventListener('click', function(e) {
      if (e.target.classList.contains('inputMsgBtn')) {
        send()
      }
    })
    msgClass.addEventListener('keyup', function(e) {
      if (e.target.tagName === 'TEXTAREA' && e.keyCode === 13){
        send()
      }
    })

  }
  
  function menuListenner() {
    uuid = msgClass.querySelector(".readMsg ul").getAttribute('id').split('id')[1]
    deleteGr = document.getElementById('deleteGr')
    const aside = document.querySelector("aside")

    const displayMenu = (e) => {
      e.stopPropagation()
      if (aside.classList.value.match('moveAside') == null) {
          aside.classList.add('moveAside')
      } else {
          aside.classList.remove('moveAside')
      } 
    }
    msgClass.querySelector('header').addEventListener('click', displayMenu)
    aside.addEventListener('click', (e) => {e.stopPropagation()})
    document.addEventListener('click', (e) => {
      aside.classList.add('moveAside')
    })
    
    if (aside.querySelector('#inputGr')) {
      menuGrAdmOperation(uuid)
    } else {
      aside.addEventListener('click', (e) => {
        console.log(e.target)
        if (e.target.classList.contains('deleteGr')) {
          websocketSend(uuid, 'deleteGr')
          aside.classList.add('moveAside');
          switchTabMobileScreen()
          msgClass.innerHTML = noSelectedChatMsg.outerHTML
        }
      // deleteGr.addEventListener('click', (e) => {
        
      // }) 
      })
    }
  }

  return {
    init,
    moveScrollAtBottom,
    switchTabMobileScreen
  }
})();

const websocketSend = websocketClient()

function createChatOperations(data) {
  create.innerHTML = data;
  submitGrBtn = create.querySelector('img')
  createGrInput = create.querySelector('input')
  checkInputs = create.querySelectorAll('label input')
  createChat = document.getElementById('createChat')
  createChat.style.display = 'block';
  usersSelected = []

  createChat.querySelectorAll('.user').forEach(element => {
    element.addEventListener('click', (e) => {
      websocketSend(null, action='createChat', null, usernames=e.target.innerHTML);
    })
  })

  create.querySelector('#createGrBtn').addEventListener('click', createGrDisplay)

  checkInputs.forEach(item => {
    item.addEventListener('click', pushSliceUser)
  })
  createGrInput.addEventListener('input', displayBtn)
  submitGrBtn.addEventListener('click', () => {
    if (createGrInput.value != '' && usersSelected.length != 0) {
      websocketSend(null, action='createGr', text=createGrInput.value, usernames=usersSelected)} 
  })

  function createGrDisplay() {
    document.getElementById('createGr').style.display = 'block';
    createChat.style.display = 'none';
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

  function displayBtn() {
    if (createGrInput.value != '' && usersSelected.length > 0) {
      submitGrBtn.style.display = 'block';
    } else {
      submitGrBtn.style.display = 'none'
    }
  }
}

function menuGrAdmOperation(uuid) {
  const aside = document.querySelector(".aside");
  inputGr = aside.querySelector('#inputGr');
  renameGr = aside.querySelector('#renameGr');
  deleteGr = aside.querySelector('#deleteGr');
  addUserGr = aside.querySelector('#addUserGr');
  addUserGrBtn = aside.querySelector('#addUserGrBtn');
  checkboxes = aside.querySelectorAll('.option');
  members = aside.querySelectorAll('.members');
  asideadm = aside.querySelector('.asideadm');
  usersDelBtns = aside.querySelectorAll('.user img');

  renameGr.addEventListener('click', (e) => {
    if(inputGr.value) {
      websocketSend(uuid, 'renameGr', inputGr.value)
      aside.classList.add('moveAside');
    }
  })

  deleteGr.addEventListener('click', (e) => {
    websocketSend(uuid, 'deleteGr')
    aside.classList.add('moveAside');
  })

  addUserGr.addEventListener('click', displayUserList)

  addUserGrBtn.addEventListener('click', (e) => {
    let usernames = []
    checkboxes.forEach(element => {
      if (element.checked) {
        usernames.push(element.value);
        element.checked = false;
      }
    })
    if (usernames.length > 0) {
      websocketSend(uuid, 'addUsersGr', null, usernames)
      aside.classList.add('moveAside');
      displayUserList();
    }
  })

  function displayUserList() {
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
      this.firstElementChild.style.display = 'block'
      this.lastElementChild.style.display = 'none'
    }else {
      this.lastElementChild.style.display = 'block'
      this.firstElementChild.style.display = 'none'
      asideadm.style.display = 'block';
      addUserGrBtn.style.display = 'block';
    }
  }

  usersDelBtns.forEach(element => {
    element.addEventListener('click', (e) => {
      websocketSend(uuid, 'deleteUserGr', null, e.target.getAttribute('id'))
    })
  })
};

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
