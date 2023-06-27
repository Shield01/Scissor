# <h1 align="center"> Scissor </h1>

Brief is the new black, this is what inspires the team at Scissor. In today's world, it's important to keep things as short as possible, and this applies to more concepts than you may realize. From music, speeches, to wedding receptions, brief is the new black. Scissor is a simple tool which makes URLs as short as possible. Scissor thinks it can disrupt the URL shortening industry and give the likes of bit.ly and ow.ly a run for their money within 2 years.

# Features:

1. Shorten long URL links : Convert long URLs to a random short string

2. Create custom shortened URLs : Specify the short URL you would like to convert your long URL to

3. Monitor your shortened URL metrics : Track the amount of traffic being directed to your shortened URL

4. Manage your shortened URLs : Enable and Disable your shortened URLs at will.

5. Gracful Forwarding : You won't get redirected, if the destination website is down, due to any reason (e.g., server maintenance).

# API Documentation

Swagger Documentation :

Postman Documentation :

# File Structure

```bash
📦scissor_app
 ┣ 📂crud
 ┃ ┣ 📜url_crud.py
 ┃ ┗ 📜user_crud.py
 ┣ 📂routes
 ┃ ┣ 📜url_routes.py
 ┃ ┗ 📜user_routes.py
 ┣ 📂schemas
 ┃ ┣ 📜url_schemas.py
 ┃ ┗ 📜user_schemas.py
 ┣ 📂utils
 ┃ ┣ 📜auth.py
 ┃ ┣ 📜clean_objects.py
 ┃ ┣ 📜get_db.py
 ┃ ┣ 📜graceful_forwarding.py
 ┃ ┣ 📜http_response.py
 ┃ ┣ 📜keygen.py
 ┃ ┗ 📜responses.py
 ┣ 📜config.py
 ┣ 📜database.py
 ┣ 📜main.py
 ┣ 📜models.py
 ┗ 📜__init__.py
 ┃
 ┣📜README.md
 ┗📜requirements.txt

```

# License
