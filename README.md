# quiz-server
quiz-server is the backend server for the CCNS quiz contest.

# Prerequisites
- python 3.8
- poetry 1.1.4
- docker 20.10.2
- docker-compose 1.27.4

# Getting Started

## Using Quiz Service
- Belows are the example usage with Python requests module, for the full game flow please refer to `invoke_e2e_game_flow.py`.

### Register New Player
- Whenever a player register successfully, the profile will be responded.
- `platform_userid` is the user id of your platform, this allows you search the mapping with player uuid reversely.
```python
player_payload = {
    "name": "{PLAYER_NAME}",
    "platform": "{PLAYER_PLATFORM}",
    "platform_userid": "{PLAYER_PLATFORM_USERID}",
}
player_response = requests.post(
    "http://{SERVICE_HOST}:{SERVICE_PORT}/players/",
    data=player_payload
)
player_uuid = player_response.json()["player_uuid"]
```
- The platform field should be one of the belows:
    - Messenger
    - Telegram
    - Discord
    - Netcat
    - Line
    - Mewe
> Example Response
```
{
    "player_uuid": "0d82943d-22a9-47ec-b795-0ec927468a00",
    "name": "Rain",
    "platform": "Line",
    "platform_userid": "DiscordUser#8657",
    "correct_count": 0,
    "incorrect_count": 0,
    "no_answer_count": 16
}
```

- You also can check the profile for your player via the player_uuid anytime.
```python
check_url = "http://{SERVICE_HOST}:{SERVICE_PORT}/players/{PLAYER_UUID}/",
check_response = requests.get(check_url)
profile = check_response.json()
```

- You should maintain the mapping relationships between your platform user id and the player uuid on your service by default.
- But if you drop them accidently, you can search it by th mapping endpoint reversely.
```python
search_url = "http://{SERVICE_HOST}:{SERVICE_PORT}/mappings/{PLATFORM_USERID}/",
search_response = requests.get(search_url)
profile = search_response.json()
```


### Get Question Feed
- If the player has not finish all quiz, a new quiz will be fed within the response.
```python
feed_url = "http://{SERVICE_HOST}:{SERVICE_PORT}/feeds/{PLAYER_UUID}/"
feed_response = requests.get(feed_url)
quiz_uuid = feed_response.json()["quiz_uuid"]
```
> Example Response
```
{
    "quiz_uuid": "f2e9cdc1-b043-4fab-9248-34435e9506cf",
    "author": "IID",
    "domain": "CCNS",
    "description": "本社 (CCNS) 的英文全名為？",
    "level": "Medium",
    "options": [
        "The Cybersecurity & Computational Neuroscience Society",
        "The Casual Coders & Night Solders",
        "The CCNS Computer and Network Society",
        "The Campus Computer & Network Society"
    ],
    "comment": "nan"
}
```

- Otherwise, you will got HTTP 204 no content, which can help you notify the Q&A chat-bot user.

### Answer the Quiz
- You only need to report the content of player's answer, the quiz serve will judge the result for you.
```python
answer_paylaod = {
    "player_uuid": "{PLAYER_UUID}",
    "quiz_uuid": "{QUIZ_UUID}",
    "answer": "{ANSWER_CONTENT}",
}
answer_response = requests.post(
    "http://{SERVICE_HOST}:{SERVICE_PORT}/answers/",
    data=answer_paylaod
)
result = answer_response.json()["correct"]
```
> Example Response
```
{
    "player_uuid": "0d82943d-22a9-47ec-b795-0ec927468a00",
    "quiz_uuid": "f2e9cdc1-b043-4fab-9248-34435e9506cf",
    "correct": true
}
```

### Provokes Your Player
- The provokes message could be query by the correctness, you can fetch and store them locally at the initialize stage.
```python
provokes_response = request.get(
    "http://{SERVICE_HOST}:{SERVICE_PORT}/provokes/?correct={CORRECTNESS}"
)
messages = provokes_response.json()
```
> Example Response
```
[
    {
        "message": "你以為答對了就會有分數？",
        "correct": true
    }
]
```

### Pick Question Randomly
- If your players wanna practice more, you can also pick a quiz randomly for them, but you will get a HTTP 409 conflict status if you trying to post the answer for an answered quiz of the player.
```python
rand_url = "http://{SERVICE_HOST}:{SERVICE_PORT}/rand/"
rand_response = requests.get(rand_url)
```

### Check the Leaderboard
- The leaderboard will respond a players list which was sorted by the score.
```python
leaderboard_url = "http://{SERVICE_HOST}:{SERVICE_PORT}/leaderboard/"
response = self.client.get(leaderboard_url)
```
> Example Response
```
[
    {
        "name": "E2E_PLAYER",
        "platform": "Messenger",
        "score": 2
    },
    {
        "name": "Rain",
        "platform": "Line",
        "score": 1
    }
]
```

## Bear Running

### Prepare the .env File
- Set the `DJANGO_DEBUG` to **False**  for the production mode, which will block the delete method for all of endpoints to avoid cheating and malicious usage.
```zsh
$ cp .env.sample .env
```

### Setup venv
- Use poetry to build the virtual environment.
```zsh
$ poetry install --no-dev
```

### Run Tests
```zsh
$ poetry run inv test
```

### Run Service
- Remember to start a local PostgreSQL databse locally.
- Add the `--insecure` tag to serve static files through wsgi if you need a human-friendly GUI.
```zsh
$ poetry run python manage.py runserver [--insecure]
```

## Containerization

### Build the docker image
```zsh
$ docker build -t rainrainwu/quiz-server:2.0 .
```

### Start services
Server will listen on the port 8080, so make sure it was available.
```zsh
$ docker-compose up
```

### Stop services
```zsh
$ docker-compose down
```

## Load Data
- Please download the csv files from the google drive of CCNS org, and modified the filenames as below.
```
provokes.csv
quizzes.csv
```

- The run the script with django extension, it will purge all of old records by default.
```zsh
$ poetry run python manage.py runscript loader
```

# Contributors
[RainrainWu](https://github.com/RainrainWu)
