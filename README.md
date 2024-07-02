# Mini-Whatsapp

![login](/images/login.png)
## Project Overview
Mini-Whatsapp is a comprehensive full-stack web chat application developed over three months as part of a university module assessment in the second year. The project's goal was to implement a client-server architecture that enables real-time communication between users.

![group](/images/group.png)

Powered by Django, the application leverages Django Channels and WebSockets to facilitate instant messaging features. It's designed to mimic the core functionalities of the popular messaging app, Whatsapp, with a focus on real-time interactions.

## Features

- **User Account Management**: Users can create and update their personal accounts.
- **Chat Functionality**: Ability to create and delete individual or group chats.
- **Group Management**: Group administrators can manage chat groups effectively.
- **Real-Time Messaging**: Send and receive messages instantly without any delay.
- **Message Confirmation**: Confirmations for message delivery and reception.
- **User Status**: Displays the last login status of users.
- **Mobile Notifications**: Popout notifications for new messages on mobile web browsers.

![mobile](/images/mobile1.png)

![mobile](/images/mobile2.png)


## Installation Guide (Linux)

- Create a Python Virtual Environment: `python3 -m venv [environment_name]`

- Activate the Virtual Environment: `cd [environment_name]; source bin/activate`

- Download and extract the repository

- Install Dependencies: `pip3 install -r messagerie/requirements.txt`

- For some reason we have to reinstall the channels package : `pip uninstall channels; pip3 install --upgrade channels`

- Set up database schema: `python3 messagerie/manage.py migrate`

- Start the Server: `python3 messagerie/manage.py runserver`

Enjoy the seamless chat experience with Mini-Whatsapp!