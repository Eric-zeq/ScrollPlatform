# Scroll Plotform 
## Introduction
This project is a lifestyle platform centred on social sharing, aiming to create a comprehensive content community that integrates the exchange of life experiences, travel exploration, product reviews, and learning insights. The platform uses a waterfall layout to display content, combining text and images to provide users with an immersive browsing experience.
## Function
#### 1. User Identity Management
    ✅ Registration and Login
    New users can register an account via email and log in with a password.

    ✅ User Profile Page
    1. Displays basic information such as user avatar, nickname, and profile.
    2. Shows all posts published by the user.
    3. Displays posts that the user has liked and saved.
    4. Provides a function to edit personal information (such as changing the avatar and signature).

#### 2. Content Publishing and Browsing
    ✅ Browsing and Searching Posts
    1. All users can browse content displayed in a waterfall format on the home page.
    2. upports keyword search function, filter posts by title or content.

    ✅ Publishing Posts
    1. Users can upload images (supports multiple images).
    2. Fill in the post title and body content.
    3. After submission, it will be automatically saved and displayed on the home page and user's personal page.

#### 3. Social Interaction Features
    ✅ Comments
    1. Users can comment on posts published by others.
    2. Users can view comments posted by other users.

    ✅ Likes & Favourites
    1. Users can like or favourite posts they enjoy.
    2. Likes/Colloct are marked with a status indicator.

    ✅ Follow
    1. Users can follow other users to establish social connections.
    2. Users who are followed will receive a system notification.

#### 4. Notification Centre
    ✅ Activity Notifications
    1. Users receive real-time notifications when their posts are commented on, liked, or Colloct
    2. Users also receive notifications when they are followed by others

    ✅ Notification Management
    Users can view historical notification records

## Setup
1. Python 3.12+
2. Poetry
3. Docker

Steps
1. Clone repository
```shell
git clone https://github.com/Eric-zeq/ScrollPlatform.git
cd ScrollPlatform
```
2. Modify .Env
SECRET_KEY needs to be configured.
```shell
cd ScrollPlatform/scrollPlatform
mv .env.sample .env
```
4. Docker build
```shell
docker-compose up --build 
```
5. Run Project
```shell
docker-compose up -d
```
6. Open website
```
http://0.0.0.0:8000
```
